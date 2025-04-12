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
                + ([] if (not row[12] or "N/A" in row[12]) else [row[12]])
                + ([] if (not row[13] or "N/A" in row[13]) else [row[13]])
            )

            attendees.add(row[5])
            named_attendees.add(row[12]) if row[12] != "N/A" and row[
                12
            ] not in named_attendees else None
            named_attendees.add(row[13]) if row[13] != "N/A" and row[
                13
            ] not in named_attendees else None
            edges.append((row[5], row[12])) if row[12] != "N/A" else None
            edges.append((row[5], row[13])) if row[13] != "N/A" else None

    return attendees_and_preferences


attendees_and_preferences: dict[str, list[str]] = import_data()
