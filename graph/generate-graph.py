import json
import faker
import random
import argparse
import faker_microservice

parser = argparse.ArgumentParser(description="Generates a mock graph")

parser.add_argument("--nodes-count", type=int, required=True, help="How many nodes should be included in the graph?")
parser.add_argument("--classes-count", type=int, required=True, help="How many classes should be included in the graph? (classes < nodes count)")
parser.add_argument("--props-count", type=int, required=True, help="How many properties should be included in the graph?")
parser.add_argument("--edge-count", type=float, required=True, help="Edges count")
parser.add_argument("--out", type=str, required=True, help="Output file for the graph")

args = parser.parse_args()

# Initialize faker
faker_api = faker.Faker()
faker_api.add_provider(faker_microservice.Provider)

# Create the graph
node_classes = [faker_api.microservice().replace("_", " ").replace("-", " ").title().replace(" ", "") for _ in range(args.classes_count)]
properties = [faker_api.bs() for _ in range(args.props_count)]

nodes_ids = list(range(args.nodes_count))
nodes = [{
    "id": i,
    "name": f"{faker_api.company()} {faker_api.company_suffix()}",
    "class": random.choice(node_classes)
} for i in nodes_ids]

# Create unique edges
edge_set = set()
final_edges = []

while len(final_edges) < args.edge_count:
    random_edge = {
        "sid": random.choice(nodes_ids),
        "tid": random.choice(nodes_ids),
        "name": random.choice(properties)
    }

    json_edge = json.dumps(random_edge)

    if json_edge not in edge_set:
        edge_set.add(json_edge)
        final_edges.append(random_edge)

out_graph = {
    "nodes": nodes,
    "edges": final_edges
}

with open(args.out, "w") as out_file:
    out_file.write(json.dumps(out_graph))
