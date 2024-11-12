import networkx as nx
import matplotlib.pyplot as plt

# Create the graph
G = nx.Graph()

# Add edges along with their weights
edges = [
    ('A', 'B', 2), ('A', 'C', 7),
    ('B', 'D', 1), ('B', 'E', 5),
    ('C', 'D', 3), ('C', 'F', 10),
    ('D', 'Z', 6), ('D', 'F', 4),
    ('E', 'Z', 3), ('F', 'Z', 3)
]

G.add_weighted_edges_from(edges)

# Define the positions of the nodes to match the image
pos = {
    'A': (0, 1), 'B': (1, 2), 'C': (1, 0),
    'D': (2, 1), 'E': (3, 2), 'F': (3, 0),
    'Z': (4, 1)
}

# Draw the original graph
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Minimum Spanning Tree")
plt.show()