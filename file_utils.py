import csv

attendees: set[str] = set()
named_attendees: set[str] = set()
edges: list[tuple[str, str]] = []


def import_data() -> dict[str, list[str]]:
    attendees_and_preferences: dict[str, list[str]] = {}
    with open("data/attendees.csv") as attendees_csv:
        csv_reader = csv.reader(attendees_csv, delimiter=",")
        next(csv_reader, None)
        for row in csv_reader:
            attendees_and_preferences[row[5]] = (
                []
                + ([] if (not row[14] or "N/A" in row[14]) else [row[14]])
                + ([] if (not row[15] or "N/A" in row[15]) else [row[15]])
            )

            attendees.add(row[5])
            named_attendees.add(row[14]) if row[14] != "N/A" and row[
                14
            ] not in named_attendees else None
            named_attendees.add(row[15]) if row[15] != "N/A" and row[
                15
            ] not in named_attendees else None
            edges.append((row[5], row[14])) if row[14] != "N/A" else None
            edges.append((row[5], row[15])) if row[15] != "N/A" else None

    print(attendees_and_preferences)

    return attendees_and_preferences


attendees_and_preferences: dict[str, list[str]] = import_data()
