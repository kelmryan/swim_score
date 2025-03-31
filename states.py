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
        if team:
            add_points(team, point_system[i], age_group)

# Define events - samples from each age group

# 13-14 AGE GROUP EVENTS
events_1314 = [
    # Relays
    {
        "name": "Girls 13-14 200 Medley Relay (#1)",
        "teams": ["NBAC-MD", "ASC-MD", "EST-MD", "FSC-MD", "LBA-MD", "NAAC-MD", "SPRC-MD", "ACA-MD", 
                 "BAY-MD", "OPST-MD", "SMDA-MD", "CAA-MD", "RAC-MD", "MAC-MD"],
        "is_relay": True
    },
    {
        "name": "Boys 13-14 200 Medley Relay (#2)",
        "teams": ["NBAC-MD", "NAAC-MD", "CAA-MD", "EST-MD", "CAC-MD", "FSC-MD", "MAC-MD", 
                 "RAC-MD", "BAY-MD", "LBA-MD", "SMDA-MD"],
        "is_relay": True
    },
    # Add more events as needed...
]

# 11-12 AGE GROUP EVENTS
events_1112 = [
    # Relays
    {
        "name": "Girls 11-12 200 Medley Relay (#13)",
        "teams": ["NBAC-MD", "FSC-MD", "MAC-MD", "ASC-MD", "CAA-MD", "BAY-MD", "EST-MD", "GBSA-MD"],
        "is_relay": True
    },
    # Add more events as needed...
]

# 10 & UNDER AGE GROUP EVENTS
events_10u = [
    # Relays
    {
        "name": "Girls 10&U 200 Medley Relay (#11)",
        "teams": ["NBAC-MD", "ASC-MD", "EST-MD", "BAY-MD", "MAC-MD", "SPRC-MD", "LBA-MD", 
                 "FSC-MD", "CAC-MD", "CAA-MD", "NAAC-MD"],
        "is_relay": True
    },
    # Add more events as needed...
]

# Process all events
print("Processing 13-14 events...")
for event in events_1314:
    process_event(event["name"], event["teams"], event["is_relay"], '13-14')

print("Processing 11-12 events...")
for event in events_1112:
    process_event(event["name"], event["teams"], event["is_relay"], '11-12')

print("Processing 10&U events...")
for event in events_10u:
    process_event(event["name"], event["teams"], event["is_relay"], '10&U')

# Display overall team scores
print("\nPROJECTED OVERALL TEAM STANDINGS:")
sorted_teams = sorted(team_scores.items(), key=lambda x: x[1], reverse=True)
for i, (team, score) in enumerate(sorted_teams, 1):
    print(f"{i}. {team}: {score} points")

# Display age group scores
for age_group in age_group_scores:
    print(f"\n{age_group} AGE GROUP STANDINGS:")
    sorted_age_group = sorted(age_group_scores[age_group].items(), key=lambda x: x[1], reverse=True)
    for i, (team, score) in enumerate(sorted_age_group, 1):
        print(f"{i}. {team}: {score} points")

# Generate a summary table for top 10 teams with columns for each age group
print("\nTOP 10 TEAMS BREAKDOWN BY AGE GROUP:")
print("Rank Team    Total  10&U  11-12  13-14")
print("-----------------------------------------")

top_10_teams = sorted(team_scores.items(), key=lambda x: x[1], reverse=True)[:10]

for i, (team, total) in enumerate(top_10_teams, 1):
    ten_under = age_group_scores['10&U'].get(team, 0)
    eleven_twelve = age_group_scores['11-12'].get(team, 0)
    thirteen_fourteen = age_group_scores['13-14'].get(team, 0)
    
    print(f"{i:<4} {team:<7} {total:<6} {ten_under:<5} {eleven_twelve:<6} {thirteen_fourteen}")

print("\nNote: This analysis is based on a sampling of events from the psyche sheet.")
print("The projection assumes swimmers finish according to their seedings.")
print("Actual results may vary depending on performance on the day of the meet.")