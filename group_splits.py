import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import community as com

from file_utils import attendees_and_preferences as attendees

G: nx.DiGraph = nx.DiGraph()
G.add_nodes_from(attendees.keys())

for attendee, preferences in attendees.items():
    for preference in preferences:
        if preference in attendees and attendee in attendees[preference]:
            G.add_edge(attendee, preference, weight=2)
        else:
            G.add_edge(attendee, preference, weight=1)

for index, SG in enumerate(nx.connected_components(G.to_undirected())):
    print(SG)

degrees = dict(G.degree)
nodes: nx.reportviews.NodeView = G.nodes()  # type: ignore[assignment]
edge_labels: dict[tuple[str, str], int] = nx.get_edge_attributes(G, "weight")
pos: dict[str, tuple[float, float]] = nx.nx_pydot.graphviz_layout(G)

partition: dict[str, int] = com.best_partition(G.to_undirected(), resolution=0.2)
cmap: plt.Colormap = mpl.colormaps["hsv"]

plt.figure(figsize=(30, 30))
plt.axis("off")

nx.draw_networkx_edges(G, pos, width=1)
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=7)

nx.draw_networkx_nodes(
    G=G,
    pos=pos,
    nodelist=partition.keys(),
    cmap=cmap,
    node_color=list(partition.values()),  # type: ignore[arg-type]
    node_size=[100 + v * 100 for v in degrees.values()],
    alpha=0.8,
)

node: str
x: float
y: float
for node, (x, y) in pos.items():
    if node in attendees:
        plt.text(
            x=x,
            y=y - 0.1,
            s=node,
            ha="center",
            va="center",
            color="#000000",
            fontsize=10,
        )
    else:
        plt.text(
            x=x,
            y=y - 0.1,
            s=node,
            ha="center",
            va="center",
            color="#ff0000",
            fontsize=10,
        )

plt.savefig("graph.png", dpi=300, bbox_inches="tight")
plt.show()
