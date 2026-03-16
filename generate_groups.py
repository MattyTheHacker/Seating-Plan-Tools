import networkx as nx
from file_utils import attendees_and_preferences as attendees

def generate_attendee_group_mapping():
    G: nx.Graph = nx.Graph() 
    
    G.add_nodes_from(attendees.keys())

    for attendee, preferences in attendees.items():
        for preference in preferences:
            if preference in attendees:
                G.add_edge(attendee, preference)

    group_names = [
        "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", 
        "Theta", "Lambda", "Kappa", "Omicron", "Pi", "Mu", 
        "Foxtrot", "Covenant", "Precursor", "Ecumene", 
        "Forerunner", "Elders", "Solitude", "Abject", 
        "Spark", "Mendicant", "Offensive", "Enduring", 
        "Bias", "Exuberant"
    ]

    attendee_to_group = {}
    name_index = 0

    for component in nx.connected_components(G):
        if len(component) == 1:
            for person in component:
                attendee_to_group[person] = "Lone Ranger"
        else:
            current_group_name = group_names[name_index]
            
            for person in component:
                attendee_to_group[person] = current_group_name
                
            name_index += 1

    return attendee_to_group

if __name__ == "__main__":
    attendee_mapping = generate_attendee_group_mapping()
    
    sorted_attendees = sorted(attendee_mapping.keys(), key=str.lower)

    print(f"{'Attendee Name'} | {'Group Name'}")
    print("-" * 50)
    for attendee in sorted_attendees:
        print(f"{attendee_mapping[attendee]}")
