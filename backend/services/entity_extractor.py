"""Entity extraction service — SpaCy + GLiNER + LLM-based relationship extraction."""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Industrial equipment tag patterns
EQUIPMENT_TAG_PATTERNS = [
    r'\b[A-Z]{1,4}-\d{2,4}[A-Z]?(?:/[A-Z])?\b',  # P-101A, HX-201, V-301A/B
    r'\b[A-Z]{2,4}\d{3,4}[A-Z]?\b',                 # PMP101A, CMP201
    r'\b(?:Pump|Motor|Valve|Compressor|Heat\s*Exchanger|Tank|Vessel|Reactor|Column|Turbine)\s*(?:No\.?\s*)?\d+\b',
]


class EntityExtractor:
    """Extracts industrial entities and relationships from text."""

    def __init__(self):
        self._spacy_model = None
        self._gliner_model = None

    def _get_spacy_model(self):
        """Lazy-load SpaCy model."""
        if self._spacy_model is None:
            try:
                import spacy
                self._spacy_model = spacy.load("en_core_web_sm")
                logger.info("SpaCy model loaded")
            except Exception as e:
                logger.error(f"Failed to load SpaCy model: {e}")
        return self._spacy_model

    def _get_gliner_model(self):
        """Lazy-load GLiNER model."""
        if self._gliner_model is None:
            try:
                from gliner import GLiNER
                self._gliner_model = GLiNER.from_pretrained("urchade/gliner_multi-v2.1")
                logger.info("GLiNER model loaded")
            except Exception as e:
                logger.warning(f"GLiNER not available: {e}")
        return self._gliner_model

    async def extract_entities(self, text: str) -> list[dict]:
        """Combined entity extraction: regex + SpaCy + GLiNER."""
        entities = []
        seen = set()

        # 1. Regex-based equipment tag extraction
        for pattern in EQUIPMENT_TAG_PATTERNS:
            for match in re.finditer(pattern, text):
                tag = match.group()
                if tag not in seen:
                    entities.append({
                        "text": tag,
                        "type": "EQUIPMENT",
                        "start": match.start(),
                        "end": match.end(),
                        "source": "regex",
                    })
                    seen.add(tag)

        # 2. SpaCy NER
        nlp = self._get_spacy_model()
        if nlp:
            doc = nlp(text[:100000])  # Limit text size for SpaCy
            for ent in doc.ents:
                key = f"{ent.text}:{ent.label_}"
                if key not in seen:
                    # Map SpaCy labels to our types
                    mapped_type = self._map_spacy_label(ent.label_)
                    if mapped_type:
                        entities.append({
                            "text": ent.text,
                            "type": mapped_type,
                            "start": ent.start_char,
                            "end": ent.end_char,
                            "source": "spacy",
                        })
                        seen.add(key)

        # 3. GLiNER zero-shot entity extraction
        gliner = self._get_gliner_model()
        if gliner:
            try:
                industrial_labels = [
                    "equipment", "process parameter", "chemical",
                    "regulation", "safety procedure", "failure mode",
                    "measurement", "location",
                ]
                # Process in chunks to avoid memory issues
                chunk_size = 5000
                for i in range(0, len(text), chunk_size):
                    chunk = text[i:i+chunk_size]
                    gliner_entities = gliner.predict_entities(chunk, industrial_labels)
                    for ge in gliner_entities:
                        key = f"{ge['text']}:{ge['label']}"
                        if key not in seen and ge.get("score", 0) > 0.3:
                            entities.append({
                                "text": ge["text"],
                                "type": self._map_gliner_label(ge["label"]),
                                "start": i + ge.get("start", 0),
                                "end": i + ge.get("end", 0),
                                "score": ge.get("score", 0),
                                "source": "gliner",
                            })
                            seen.add(key)
            except Exception as e:
                logger.warning(f"GLiNER extraction failed: {e}")

        # 4. Regex for regulatory references
        reg_patterns = [
            r'\bOISD[-\s]?(?:STD[-\s])?\d+\b',
            r'\bIS[-\s]?\d{4,5}(?:[-\s]?\d{4})?\b',
            r'\bISO[-\s]?\d{4,5}(?:[-:]\d{4})?\b',
            r'\bAPI[-\s]?\d{3,4}\b',
            r'\bASME[-\s][A-Z]?\d+\b',
            r'\bFactory\s+Act\s+(?:Section\s+)?\d+\b',
        ]
        for pattern in reg_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                ref = match.group()
                if ref not in seen:
                    entities.append({
                        "text": ref,
                        "type": "REGULATION",
                        "start": match.start(),
                        "end": match.end(),
                        "source": "regex",
                    })
                    seen.add(ref)

        return entities

    async def extract_relationships(
        self, text: str, entities: list[dict]
    ) -> list[dict]:
        """Extract relationships between entities using LLM."""
        if not entities or len(entities) < 2:
            return []

        try:
            from services.llm_service import LLMService
            from utils.prompts import RELATIONSHIP_EXTRACTION_PROMPT

            llm = LLMService()
            entity_list = "\n".join(
                f"- {e['text']} (type: {e['type']})" for e in entities[:50]
            )

            prompt = RELATIONSHIP_EXTRACTION_PROMPT.format(
                text=text[:3000],
                entities=entity_list,
            )

            response = await llm.generate(prompt)
            relationships = self._parse_relationship_response(response)
            return relationships

        except Exception as e:
            logger.error(f"Relationship extraction failed: {e}")
            # Fallback: create basic relationships from co-occurrence
            return self._extract_cooccurrence_relationships(text, entities)

    def _extract_cooccurrence_relationships(
        self, text: str, entities: list[dict]
    ) -> list[dict]:
        """Fallback: extract relationships from entity co-occurrence in sentences."""
        import re
        sentences = re.split(r'[.!?\n]', text)
        relationships = []

        for sentence in sentences:
            entities_in_sentence = [
                e for e in entities
                if e["text"].lower() in sentence.lower()
            ]

            # Create relationships between co-occurring entities
            for i in range(len(entities_in_sentence)):
                for j in range(i + 1, len(entities_in_sentence)):
                    e1 = entities_in_sentence[i]
                    e2 = entities_in_sentence[j]
                    rel_type = self._infer_relationship_type(e1["type"], e2["type"])
                    if rel_type:
                        relationships.append({
                            "source": e1["text"],
                            "source_type": e1["type"],
                            "target": e2["text"],
                            "target_type": e2["type"],
                            "type": rel_type,
                            "context": sentence.strip()[:200],
                        })

        return relationships

    def _infer_relationship_type(self, type1: str, type2: str) -> Optional[str]:
        """Infer relationship type from entity types."""
        pair = frozenset([type1, type2])
        relationship_map = {
            frozenset(["EQUIPMENT", "DOCUMENT"]): "HAS_DOCUMENT",
            frozenset(["EQUIPMENT", "REGULATION"]): "GOVERNED_BY",
            frozenset(["EQUIPMENT", "FAILURE_MODE"]): "HAS_FAILURE_MODE",
            frozenset(["EQUIPMENT", "PROCEDURE"]): "FOLLOWS_PROCEDURE",
            frozenset(["EQUIPMENT", "PROCESS_PARAMETER"]): "MONITORS",
            frozenset(["EQUIPMENT", "PERSONNEL"]): "MAINTAINED_BY",
            frozenset(["REGULATION", "PROCEDURE"]): "COMPLIES_WITH",
            frozenset(["FAILURE_MODE", "PROCEDURE"]): "MITIGATED_BY",
        }
        return relationship_map.get(pair)

    def resolve_entities(self, entities: list[dict]) -> list[dict]:
        """Deduplicate entities using fuzzy matching."""
        if not entities:
            return []

        # Group by type
        by_type = {}
        for e in entities:
            by_type.setdefault(e["type"], []).append(e)

        resolved = []
        for entity_type, type_entities in by_type.items():
            seen_normalized = {}

            for e in type_entities:
                normalized = self._normalize_entity(e["text"], entity_type)

                if normalized in seen_normalized:
                    # Merge: keep the one with higher score or longer text
                    existing = seen_normalized[normalized]
                    if len(e["text"]) > len(existing["text"]):
                        seen_normalized[normalized] = e
                else:
                    seen_normalized[normalized] = e

            resolved.extend(seen_normalized.values())

        return resolved

    def _normalize_entity(self, text: str, entity_type: str) -> str:
        """Normalize entity text for deduplication."""
        text = text.strip()

        if entity_type == "EQUIPMENT":
            # Normalize equipment tags: remove spaces, uppercase
            text = re.sub(r'\s+', '', text).upper()
            # Remove common prefixes
            text = re.sub(r'^(PUMP|MOTOR|VALVE|COMPRESSOR)\s*', '', text, flags=re.IGNORECASE)

        return text.lower()

    def _map_spacy_label(self, label: str) -> Optional[str]:
        """Map SpaCy NER labels to our entity types."""
        mapping = {
            "PERSON": "PERSONNEL",
            "ORG": "ORGANIZATION",
            "DATE": "DATE",
            "GPE": "LOCATION",
            "LOC": "LOCATION",
            "FAC": "LOCATION",
            "PRODUCT": "EQUIPMENT",
            "QUANTITY": "MEASUREMENT",
        }
        return mapping.get(label)

    def _map_gliner_label(self, label: str) -> str:
        """Map GLiNER labels to our entity types."""
        mapping = {
            "equipment": "EQUIPMENT",
            "process parameter": "PROCESS_PARAMETER",
            "chemical": "CHEMICAL",
            "regulation": "REGULATION",
            "safety procedure": "PROCEDURE",
            "failure mode": "FAILURE_MODE",
            "measurement": "MEASUREMENT",
            "location": "LOCATION",
        }
        return mapping.get(label, label.upper())

    def _parse_relationship_response(self, response: str) -> list[dict]:
        """Parse LLM response into structured relationships."""
        relationships = []

        # Try to parse as JSON first
        try:
            import json
            data = json.loads(response)
            if isinstance(data, list):
                return data
        except (json.JSONDecodeError, TypeError):
            pass

        # Parse line-by-line format: "SOURCE -> RELATIONSHIP -> TARGET"
        for line in response.split("\n"):
            line = line.strip()
            if "->" in line:
                parts = [p.strip() for p in line.split("->")]
                if len(parts) >= 3:
                    relationships.append({
                        "source": parts[0],
                        "type": parts[1].upper().replace(" ", "_"),
                        "target": parts[2],
                    })

        return relationships
