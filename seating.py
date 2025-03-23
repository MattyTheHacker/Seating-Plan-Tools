from pyvis.network import Network  # type: ignore[import-untyped]
import webbrowser

INPUT_FILE = "data.tsv"


def main() -> None:
    # Reads the input file.
    with open(INPUT_FILE) as file:
        data = [
            line.split("\t") for line in file.read().split("\n")[1:] if line != "\t\t"
        ]

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
        height="720px",
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
