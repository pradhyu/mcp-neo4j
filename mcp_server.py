import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from neo4j import GraphDatabase, basic_auth

# MCP server config
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "testtest")

app = FastAPI(title="MCP Neo4j Server")
driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD))

class QueryRequest(BaseModel):
    cypher: str
    parameters: dict = {}

@app.post("/query")
def run_query(request: QueryRequest):
    try:
        with driver.session() as session:
            result = session.run(request.cypher, **request.parameters)
            records = [record.data() for record in result]
        return {"results": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    try:
        with driver.session() as session:
            session.run("RETURN 1")
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
