import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import community as com
import csv

attendees = {}

with open('attendees.csv') as attendees_csv:
    csv_reader = csv.reader(attendees_csv, delimiter=',')
    next(csv_reader, None)
    for row in csv_reader:
        attendees[row[5]] = [] + ([] if (not row[12] or "N/A" in row[12]) else [row[12]]) + ([] if (not row[13] or "N/A" in row[13]) else [row[13]])

G = nx.DiGraph()
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
nodes = G.nodes()
edge_labels = nx.get_edge_attributes(G,'weight')
pos = nx.nx_pydot.graphviz_layout(G)

partition = com.best_partition(G.to_undirected(), resolution=0.2)
cmap = mpl.colormaps['hsv']


plt.figure(figsize=(30, 30))
plt.axis('off')

nx.draw_networkx_edges(G, pos, width=1) 
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=7)

nx.draw_networkx_nodes(G, pos, partition.keys(), 
                       cmap=cmap, node_color=list(partition.values()),
                       node_size=[100 + v * 100 for v in degrees.values()],
                       alpha=0.8)

for node, (x, y) in pos.items():
    if node in attendees:
        plt.text(x, y - 0.1, node, ha='center', va='center', color='#000000', fontsize=10)
    else:
        plt.text(x, y - 0.1, node, ha='center', va='center', color='#ff0000', fontsize=10)

plt.savefig('graph.png', dpi=300, bbox_inches='tight')
plt.show()
