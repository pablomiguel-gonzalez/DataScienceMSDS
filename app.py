import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Define the graph based on the mileage table
edges = [
    ('Origin', 'A', 40),
    ('Origin', 'B', 60),
    ('Origin', 'C', 50),
    ('A', 'B', 10),
    ('A', 'D', 70),
    ('B', 'C', 20),
    ('B', 'D', 55),
    ('B', 'E', 40),
    ('C', 'E', 50),
    ('D', 'E', 10),
    ('D', 'Destination', 60),
    ('E', 'Destination', 80)
]

# Initialize the graph
G = nx.DiGraph()
G.add_weighted_edges_from(edges)

# Streamlit UI
st.title("Shortest Path Finder")
st.write("Visualize and compute the shortest path from Origin to Destination.")

# Compute shortest path using Dijkstra's algorithm
shortest_path = nx.dijkstra_path(G, 'Origin', 'Destination')
shortest_distance = nx.dijkstra_path_length(G, 'Origin', 'Destination')

st.subheader("Shortest Path Result")
st.write(f"**Path:** {' → '.join(shortest_path)}")
st.write(f"**Total Distance:** {shortest_distance} miles")

# Draw the network
st.subheader("Network Visualization")

fig, ax = plt.subplots(figsize=(10, 6))

# Use spring layout for readability
pos = nx.spring_layout(G, seed=42)

# Draw nodes and edges
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1200, ax=ax, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)}, ax=ax)

# Highlight shortest path
edge_path = list(zip(shortest_path, shortest_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=edge_path, edge_color='red', width=3, ax=ax)

st.pyplot(fig)
