import numpy as np
import pandas as pd
from scipy.stats import pearsonr, chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns

import codecademylib3
np.set_printoptions(suppress=True, precision = 2)

nba = pd.read_csv('./nba_games.csv')

# Defining the two years to measure from
base_year = 2010
target_year = 2014

# Subset Data to 2010 Season, 2014 Season
nba_base_yr = nba[nba.year_id == base_year]
nba_target_yr = nba[nba.year_id == target_year]

print(nba_base_yr.head())
print(nba_target_yr.head())


# 1, 2 & 3. Association between quantitave and categorical variable 
# (team and year)
def compare_team_scores(nba_data, year, team1, team2, color1="dodgerblue", color2="orange", opacity=0.8):
    # Filter data for the specified year
    nba_year = nba_data[nba_data.year_id == year]
    
    # Extract points for each team
    team1_pts = nba_year.pts[nba_year.fran_id == team1]
    team2_pts = nba_year.pts[nba_year.fran_id == team2]
    
    # Calculate the difference in means
    team1_mean_score = np.mean(team1_pts)
    team2_mean_score = np.mean(team2_pts)
    diff_means = team1_mean_score - team2_mean_score
    
    print(f"\nDifference in means for {year}: {diff_means}")
    
    # Visualize the difference with histograms

    # Create a new figure for each call
    plt.figure()

    plt.hist(team1_pts, alpha=opacity, normed=True, label=team1, color=color1)
    plt.hist(team2_pts, alpha=opacity, normed=True, label=team2, color=color2)
    plt.legend()
    plt.title(f"{year} Season")
    plt.show()


compare_team_scores(nba, base_year, 'Knicks', 'Nets')

# 4. Compare two teams in year 2014
compare_team_scores(nba, target_year, 'Knicks', 'Nets', color1='magenta', color2='green', opacity=0.6)

# 5. Boxplot 2010
def plot_team_boxplot(nba_data, year):
    # Clear the current figure
    plt.clf()
    
    nba_year = nba_data[nba_data.year_id == year]
    sns.boxplot(data=nba_year, x='fran_id', y='pts')
    plt.title(f"Points per team in {year} Season")
    plt.show()


plot_team_boxplot(nba, base_year)


# 6. Contingency table showing the relationship between winnings when teams play @home or away
location_result_freq = pd.crosstab(nba_base_yr.game_result, nba_base_yr.game_location)
print(location_result_freq)

# 7. Contingency proportion
location_result_proportions = round(location_result_freq/len(nba_base_yr), 2)
print(location_result_proportions)

# 8. Expected Contingency table
chi2, pval, dof, expected = chi2_contingency(location_result_freq)
print(expected)
print(chi2)    # Not much of a difference. No association


# 9. Exploring the accuracy of forecast
point_diff_forecast_cov = np.cov(nba_base_yr.forecast, nba_base_yr.point_diff)

print(f"\nForecast Covariance matrix =\n{point_diff_forecast_cov}\n")
print(f"Covariance = {round(point_diff_forecast_cov[0][1], 2)}\n")

# 10. Correlation between forecast and point_diff
point_diff_forecast_corr, pvalue = pearsonr(nba_base_yr.forecast, nba_base_yr.point_diff)
print(f"Correlation = {round(point_diff_forecast_corr, 2)}")

# 11. Scatter plot of correlation between forecast and point_diff
plt.clf() 
plt.scatter('forecast', 'point_diff', data=nba_base_yr)
plt.xlabel('Forecasted Win Probability')
plt.ylabel('Point Differential')
plt.title(f"Correlation between Forecast and Point_differential = {round(point_diff_forecast_corr, 2)}")
plt.show()

