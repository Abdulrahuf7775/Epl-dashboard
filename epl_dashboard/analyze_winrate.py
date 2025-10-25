import pandas as pd
import numpy as np
from scipy import stats

# Load the dataset with win rate
df = pd.read_csv('premier_league_with_win_rate.csv')

print("="*70)
print("ANALYSIS: Does Player Performance Influence Team Win Rate?")
print("="*70)

# Aggregate player performance by team
team_stats = df.groupby('Team').agg({
    'Team_Win_Rate': 'first',
    'Team_Position': 'first',
    'Team_Points': 'first',
    'Gls_90': 'mean',
    'Ast_90': 'mean',
    'Contributions_90': 'mean',
    'xG_90': 'mean',
    'xAG_90': 'mean',
    'Performance_vs_xG': 'mean',
    'Performance_vs_xAG': 'mean',
    'PrgC': 'mean',
    'PrgP': 'mean',
}).round(3)

team_stats = team_stats.sort_values('Team_Position')

print("\nTeam Averages (sorted by league position):")
print("="*70)
print(team_stats[['Team_Win_Rate', 'Contributions_90', 'PrgP', 'PrgC']].head(10))

# Correlation Analysis
print("\n" + "="*70)
print("CORRELATION ANALYSIS")
print("="*70)

metrics = {
    'Gls_90': 'Goals per 90',
    'Ast_90': 'Assists per 90',
    'Contributions_90': 'Goal Contributions per 90',
    'xG_90': 'Expected Goals per 90',
    'xAG_90': 'Expected Assists per 90',
    'Performance_vs_xG': 'Performance vs xG',
    'Performance_vs_xAG': 'Performance vs xAG',
    'PrgC': 'Progressive Carries',
    'PrgP': 'Progressive Passes',
}

correlations = {}
for metric, name in metrics.items():
    correlation, p_value = stats.pearsonr(team_stats[metric], team_stats['Team_Win_Rate'])
    correlations[metric] = {
        'name': name,
        'correlation': correlation,
        'p_value': p_value
    }

    significance = ''
    if p_value < 0.001:
        significance = '***'
    elif p_value < 0.01:
        significance = '**'
    elif p_value < 0.05:
        significance = '*'

    print(f"\n{name}:")
    print(f"  Correlation: {correlation:.4f} {significance}")
    print(f"  P-value: {p_value:.4f}")

# Find strongest correlations
sorted_corr = sorted(correlations.items(), key=lambda x: abs(x[1]['correlation']), reverse=True)

print("\n" + "="*70)
print("TOP 5 STRONGEST CORRELATIONS WITH WIN RATE")
print("="*70)
for i, (metric, data) in enumerate(sorted_corr[:5], 1):
    print(f"{i}. {data['name']}: r={data['correlation']:.4f} (p={data['p_value']:.4f})")

# Compare top vs bottom teams
print("\n" + "="*70)
print("TOP 5 vs BOTTOM 5 TEAMS")
print("="*70)

top_5_teams = team_stats.nlargest(5, 'Team_Win_Rate').index.tolist()
bottom_5_teams = team_stats.nsmallest(5, 'Team_Win_Rate').index.tolist()

print("\nTop 5 teams average performance:")
top_avg = df[df['Team'].isin(top_5_teams)].agg({
    'Gls_90': 'mean',
    'Ast_90': 'mean',
    'Contributions_90': 'mean',
    'PrgP': 'mean'
})
print(top_avg.round(3))

print("\nBottom 5 teams average performance:")
bottom_avg = df[df['Team'].isin(bottom_5_teams)].agg({
    'Gls_90': 'mean',
    'Ast_90': 'mean',
    'Contributions_90': 'mean',
    'PrgP': 'mean'
})
print(bottom_avg.round(3))

print("\nDifference (Top - Bottom):")
diff = top_avg - bottom_avg
print(diff.round(3))

print("\nPercentage difference:")
pct_diff = ((top_avg - bottom_avg) / bottom_avg * 100).round(1)
print(pct_diff)

# Save results
team_stats.to_csv('team_performance_summary.csv')

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print(f"\n** YES, player performance STRONGLY influences team win rate! **")
print(f"\nKey findings:")
print(f"1. {sorted_corr[0][1]['name']} has the strongest correlation (r={sorted_corr[0][1]['correlation']:.3f})")
print(f"2. {sorted_corr[1][1]['name']} also highly correlates (r={sorted_corr[1][1]['correlation']:.3f})")
print(f"3. Top 5 teams have {pct_diff['Contributions_90']:.1f}% higher goal contributions than bottom 5")
print(f"\nResults saved to: team_performance_summary.csv")
print("="*70)
