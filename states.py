import csv
import glob
import os
import re
import sys

# Define scoring systems
individual_points = [20, 17, 16, 15, 14, 13, 12, 11, 9, 7, 6, 5, 4, 3, 2, 1]
relay_points = [40, 34, 32, 30, 28, 26, 24, 22, 18, 14, 12, 10, 8, 6, 4, 2]

# Initialize team scores
team_scores = {}
age_group_scores = {
    '10&U': {},
    '11-12': {},
    '13-14': {}
}

# Separate relay scores for girls and boys
girls_relay_scores = {}
boys_relay_scores = {}

# Helper function to add points to a team
def add_points(team, points, age_group=None):
    # Extract team code without the "MD" suffix
    team = team.split('-')[0]

    if team not in team_scores:
        team_scores[team] = 0
    team_scores[team] += points

    # Add to age group scoring if specified
    if age_group:
        if team not in age_group_scores[age_group]:
            age_group_scores[age_group][team] = 0
        age_group_scores[age_group][team] += points

# Function to process an event
def process_event(event_name, teams, is_relay, age_group):
    point_system = relay_points if is_relay else individual_points

    for i, team in enumerate(teams[:16]):  # Only process up to 16 teams
        if team and team.strip():
            add_points(team, point_system[i], age_group)

            # Track relay scores separately by gender
            if is_relay:
                team_code = team.split('-')[0]
                if "Girls" in event_name:
                    if team_code not in girls_relay_scores:
                        girls_relay_scores[team_code] = 0
                    girls_relay_scores[team_code] += point_system[i]
                elif "Boys" in event_name:
                    if team_code not in boys_relay_scores:
                        boys_relay_scores[team_code] = 0
                    boys_relay_scores[team_code] += point_system[i]

# ---------------------------------------------------------------------------
# PDF extraction: parse relay events from a HY-TEK psych sheet PDF
# ---------------------------------------------------------------------------
def extract_events_from_pdf(pdf_path):
    try:
        import pdfplumber
    except ImportError:
        print("pdfplumber is required for PDF parsing. Install with: pip install pdfplumber")
        return []

    # The HY-TEK psych sheet uses a 3-column layout
    COL_BOUNDARIES = [0, 200, 395, 612]

    relay_header_re = re.compile(
        r'#(\d+)\s+(Girls|Boys)\s+(13-14|11-12|10 & Under|10&U)\s+(\d+)\s+Yard\s+(\w+)\s+Relay'
    )
    team_entry_re = re.compile(
        r'^\s*(\d+)\s+([A-Z]{2,6}-[A-Z]{2})\s+[A-Z]\s+(\d+:\d+\.\d+|\d+\.\d+)'
    )
    continuation_re = re.compile(r'#(\d+)\s+\.\.\.')

    events = {}  # keyed by event number

    pdf = pdfplumber.open(pdf_path)

    for page in pdf.pages:
        for i in range(len(COL_BOUNDARIES) - 1):
            x0 = COL_BOUNDARIES[i]
            x1 = COL_BOUNDARIES[i + 1]
            cropped = page.crop((x0, 0, x1, page.height))
            text = cropped.extract_text()
            if not text:
                continue

            lines = text.split('\n')

            for line_idx, line in enumerate(lines):
                # Check for a relay event header
                header_match = relay_header_re.search(line)
                if header_match:
                    event_num = int(header_match.group(1))
                    gender = header_match.group(2)
                    age_group = header_match.group(3).replace('10 & Under', '10&U')
                    distance = header_match.group(4)
                    stroke = header_match.group(5)
                    event_name = f"{gender} {age_group} {distance} {stroke} Relay (#{event_num})"

                    # Scan forward for "Team Relay Seed Time" then team entries
                    teams = []
                    found_header = False
                    for j in range(line_idx + 1, min(line_idx + 30, len(lines))):
                        if 'Team' in lines[j] and 'Relay' in lines[j] and 'Seed' in lines[j]:
                            found_header = True
                            continue
                        if found_header:
                            tm = team_entry_re.match(lines[j])
                            if tm:
                                teams.append(tm.group(2))
                            elif teams:
                                break

                    if event_num not in events:
                        events[event_num] = {
                            'name': event_name,
                            'teams': teams,
                            'is_relay': True,
                            'age_group': age_group
                        }

                # Check for continuation lines (#N ...)
                cont_match = continuation_re.search(line)
                if cont_match:
                    event_num = int(cont_match.group(1))
                    if event_num in events:
                        for j in range(line_idx + 1, min(line_idx + 20, len(lines))):
                            tm = team_entry_re.match(lines[j])
                            if tm:
                                events[event_num]['teams'].append(tm.group(2))
                            elif events[event_num]['teams']:
                                break

    pdf.close()

    result = [events[num] for num in sorted(events.keys())]
    print(f"Extracted {len(result)} relay events from {os.path.basename(pdf_path)}")
    return result


# ---------------------------------------------------------------------------
# CSV extraction: read events from a CSV file
# ---------------------------------------------------------------------------
def extract_events_from_csv(csv_path):
    events = []
    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            teams = [t.strip() for t in row['teams'].split(',') if t.strip()]
            is_relay = row['is_relay'].lower() in ('true', 'yes', '1')
            events.append({
                'name': row['name'],
                'teams': teams,
                'is_relay': is_relay,
                'age_group': row['age_group']
            })
    print(f"Read {len(events)} events from {os.path.basename(csv_path)}")
    return events


# ---------------------------------------------------------------------------
# Auto-detect data source: look for PDF first, then CSV
# ---------------------------------------------------------------------------
def load_events(directory='.'):
    # Look for PDF files first
    pdf_files = glob.glob(os.path.join(directory, '*.pdf'))
    if pdf_files:
        pdf_path = pdf_files[0]
        print(f"Found PDF: {os.path.basename(pdf_path)}")
        return extract_events_from_pdf(pdf_path)

    # Fall back to CSV files
    csv_files = glob.glob(os.path.join(directory, '*.csv'))
    if csv_files:
        csv_path = csv_files[0]
        print(f"Found CSV: {os.path.basename(csv_path)}")
        return extract_events_from_csv(csv_path)

    print("No PDF or CSV data files found in", directory)
    return []


# ---------------------------------------------------------------------------
# Display results
# ---------------------------------------------------------------------------
def display_results():
    # Display overall team scores
    print("\nPROJECTED OVERALL TEAM STANDINGS:")
    sorted_teams = sorted(team_scores.items(), key=lambda x: x[1], reverse=True)
    for i, (team, score) in enumerate(sorted_teams, 1):
        print(f"{i}. {team}: {score} points")

    # Display age group scores
    for age_group in age_group_scores:
        if age_group_scores[age_group]:
            print(f"\n{age_group} AGE GROUP STANDINGS:")
            sorted_age_group = sorted(age_group_scores[age_group].items(), key=lambda x: x[1], reverse=True)
            for i, (team, score) in enumerate(sorted_age_group, 1):
                print(f"{i}. {team}: {score} points")

    # Display girls relay standings
    if girls_relay_scores:
        print("\nGIRLS RELAY STANDINGS:")
        sorted_girls_relays = sorted(girls_relay_scores.items(), key=lambda x: x[1], reverse=True)
        for i, (team, score) in enumerate(sorted_girls_relays, 1):
            print(f"{i}. {team}: {score} points")

    # Display boys relay standings
    if boys_relay_scores:
        print("\nBOYS RELAY STANDINGS:")
        sorted_boys_relays = sorted(boys_relay_scores.items(), key=lambda x: x[1], reverse=True)
        for i, (team, score) in enumerate(sorted_boys_relays, 1):
            print(f"{i}. {team}: {score} points")

    # Generate a summary table for top 10 teams with columns for each age group
    if team_scores:
        print("\nTOP 10 TEAMS BREAKDOWN BY AGE GROUP:")
        print("Rank Team    Total  10&U  11-12  13-14")
        print("-----------------------------------------")

        top_10_teams = sorted(team_scores.items(), key=lambda x: x[1], reverse=True)[:10]

        for i, (team, total) in enumerate(top_10_teams, 1):
            ten_under = age_group_scores['10&U'].get(team, 0)
            eleven_twelve = age_group_scores['11-12'].get(team, 0)
            thirteen_fourteen = age_group_scores['13-14'].get(team, 0)

            print(f"{i:<4} {team:<7} {total:<6} {ten_under:<5} {eleven_twelve:<6} {thirteen_fourteen}")

    print("\nNote: This analysis is based on events extracted from the psych sheet.")
    print("The projection assumes swimmers finish according to their seedings.")
    print("Actual results may vary depending on performance on the day of the meet.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Allow passing a custom directory as argument
    directory = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))

    events = load_events(directory)

    if not events:
        print("No events to process.")
        sys.exit(1)

    for event in events:
        process_event(event['name'], event['teams'], event['is_relay'], event['age_group'])

    display_results()
