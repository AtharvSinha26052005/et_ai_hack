"""LLM Service — Google Gemini API wrapper with retry logic."""

import logging
import asyncio
from config.settings import settings

logger = logging.getLogger(__name__)


class LLMService:
    """Wrapper around Google Gemini for all LLM calls."""

    def __init__(self):
        self._model = None

    def _get_model(self):
        """Lazy-load the Gemini model."""
        if self._model is None:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI

                self._model = ChatGoogleGenerativeAI(
                    model=settings.llm_model,
                    google_api_key=settings.google_api_key,
                    temperature=0.1,
                    max_output_tokens=4096,
                )
                logger.info(f"Gemini model initialized: {settings.llm_model}")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
                raise
        return self._model

    async def generate(
        self,
        prompt: str,
        max_retries: int = 3,
        temperature: float = 0.1,
    ) -> str:
        """Generate a response from the LLM with retry logic."""
        model = self._get_model()

        for attempt in range(max_retries):
            try:
                response = await model.ainvoke(prompt)
                return response.content

            except Exception as e:
                if "429" in str(e) or "rate_limit" in str(e).lower():
                    # Rate limited — exponential backoff
                    wait_time = (2 ** attempt) * 2
                    logger.warning(
                        f"Rate limited (attempt {attempt + 1}/{max_retries}). "
                        f"Waiting {wait_time}s..."
                    )
                    await asyncio.sleep(wait_time)
                elif attempt < max_retries - 1:
                    logger.warning(f"LLM call failed (attempt {attempt + 1}): {e}")
                    await asyncio.sleep(1)
                else:
                    logger.error(f"LLM call failed after {max_retries} attempts: {e}")
                    raise

        raise RuntimeError("LLM call failed after all retries")

    async def generate_structured(
        self,
        prompt: str,
        output_schema: dict = None,
    ) -> str:
        """Generate structured (JSON) output from the LLM."""
        structured_prompt = prompt + "\n\nRespond ONLY with valid JSON. No markdown, no code blocks, no explanations."
        return await self.generate(structured_prompt)

    async def stream_generate(self, prompt: str):
        """Stream tokens from the LLM."""
        model = self._get_model()

        try:
            async for chunk in model.astream(prompt):
                if hasattr(chunk, "content") and chunk.content:
                    yield {"token": chunk.content}
        except Exception as e:
            logger.error(f"Stream generation failed: {e}")
            yield {"token": f"[Error: {str(e)}]"}
