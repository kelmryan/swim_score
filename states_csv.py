import csv
import os

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
    # Extract team code without the "MD" suffix if present
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
        if team and team.strip():  # Make sure the team name isn't empty
            add_points(team, point_system[i], age_group)

# Function to read events from CSV file
def read_events_from_csv(filename):
    events = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Parse the teams field into a list
                teams = [team.strip() for team in row['teams'].split(',') if team.strip()]
                
                # Convert is_relay string to boolean
                is_relay = row['is_relay'].lower() in ('true', 'yes', '1')
                
                events.append({
                    'name': row['name'],
                    'teams': teams,
                    'is_relay': is_relay,
                    'age_group': row['age_group']
                })
        return events
    except Exception as e:
        print(f"Error reading CSV file {filename}: {e}")
        return []

# Process all events from CSV files
def process_all_csv_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            print(f"Processing events from {filename}...")
            events = read_events_from_csv(file_path)
            for event in events:
                process_event(event['name'], event['teams'], event['is_relay'], event['age_group'])

# Main execution
if __name__ == "__main__":
    # Directory where CSV files are stored
    csv_directory = "event_files"
    
    # Check if directory exists
    if not os.path.exists(csv_directory):
        print(f"Creating directory {csv_directory} for event files...")
        os.makedirs(csv_directory)
        print(f"Please place your event CSV files in the {csv_directory} directory.")
    else:
        # Process all CSV files in the directory
        process_all_csv_files(csv_directory)
        
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
        
        print("\nNote: This analysis is based on events from the CSV files.")
        print("The projection assumes swimmers finish according to their seedings.")
        print("Actual results may vary depending on performance on the day of the meet.")