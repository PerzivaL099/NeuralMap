from fastapi import FastAPI, HTTPException
from neo4j import GraphDatabase
import os

#Initializing FastAPI app
app = FastAPI(
    title="NeuralMap API",
    description="API for managing and querying the NeuralMap knowledge graph.",
    version="1.0.0"
)

#Database configuration
#TODO : Move these to environment variables or a config file
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

#Initialize Neo4j driver
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

@app.on_event("shutdown")
def close_driver():
    driver.close()

@app.get("/health/db")
def health_check_db():
    try:
        with driver.session() as session:
            result = session.run("RETURN 1 AS num")
            record = result.single()
            if record and record['num'] == 1:
                return {"status": "ok", "message":  "Connnected to Neo4j successfully."}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")