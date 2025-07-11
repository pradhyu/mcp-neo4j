import requests

response = requests.post(
    "http://localhost:8000/query",
    json={
        "cypher": "MATCH (c:County {name: 'Harris'})-[:IN_STATE]->(s:State) RETURN s.name AS state",
        "parameters": {}
    }
)

result = response.json().get("results", [])
if result:
    print(f"Harris is in state: {result[0]['state']}")
else:
    print("No state found for Harris.")
