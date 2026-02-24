# Swimming States Score Projector

A Python script to project team standings for Maryland swimming state championships based on psych sheet seedings.

## Requirements

- Python 3.6+

## Usage

```bash
python states.py
```

## How It Works

The script calculates projected team scores based on the assumption that swimmers finish according to their seeded positions from the psych sheet.

### Scoring Systems

**Individual Events** (places 1-16):
```
20, 17, 16, 15, 14, 13, 12, 11, 9, 7, 6, 5, 4, 3, 2, 1
```

**Relay Events** (places 1-16):
```
40, 34, 32, 30, 28, 26, 24, 22, 18, 14, 12, 10, 8, 6, 4, 2
```

### Age Groups

- 10 & Under
- 11-12
- 13-14

## Adding Events

Events are defined in three lists based on age group:

- `events_1314` - 13-14 age group events
- `events_1112` - 11-12 age group events
- `events_10u` - 10 & Under events

Each event is a dictionary with the following structure:

```python
{
    "name": "Girls 13-14 200 Medley Relay (#1)",
    "teams": ["NBAC-MD", "ASC-MD", "EST-MD", ...],
    "is_relay": True  # or False for individual events
}
```

**Important:** Event names must include "Girls" or "Boys" for relay events to be tracked separately by gender.

## Output

The script produces the following standings:

1. **Overall Team Standings** - Total projected points for each team
2. **Age Group Standings** - Points broken down by 10&U, 11-12, and 13-14
3. **Girls Relay Standings** - Relay points for girls events only
4. **Boys Relay Standings** - Relay points for boys events only
5. **Top 10 Breakdown** - Summary table showing top 10 teams with points by age group

## Example Output

```
PROJECTED OVERALL TEAM STANDINGS:
1. NBAC: 120 points
2. ASC: 85 points
...

GIRLS RELAY STANDINGS:
1. NBAC: 40 points
2. FSC: 34 points
...

BOYS RELAY STANDINGS:
1. NBAC: 40 points
2. NAAC: 34 points
...
```

## Notes

- Projections assume swimmers finish according to their seedings
- Actual results may vary based on performance on meet day
- Team codes are automatically parsed (e.g., "NBAC-MD" becomes "NBAC")
