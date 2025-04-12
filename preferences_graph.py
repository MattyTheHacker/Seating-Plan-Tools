from pyvis.network import Network  # type: ignore[import-untyped]

import webbrowser

from file_utils import attendees as confirmed_attendees
from file_utils import named_attendees
from file_utils import edges


net = Network(
    notebook=True,
    cdn_resources="remote",
    bgcolor="#222222",
    font_color=True,
    height="1080px",
    width="100%",
    directed=True,
)

# Allows deleting edges for fitting onto tables.
net.show_buttons(["manipulation"])

# Graphs it.
for node in confirmed_attendees:
    net.add_node(str(node), color="green")

for node in named_attendees:
    net.add_node(str(node), color="red")

net.add_edges(edges)
net.show("graph.html")

# Opens it.
if input("Would you like to open the graph? (Y/N) >> ").lower() == "y":
    webbrowser.open("graph.html")
