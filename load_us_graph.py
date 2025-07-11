# This script populates the Neo4j database with US states, counties, and cities as a graph.
from neo4j import GraphDatabase, basic_auth

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "testtest"

data = {
    "California": {
        "counties": {
            "Los Angeles": ["Los Angeles", "Long Beach", "Glendale"],
            "San Diego": ["San Diego", "Chula Vista", "Oceanside"],
        }
    },
    "Texas": {
        "counties": {
            "Harris": ["Houston", "Pasadena", "Baytown"],
            "Dallas": ["Dallas", "Irving", "Garland"],
        }
    },
    "New York": {
        "counties": {
            "New York": ["New York City"],
            "Kings": ["Brooklyn"],
        }
    }
}

driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD))

def create_graph(tx):
    for state, state_data in data.items():
        tx.run("MERGE (s:State {name: $state})", state=state)
        for county, cities in state_data["counties"].items():
            tx.run("""
                MATCH (s:State {name: $state})
                MERGE (c:County {name: $county})-[:IN_STATE]->(s)
            """, state=state, county=county)
            for city in cities:
                tx.run("""
                    MATCH (c:County {name: $county})
                    MERGE (ci:City {name: $city})-[:IN_COUNTY]->(c)
                """, county=county, city=city)

with driver.session() as session:
    session.write_transaction(create_graph)

driver.close()
print("Graph data loaded: states, counties, and cities.")
