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

# Define the positions of the nodes
pos = {
    'A': (0, 1), 'B': (1, 2), 'C': (1, 0),
    'D': (2, 1), 'E': (3, 2), 'F': (3, 0),
    'Z': (4, 1)
}

# Step a: Depict the original graph
plt.figure()
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.suptitle("Original Graph", fontsize=14)
plt.show()

# Step b: State that Kruskal's Algorithm is being used for MST creation
print("Using Kruskal's Algorithm to find the Minimum Spanning Tree (MST)")

from networkx.algorithms.tree import minimum_spanning_edges

# Function to depict the graph step by step
def draw_mst_steps(G, mst_edges, pos):
    plt.figure()
    for i, edge in enumerate(mst_edges):
        plt.clf()  # Clear the current figure
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
        nx.draw_networkx_edges(G, pos, edgelist=mst_edges[:i+1], width=4, edge_color='red')
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        
        # Main title
        plt.suptitle("Kruskal's Algorithm - Minimum Spanning Tree", fontsize=14, y=1)
        
        # Step label on the canvas
        plt.annotate(f"Step {i+1}", xy=(0.5, -0.1), xycoords="axes fraction", ha="center", fontsize=12)
        
        plt.pause(1)  # Pause for 1 second for each step
    plt.show()

# Get the minimum spanning edges using Kruskal's algorithm
mst_edges = list(minimum_spanning_edges(G, algorithm='kruskal', data=False))

# Depict each step of MST creation using Kruskal's Algorithm
draw_mst_steps(G, mst_edges, pos)
