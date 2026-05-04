import os
from neo4j import AsyncGraphDatabase, AsyncDriver
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

class Neo4jDriver:
    _driver: Optional[AsyncDriver] = None

    async def connect(self):
        uri  = os.getenv("NEO4J_URI",      "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER",     "neo4j")
        pwd  = os.getenv("NEO4J_PASSWORD", "neuralmap")
        self._driver = AsyncGraphDatabase.driver(uri, auth=(user, pwd))
        # Verify connectivity
        await self._driver.verify_connectivity()
        print(f"[NeuralMap] Connected to Neo4j at {uri}")

    async def close(self):
        if self._driver:
            await self._driver.close()

    def get_session(self):
        if not self._driver:
            raise RuntimeError("Neo4j driver not initialised. Call connect() first.")
        return self._driver.session()

    async def apply_schema(self):
        """
        Idempotent schema bootstrap.
        Creates uniqueness constraints and indexes on first run.
        Neo4j will silently skip them if they already exist.
        """
        constraints = [
            # Every Node has a unique id
            "CREATE CONSTRAINT node_id_unique IF NOT EXISTS "
            "FOR (n:Node) REQUIRE n.id IS UNIQUE",

            # Every Edge relationship carries a unique id property
            # (Relationships don't get constraints in Neo4j CE,
            #  so we track edge ids on the relationship property)
            "CREATE INDEX edge_id_index IF NOT EXISTS "
            "FOR ()-[r:RELATES_TO]-() ON (r.id)",

            # Speed up viewport / spatial queries
            "CREATE INDEX node_type_index IF NOT EXISTS "
            "FOR (n:Node) ON (n.type)",

            "CREATE INDEX node_created_index IF NOT EXISTS "
            "FOR (n:Node) ON (n.created_at)",
        ]

        async with self.get_session() as session:
            for cypher in constraints:
                await session.run(cypher)

        print("[NeuralMap] Neo4j schema applied.")


# Module-level singleton — imported by routes & repos
neo4j_driver = Neo4jDriver()
