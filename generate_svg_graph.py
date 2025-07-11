import requests
import graphviz

# Query all nodes and relationships
response = requests.post(
    "http://localhost:8000/query",
    json={
        "cypher": """
            MATCH (n)-[r]->(m)
            RETURN labels(n) AS n_labels, n.name AS n_name, type(r) AS rel, labels(m) AS m_labels, m.name AS m_name
        """,
        "parameters": {}
    }
)

g = graphviz.Digraph('G', format='svg')
added = set()

for row in response.json().get("results", []):
    n_label = row["n_labels"][0]
    n_name = row["n_name"]
    m_label = row["m_labels"][0]
    m_name = row["m_name"]
    rel = row["rel"]
    n_id = f"{n_label}:{n_name}"
    m_id = f"{m_label}:{m_name}"
    if n_id not in added:
        g.node(n_id, f"{n_label}\n{n_name}")
        added.add(n_id)
    if m_id not in added:
        g.node(m_id, f"{m_label}\n{m_name}")
        added.add(m_id)
    g.edge(n_id, m_id, label=rel)

g.render(filename="full_graph", cleanup=True)
print("SVG graph generated as full_graph.svg")
