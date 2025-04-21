import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Define the graph edges with weights (miles between towns)
edges = {
    ('Origin', 'A'): 40,
    ('Origin', 'B'): 60,
    ('Origin', 'C'): 50,
    ('A', 'B'): 10,
    ('A', 'D'): 70,
    ('B', 'C'): 20,
    ('B', 'D'): 55,
    ('B', 'E'): 40,
    ('C', 'E'): 50,
    ('D', 'E'): 10,
    ('D', 'Destination'): 60,
    ('E', 'Destination'): 80
}

# Create graph
G = nx.DiGraph()
for (u, v), w in edges.items():
    G.add_edge(u, v, weight=w)

# Streamlit App
st.title("🚗 Shortest Path Finder Between Towns")

# User input: origin and destination
origin = st.selectbox("Select Starting Town", options=list(G.nodes), index=0)
destination = st.selectbox("Select Destination Town", options=list(G.nodes), index=list(G.nodes).index('Destination'))

# Compute shortest path
try:
    shortest_path = nx.dijkstra_path(G, source=origin, target=destination, weight='weight')
    path_length = nx.dijkstra_path_length(G, source=origin, target=destination, weight='weight')

    st.success(f"✅ Shortest path from **{origin}** to **{destination}** is:")
    st.markdown(" → ".join(shortest_path))
    st.info(f"Total Distance (or Cost/Time): **{path_length}** miles")

    # Plot the graph with the shortest path highlighted
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='gray')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    # Highlight shortest path
    path_edges = list(zip(shortest_path, shortest_path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)

    st.pyplot(plt.gcf())

except nx.NetworkXNoPath:
    st.error(f"No path found from {origin} to {destination}.")
