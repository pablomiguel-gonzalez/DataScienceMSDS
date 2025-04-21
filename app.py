import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Define the graph edges (road connections and distances)
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

# Initialize directed graph
G = nx.DiGraph()
G.add_weighted_edges_from(edges)

# Define custom layout to spread out towns for better readability
custom_pos = {
    'Origin': (0, 2),
    'A': (1, 3),
    'B': (2, 2),
    'C': (3, 3),
    'D': (3, 1),
    'E': (4, 2),
    'Destination': (5, 2)
}

# Streamlit UI
st.title("🚗 Shortest Path Explorer Between Towns")
st.markdown("Use the dropdowns below to explore the shortest route between any two towns.")

# Select origin and destination interactively
towns = list(G.nodes)
start_town = st.selectbox("Select starting town:", towns, index=0)
end_town = st.selectbox("Select destination town:", towns, index=towns.index("Destination"))

# Compute shortest path
if start_town != end_town:
    try:
        path = nx.dijkstra_path(G, source=start_town, target=end_town)
        distance = nx.dijkstra_path_length(G, source=start_town, target=end_town)
        st.success(f"**Shortest Path:** {' → '.join(path)}")
        st.info(f"**Total Distance:** {distance} miles")

        # Draw the graph
        fig, ax = plt.subplots(figsize=(10, 6))
        nx.draw(G, pos=custom_pos, with_labels=True, node_color='skyblue',
                node_size=1200, font_weight='bold', ax=ax)
        nx.draw_networkx_edge_labels(G, pos=custom_pos,
                                     edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)}, ax=ax)

        # Highlight path in red
        edge_path = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos=custom_pos, edgelist=edge_path,
                               edge_color='red', width=3, ax=ax)

        st.pyplot(fig)

    except nx.NetworkXNoPath:
        st.error(f"No path found between {start_town} and {end_town}.")
else:
    st.warning("Please select different towns for origin and destination.")

