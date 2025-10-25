import pandas as pd

# Load the dataset
df = pd.read_csv('premier_league_cleaned.csv')
 
# 2023/24 Premier League final standings (Wins/Total Matches = Win Rate)
# Based on actual 2023/24 season results
team_standings = {
    'Manchester City': {'wins': 28, 'matches': 38, 'points': 91, 'position': 1},
    'Arsenal': {'wins': 28, 'matches': 38, 'points': 89, 'position': 2},
    'Liverpool': {'wins': 24, 'matches': 38, 'points': 82, 'position': 3},
    'Aston Villa': {'wins': 20, 'matches': 38, 'points': 68, 'position': 4},
    'Tottenham Hotspur': {'wins': 20, 'matches': 38, 'points': 66, 'position': 5},
    'Chelsea': {'wins': 18, 'matches': 38, 'points': 63, 'position': 6},
    'Newcastle United': {'wins': 18, 'matches': 38, 'points': 60, 'position': 7},
    'Manchester United': {'wins': 18, 'matches': 38, 'points': 60, 'position': 8},
    'West Ham United': {'wins': 14, 'matches': 38, 'points': 52, 'position': 9},
    'Crystal Palace': {'wins': 13, 'matches': 38, 'points': 49, 'position': 10},
    'Brighton': {'wins': 12, 'matches': 38, 'points': 48, 'position': 11},
    'Bournemouth': {'wins': 13, 'matches': 38, 'points': 48, 'position': 12},
    'Fulham': {'wins': 13, 'matches': 38, 'points': 47, 'position': 13},
    'Wolverhampton': {'wins': 13, 'matches': 38, 'points': 46, 'position': 14},
    'Everton': {'wins': 13, 'matches': 38, 'points': 40, 'position': 15},
    'Brentford': {'wins': 10, 'matches': 38, 'points': 39, 'position': 16},
    'Nottingham Forest': {'wins': 9, 'matches': 38, 'points': 32, 'position': 17},
    'Luton Town': {'wins': 6, 'matches': 38, 'points': 26, 'position': 18},
    'Burnley': {'wins': 5, 'matches': 38, 'points': 24, 'position': 19},
    'Sheffield United': {'wins': 3, 'matches': 38, 'points': 16, 'position': 20},
}

# Calculate win rate for each team
for team in team_standings:
    team_standings[team]['win_rate'] = (team_standings[team]['wins'] / team_standings[team]['matches']) * 100

# Add win rate and team position to the dataframe
df['Team_Win_Rate'] = df['Team'].map(lambda x: team_standings.get(x, {}).get('win_rate', 0))
df['Team_Position'] = df['Team'].map(lambda x: team_standings.get(x, {}).get('position', 0))
df['Team_Points'] = df['Team'].map(lambda x: team_standings.get(x, {}).get('points', 0))

# Save the updated dataset
df.to_csv('premier_league_with_win_rate.csv', index=False)

print("Win rate data added successfully!")
print(f"\nDataset now has {len(df.columns)} columns")
print("\nNew columns added:")
print("- Team_Win_Rate: Team's win percentage in 2023/24 season")
print("- Team_Position: Final league position")
print("- Team_Points: Total points earned")
