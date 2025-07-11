import requests

response = requests.post(
    "http://localhost:8000/query",
    json={
        "cypher": "MATCH (s:State) RETURN s.name AS state ORDER BY s.name",
        "parameters": {}
    }
)

print("States:")
for row in response.json().get("results", []):
    print("-", row["state"])
