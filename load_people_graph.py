# This script populates Neo4j with states and people living in those states.
from neo4j import GraphDatabase, basic_auth

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "testtest"

data = {
    "California": ["Alice", "Bob", "Carol"],
    "Texas": ["Dave", "Eve", "Frank"],
    "New York": ["Grace", "Heidi", "Ivan"]
}

driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD))

def create_people_graph(tx):
    for state, people in data.items():
        tx.run("MERGE (s:State {name: $state})", state=state)
        for person in people:
            tx.run("""
                MATCH (s:State {name: $state})
                MERGE (p:Person {name: $person})-[:LIVES_IN]->(s)
            """, state=state, person=person)

with driver.session() as session:
    session.write_transaction(create_people_graph)

driver.close()
print("Graph data loaded: states and people.")
