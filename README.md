# Women's World Cup Prediction

This script uses statistical models to predict the scores of Women's World Cup matches based on historical data. It utilizes the `pandas`, `statsmodels`, `rapidfuzz`, and `scikit-learn` libraries to load and analyze the data.
## Setup

Make sure you have [python](https://www.python.org/) >= 3.9 installed. Then run

    python/python3 setup.py install

to install the necessary packages.

## Usage

1. Make sure you have the Women's World Cup data file (`match_data.csv`) in the same directory as the script.
2. Run the script:
   ```shell
   python predict_outcome.py
   ```
3. When prompted, enter the names of the two teams playing the match.
4. The script will predict the scores for the match and display the result.
5. If you wish to predict another match, you will be given the opportunity to enter two new teams. If you wish to stop the script, type 'quit' when prompted to enter Team 1.

## How It Works

The script uses statistical models known as [Generalized Linear Models (GLMs)](https://en.wikipedia.org/wiki/Generalized_linear_model) to predict the scores of Women's World Cup matches. GLMs are a flexible class of models that can handle various types of response variables and model the relationship between predictors and the response.

For this script, two GLMs are created using the statsmodels library:

Model 1: `team1_score ~ team1 + team2`

This model predicts the score of Team 1 (`team1_score`) based on the names of Team 1 (`team1`) and Team 2 (`team2`).

Model 2: `team2_score ~ team1 + team2`

This model predicts the score of Team 2 (`team2_score`) based on the names of Team 1 (`team1`) and Team 2 (`team2`).
Both models are fitted using the Poisson family, which is commonly used for count data. The Poisson distribution is suitable for modeling the number of goals scored by a team in a match.

To predict the outcome of a match, the script prompts the user to enter the names of the two teams playing. It then searches the historical data for matches involving the entered team names. If an exact match is not found, it uses the rapidfuzz library to find the closest matching team name.

Once the team names are validated, the script creates a new DataFrame for the match and uses the trained GLMs to predict the scores for Team 1 and Team 2.

Finally, the script displays the predicted scores for the match.

Feel free to update any details or add more information to the README file based on your specific project requirements.

