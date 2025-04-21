import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# --- Page Setup ---
st.set_page_config(page_title="Fictional Roadtrip Shortest Path", layout="wide")
st.title("🚗 Fictional Roadtrip Across the U.S.")
st.markdown("Find the shortest route from San Francisco to Miami, passing through imaginary towns!")

# --- Define the Graph ---
edges = {
    ('Origin', 'A'): 40,
    ('Origin', 'B'): 15,
    ('A', 'C'): 25,
    ('A', 'D'): 10,
    ('B', 'A'): 20,
    ('B', 'D'): 30,
    ('C', 'Destination'): 20,
    ('D', 'C'): 15,
    ('D', 'Destination'): 35,
    ('E', 'Destination'): 10,
    ('B', 'E'): 50
}

G = nx.DiGraph()
for (u, v), w in edges.items():
    G.add_edge(u, v, weight=w)

# --- Custom Map-Like Coordinates (Imaginary US Locations) ---
custom_pos = {
    'Origin': (-120, 37),        # San Francisco
    'A': (-105, 39),             # Denver
    'B': (-87, 41),              # Chicago
    'C': (-74, 40),              # NYC
    'D': (-86, 36),              # Nashville
    'E': (-84, 33),              # Atlanta
    'Destination': (-80, 26)     # Miami
}

# Normalize coordinates
min_x = min(x for x, y in custom_pos.values())
max_x = max(x for x, y in custom_pos.values())
min_y = min(y for x, y in custom_pos.values())
max_y = max(y for x, y in custom_pos.values())

norm_pos = {
    node: (
        (x - min_x) / (max_x - min_x),
        (y - min_y) / (max_y - min_y)
    )
    for node, (x, y) in custom_pos.items()
}

# --- Shortest Path ---
source, target = "Origin", "Destination"
shortest_path = nx.dijkstra_path(G, source, target)
shortest_distance = nx.dijkstra_path_length(G, source, target)

# --- Sidebar Info ---
st.sidebar.header("Path Info")
st.sidebar.markdown(f"**Start:** {source}")
st.sidebar.markdown(f"**End:** {target}")
st.sidebar.markdown(f"**Shortest Path:** {' → '.join(shortest_path)}")
st.sidebar.markdown(f"**Total Distance:** {shortest_distance} miles")

# Optional step table
with st.expander("📊 View Step-by-Step Table"):
    path_data = []
    for i in range(len(shortest_path) - 1):
        u = shortest_path[i]
        v = shortest_path[i + 1]
        path_data.append({
            "From": u,
            "To": v,
            "Distance": G[u][v]["weight"]
        })
    st.dataframe(path_data)

# --- Draw Graph ---
fig, ax = plt.subplots(figsize=(10, 6))

# Base nodes and edges
nx.draw_networkx_nodes(G, norm_pos, node_color="#66b3ff", node_size=1200, ax=ax)
nx.draw_networkx_labels(G, norm_pos, font_size=12, font_weight='bold', ax=ax)
nx.draw_networkx_edges(G, norm_pos, edgelist=G.edges(), edge_color='gray', arrows=True, alpha=0.4, ax=ax)
nx.draw_networkx_edge_labels(G, norm_pos, edge_labels=nx.get_edge_attributes(G, 'weight'), font_size=9, ax=ax)

# Highlight shortest path
path_edges = list(zip(shortest_path[:-1], shortest_path[1:]))
nx.draw_networkx_edges(G, norm_pos, edgelist=path_edges, edge_color='red', width=3, arrows=True, ax=ax)

ax.set_title("📍 Shortest Path Roadtrip Map", fontsize=16)
ax.axis('off')
st.pyplot(fig)
