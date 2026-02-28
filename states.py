import csv
import glob
import os
import re
import sys
from collections import defaultdict

# Define scoring systems
individual_points = [20, 17, 16, 15, 14, 13, 12, 11, 9, 7, 6, 5, 4, 3, 2, 1]
relay_points = [40, 34, 32, 30, 28, 26, 24, 22, 18, 14, 12, 10, 8, 6, 4, 2]

# Score accumulators
overall = defaultdict(int)
by_gender = {'Girls': defaultdict(int), 'Boys': defaultdict(int)}
by_age = {'10&U': defaultdict(int), '11-12': defaultdict(int), '13-14': defaultdict(int)}
by_gender_age = {
    'Girls': {'10&U': defaultdict(int), '11-12': defaultdict(int), '13-14': defaultdict(int)},
    'Boys': {'10&U': defaultdict(int), '11-12': defaultdict(int), '13-14': defaultdict(int)},
}


# ---------------------------------------------------------------------------
# PDF extraction: parse individual AND relay events from a HY-TEK psych sheet
# ---------------------------------------------------------------------------
def extract_events_from_pdf(pdf_path):
    try:
        import pdfplumber
    except ImportError:
        print("pdfplumber is required for PDF parsing. Install with: pip install pdfplumber")
        return []

    # The HY-TEK psych sheet uses a 3-column layout
    COL_BOUNDARIES = [0, 200, 395, 612]

    # Event header: #N Gender AgeGroup Distance Yard Stroke [Relay]
    event_header_re = re.compile(
        r'^#(\d+)\s+(Girls|Boys)\s+(13-14|11-12|10 & Under|10&U)\s+'
        r'(\d+)\s+Yard\s+(.+?)$'
    )
    # Continuation header: #N ... (description)
    continuation_re = re.compile(r'^#(\d+)\s+\.\.\.\s*\((.+?)\)')

    # Relay entry: rank TEAM-MD letter time
    relay_entry_re = re.compile(
        r'^\s*(\d+)\s+([A-Z]{2,6})-[A-Z]{2}\s+[A-Z]\s+(\d+:?\d*\.\d+)'
    )
    # Individual entry: rank Name ... age+TEAM-MD time
    individual_entry_re = re.compile(
        r'^\s*(\d+)\s+[\w\',\-]+.*?\s+(\d{1,2})([A-Z]{2,6})-[A-Z]{2}\s+(\d+:?\d*\.\d+)'
    )

    # Extract all text column-by-column to avoid interleaving
    lines_all = []
    pdf = pdfplumber.open(pdf_path)
    for page in pdf.pages:
        for i in range(len(COL_BOUNDARIES) - 1):
            x0 = COL_BOUNDARIES[i]
            x1 = COL_BOUNDARIES[i + 1]
            cropped = page.crop((x0, 0, x1, page.height))
            text = cropped.extract_text()
            if text:
                for line in text.split('\n'):
                    lines_all.append(line)
    pdf.close()

    events = {}  # keyed by event number
    current_event = None

    for line in lines_all:
        if not line.strip():
            continue
        if 'HY-TEK' in line or 'Psych Sheet' in line or 'Sanction' in line:
            continue
        if 'MEET MANAGER' in line:
            continue

        # Check for event header
        hm = event_header_re.match(line)
        if hm:
            event_num = int(hm.group(1))
            gender = hm.group(2)
            age_group = hm.group(3).replace('10 & Under', '10&U')
            distance = hm.group(4)
            stroke = hm.group(5).strip()
            is_relay = 'Relay' in stroke
            event_name = f"#{event_num} {gender} {age_group} {distance} Yard {stroke}"

            if event_num not in events:
                events[event_num] = {
                    'name': event_name,
                    'gender': gender,
                    'age_group': age_group,
                    'is_relay': is_relay,
                    'entries': []
                }
            current_event = event_num
            continue

        # Check for continuation
        cm = continuation_re.match(line)
        if cm:
            event_num = int(cm.group(1))
            if event_num in events:
                current_event = event_num
            continue

        # Skip sub-headers
        if 'Team' in line and 'Relay' in line and 'Seed' in line:
            continue
        if 'Name' in line and 'Age' in line and 'Team' in line and 'Seed' in line:
            continue

        if current_event is None:
            continue

        evt = events.get(current_event)
        if evt is None:
            continue

        if evt['is_relay']:
            rm = relay_entry_re.match(line)
            if rm:
                rank = int(rm.group(1))
                team = rm.group(2)
                evt['entries'].append((rank, team))
        else:
            im = individual_entry_re.match(line)
            if im:
                rank = int(im.group(1))
                team = im.group(3)
                evt['entries'].append((rank, team))

    print(f"Extracted {len(events)} events from {os.path.basename(pdf_path)}")
    relay_count = sum(1 for e in events.values() if e['is_relay'])
    print(f"  Individual events: {len(events) - relay_count}")
    print(f"  Relay events: {relay_count}")

    # Convert to list sorted by event number
    result = []
    for num in sorted(events.keys()):
        evt = events[num]
        # Sort entries by rank and deduplicate
        entries = sorted(evt['entries'], key=lambda x: x[0])
        seen_ranks = set()
        unique_entries = []
        for rank, team in entries:
            if rank not in seen_ranks:
                seen_ranks.add(rank)
                unique_entries.append(team)
        result.append({
            'name': evt['name'],
            'gender': evt['gender'],
            'age_group': evt['age_group'],
            'is_relay': evt['is_relay'],
            'teams': unique_entries[:16],
        })

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
            gender = None
            if 'Girls' in row['name']:
                gender = 'Girls'
            elif 'Boys' in row['name']:
                gender = 'Boys'
            events.append({
                'name': row['name'],
                'teams': teams,
                'is_relay': is_relay,
                'age_group': row['age_group'],
                'gender': gender,
            })
    print(f"Read {len(events)} events from {os.path.basename(csv_path)}")
    return events


# ---------------------------------------------------------------------------
# Auto-detect data source: look for PDF first, then CSV
# ---------------------------------------------------------------------------
def load_events(directory='.'):
    pdf_files = glob.glob(os.path.join(directory, '*.pdf'))
    if pdf_files:
        pdf_path = pdf_files[0]
        print(f"Found PDF: {os.path.basename(pdf_path)}")
        return extract_events_from_pdf(pdf_path)

    csv_files = glob.glob(os.path.join(directory, '*.csv'))
    if csv_files:
        csv_path = csv_files[0]
        print(f"Found CSV: {os.path.basename(csv_path)}")
        return extract_events_from_csv(csv_path)

    print("No PDF or CSV data files found in", directory)
    return []


# ---------------------------------------------------------------------------
# Score events
# ---------------------------------------------------------------------------
def score_events(events):
    for evt in events:
        pts = relay_points if evt['is_relay'] else individual_points
        gender = evt.get('gender')
        if not gender:
            if 'Girls' in evt['name']:
                gender = 'Girls'
            elif 'Boys' in evt['name']:
                gender = 'Boys'
        age_group = evt['age_group']

        for i, team in enumerate(evt['teams'][:16]):
            if not team or not team.strip():
                continue
            team = team.split('-')[0]  # strip -MD suffix if present
            p = pts[i]
            overall[team] += p
            if gender:
                by_gender[gender][team] += p
                by_gender_age[gender][age_group][team] += p
            by_age[age_group][team] += p


# ---------------------------------------------------------------------------
# Display results
# ---------------------------------------------------------------------------
def display_results(events):
    # Print per-event scoring
    for evt in events:
        pts = relay_points if evt['is_relay'] else individual_points
        tag = "RELAY" if evt['is_relay'] else "INDIV"
        print(f"\n{evt['name']} [{tag}]")
        for i, team in enumerate(evt['teams'][:16]):
            if not team or not team.strip():
                continue
            team_code = team.split('-')[0]
            print(f"  {i+1:>2}. {team_code:<6} -> {pts[i]} pts")

    # Overall standings
    print("\n" + "=" * 60)
    print("PROJECTED OVERALL TEAM STANDINGS (COMBINED)")
    print("=" * 60)
    for i, (team, score) in enumerate(sorted(overall.items(), key=lambda x: x[1], reverse=True), 1):
        print(f"  {i:>2}. {team:<8} {score:>5} pts")

    # Girls overall
    print("\n" + "=" * 60)
    print("GIRLS OVERALL STANDINGS")
    print("=" * 60)
    for i, (team, score) in enumerate(sorted(by_gender['Girls'].items(), key=lambda x: x[1], reverse=True), 1):
        print(f"  {i:>2}. {team:<8} {score:>5} pts")

    # Boys overall
    print("\n" + "=" * 60)
    print("BOYS OVERALL STANDINGS")
    print("=" * 60)
    for i, (team, score) in enumerate(sorted(by_gender['Boys'].items(), key=lambda x: x[1], reverse=True), 1):
        print(f"  {i:>2}. {team:<8} {score:>5} pts")

    # Gender + Age group breakdowns
    for gender in ['Girls', 'Boys']:
        for ag in ['10&U', '11-12', '13-14']:
            data = by_gender_age[gender][ag]
            if data:
                print(f"\n{gender.upper()} {ag} STANDINGS:")
                for i, (team, score) in enumerate(sorted(data.items(), key=lambda x: x[1], reverse=True), 1):
                    print(f"  {i:>2}. {team:<8} {score:>5} pts")

    # Top 10 breakdown tables
    for label, scores, age_src in [
        ("GIRLS", by_gender['Girls'], by_gender_age['Girls']),
        ("BOYS", by_gender['Boys'], by_gender_age['Boys']),
        ("COMBINED", overall, None),
    ]:
        print(f"\nTOP 10 {label} BREAKDOWN BY AGE GROUP:")
        print(f"{'Rank':<5} {'Team':<8} {'Total':>6} {'10&U':>6} {'11-12':>6} {'13-14':>6}")
        print("-" * 45)
        top10 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
        for i, (team, total) in enumerate(top10, 1):
            if age_src is None:
                ten = by_age['10&U'].get(team, 0)
                elev = by_age['11-12'].get(team, 0)
                thir = by_age['13-14'].get(team, 0)
            else:
                ten = age_src['10&U'].get(team, 0)
                elev = age_src['11-12'].get(team, 0)
                thir = age_src['13-14'].get(team, 0)
            print(f"  {i:<3} {team:<8} {total:>6} {ten:>6} {elev:>6} {thir:>6}")

    print("\n" + "=" * 60)
    print("NOTE: Projected based on psych sheet seed order.")
    print("Assumes swimmers finish according to their seedings.")
    print("Actual results will vary based on meet-day performance.")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))

    events = load_events(directory)

    if not events:
        print("No events to process.")
        sys.exit(1)

    score_events(events)
    display_results(events)
