from pyvis.network import Network  # type: ignore[import-untyped]
from tkinter.filedialog import askopenfilename

import webbrowser


def main() -> None:
    path: str = askopenfilename(
        title="Select the input file",
        filetypes=[("Tab-separated values", "*.tsv")],
        initialdir=".",
    )

    if not path:
        print("No file selected.")
        return

    with open(path) as file:
        data = [line.split("\t") for line in file.read().split("\n") if line != "\t\t"]

    print(data)

    # Gets all the nodes and edges, ignoring and removing 'N/A'.
    confirmed_attendees: set[str] = set()
    named_attendees: set[str] = set()
    edges: list[tuple[str, str]] = []
    for n, p1, p2 in data:
        confirmed_attendees.add(n) if n != "N/A" else None

        named_attendees.add(p1) if p1 != "N/A" and p1 not in named_attendees else None
        named_attendees.add(p2) if p2 != "N/A" and p2 not in named_attendees else None

        edges.append((n, p1)) if p1 != "N/A" else None
        edges.append((n, p2)) if p2 != "N/A" else None

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


if __name__ == "__main__":
    main()
