"""Neo4j database client — async driver singleton."""

from neo4j import AsyncGraphDatabase, AsyncDriver
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class Neo4jClient:
    """Manages Neo4j async driver lifecycle and provides query helpers."""

    _driver: AsyncDriver | None = None

    @classmethod
    async def connect(cls) -> None:
        """Initialize the Neo4j async driver."""
        try:
            cls._driver = AsyncGraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_user, settings.neo4j_password),
            )
            # Verify connectivity
            await cls._driver.verify_connectivity()
            logger.info(f"Connected to Neo4j at {settings.neo4j_uri}")

            # Create constraints and indexes on startup
            await cls._create_schema()
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            cls._driver = None

    @classmethod
    async def _create_schema(cls) -> None:
        """Create indexes and constraints for the knowledge graph schema."""
        constraints = [
            "CREATE CONSTRAINT equipment_tag IF NOT EXISTS FOR (e:Equipment) REQUIRE e.tag IS UNIQUE",
            "CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.doc_id IS UNIQUE",
            "CREATE CONSTRAINT regulation_id IF NOT EXISTS FOR (r:Regulation) REQUIRE r.standard_id IS UNIQUE",
            "CREATE CONSTRAINT procedure_id IF NOT EXISTS FOR (p:Procedure) REQUIRE p.procedure_id IS UNIQUE",
            "CREATE CONSTRAINT personnel_id IF NOT EXISTS FOR (p:Personnel) REQUIRE p.employee_id IS UNIQUE",
            "CREATE CONSTRAINT maintenance_id IF NOT EXISTS FOR (m:MaintenanceRecord) REQUIRE m.work_order_id IS UNIQUE",
            "CREATE CONSTRAINT finding_id IF NOT EXISTS FOR (f:InspectionFinding) REQUIRE f.finding_id IS UNIQUE",
        ]
        indexes = [
            "CREATE FULLTEXT INDEX equipment_search IF NOT EXISTS FOR (e:Equipment) ON EACH [e.name, e.tag, e.type, e.manufacturer]",
            "CREATE FULLTEXT INDEX document_search IF NOT EXISTS FOR (d:Document) ON EACH [d.title, d.type, d.source]",
            "CREATE FULLTEXT INDEX regulation_search IF NOT EXISTS FOR (r:Regulation) ON EACH [r.title, r.standard_id, r.body]",
        ]

        async with cls.get_session() as session:
            for query in constraints + indexes:
                try:
                    await session.run(query)
                except Exception as e:
                    logger.warning(f"Schema setup warning: {e}")

        logger.info("Neo4j schema initialized")

    @classmethod
    def get_driver(cls) -> AsyncDriver:
        """Get the Neo4j driver instance."""
        if cls._driver is None:
            raise RuntimeError("Neo4j driver not initialized. Call connect() first.")
        return cls._driver

    @classmethod
    def get_session(cls):
        """Get an async session from the driver."""
        return cls.get_driver().session()

    @classmethod
    async def execute_query(cls, query: str, parameters: dict = None) -> list:
        """Execute a Cypher query and return results as list of dicts."""
        async with cls.get_session() as session:
            result = await session.run(query, parameters or {})
            records = await result.data()
            return records

    @classmethod
    async def execute_write(cls, query: str, parameters: dict = None) -> None:
        """Execute a write Cypher query."""
        async with cls.get_session() as session:
            await session.run(query, parameters or {})

    @classmethod
    async def close(cls) -> None:
        """Close the Neo4j driver."""
        if cls._driver:
            await cls._driver.close()
            cls._driver = None
            logger.info("Neo4j connection closed")

    @classmethod
    def is_connected(cls) -> bool:
        """Check if Neo4j is connected."""
        return cls._driver is not None
