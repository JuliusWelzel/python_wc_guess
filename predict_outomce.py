import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import glm
from rapidfuzz import process
from sklearn.preprocessing import MinMaxScaler

# Load data
df_org = pd.read_csv('match_data.csv')

# Combine home and away matches into one row per match
df1 = df_org[['date', 'home_team', 'away_team', 'home_score', 'away_score']].copy()
df1.columns = ['date', 'team1', 'team2', 'team1_score', 'team2_score']

df2 = df_org[['date', 'away_team', 'home_team', 'away_score', 'home_score']].copy()
df2.columns = ['date', 'team1', 'team2', 'team1_score', 'team2_score']

df = pd.concat([df1, df2])

# Convert date to datetime and extract year
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

# Create a weight column with higher weight for recent years
scaler = MinMaxScaler()
df['weight'] = np.exp(2023 - df['year'])
df['weight'] = scaler.fit_transform(df[['weight']])

# Define formulas for the models
formula_team1 = 'team1_score ~ team1 + team2'
formula_team2 = 'team2_score ~ team1 + team2'

# Create Generalized Linear Models with weights
model_team1 = glm(formula_team1, data=df, family=sm.families.Poisson()).fit(sample_weight=df['weight'])
model_team2 = glm(formula_team2, data=df, family=sm.families.Poisson()).fit(sample_weight=df['weight'])

# Get list of teams
teams = pd.concat([df['team1'], df['team2']]).unique()

# Run the prediction in a loop
while True:
    # For instance, if there's a match between Italy and France
    t1 = input("Enter Team 1 (or 'quit' to stop):")
    if t1.lower() == 'quit':
        break

    t2 = input("Enter Team 2:")

    # Check if team names are in the data
    if t1 not in teams:
        closest_match = process.extractOne(t1, teams)
        print(f"{t1} not found, did you mean {closest_match[0]}?")
        t1 = closest_match[0]

    if t2 not in teams:
        closest_match = process.extractOne(t2, teams)
        print(f"{t2} not found, did you mean {closest_match[0]}?")
        t2 = closest_match[0]

    new_match = pd.DataFrame({
        'team1': [t1],
        'team2': [t2]
    })

    # Predict scores
    predicted_team1_score = model_team1.predict(new_match)
    predicted_team2_score = model_team2.predict(new_match)

    print(f'Predicted score: {t1} {predicted_team1_score[0]:.0f} - {predicted_team2_score[0]:.0f} {t2}\n')
