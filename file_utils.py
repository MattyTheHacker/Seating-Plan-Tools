import csv

food_attendees: set[str] = set()
non_food_attendees: set[str] = set()
named_attendees: set[str] = set()
edges: list[tuple[str, str]] = []
emails: dict[str, str] = {}  # Added: Dictionary to store emails

def import_data() -> dict[str, list[str]]:
    attendees_and_preferences: dict[str, list[str]] = {}
    with open("data/attendees.csv") as attendees_csv:
        csv_reader = csv.DictReader(attendees_csv, delimiter=",")
        for row in csv_reader:
            if not row["Name"]:
                continue

            emails[row["Name"]] = row["Contact Email"]

            attendees_and_preferences[row["Name"]] = (
                []
                + ([] if (not row["Seat Pref 1"] or "N/A" in row["Seat Pref 1"]) else [row["Seat Pref 1"]])
                + ([] if (not row["Seat Pref 2"] or "N/A" in row["Seat Pref 2"]) else [row["Seat Pref 2"]])
            )

            (food_attendees if "3 course" in row["Ticket Type"] else non_food_attendees).add(row["Name"])

            named_attendees.add(row["Seat Pref 1"]) if row["Seat Pref 1"] != "N/A" and row["Seat Pref 1"] not in named_attendees else None
            named_attendees.add(row["Seat Pref 2"]) if row["Seat Pref 2"] != "N/A" and row["Seat Pref 2"] not in named_attendees else None
            edges.append((row["Name"], row["Seat Pref 1"])) if row["Seat Pref 1"] != "N/A" else None
            edges.append((row["Name"], row["Seat Pref 2"])) if row["Seat Pref 2"] != "N/A" else None

    return attendees_and_preferences

attendees_and_preferences: dict[str, list[str]] = import_data()

# Added: Calculate and print the unpurchased preference emails
unpurchased_preferences = named_attendees - attendees_and_preferences.keys()
target_emails = {emails[purchaser] for purchaser, pref in edges if pref in unpurchased_preferences}
print("Emails of attendees whose preferences haven't purchased:", list(target_emails))
