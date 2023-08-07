import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def extract_date(date_string):
    # Use regular expression to extract the date in the format 'yyyy-mm-dd' from the given string format
    date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', date_string)
    if date_match:
        year, month, day = date_match.groups()
        return f"{year}-{month}-{day}"
    else:
        return None

def scrape_table_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.content
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the containers that hold the table data (each match represented by a separate container)
    table_containers = soup.find_all('div', class_='footballbox')

    # Initialize an empty list to store the formatted data
    formatted_data = []

    # Iterate through each container (match) to extract and format the data
    for container in table_containers:
        # Extract relevant data from the container
        date_string = container.find('div', class_='fdate').get_text(strip=True).split(',')[0]
        date = extract_date(date_string)
        home_team = container.find('th', class_='fhome').get_text(strip=True)
        away_team = container.find('th', class_='faway').get_text(strip=True)
        score = container.find('th', class_='fscore').get_text(strip=True).rstrip('(a.e.t.)')

        # Skip matches with the string 'Match' in the score
        if 'Match' in score:
            continue

        # Extracting scores in the format "1-0" instead of "1.0"
        if '–' in score:
            home_score, away_score = map(int, score.split('–'))
        else:
            home_score, away_score = None, None

        # Extract additional data like tournament, city, country, and neutral status (if available)
        tournament = 'World Cup'
        location_div = container.find('div', itemprop='location')
        city = location_div.find('a').get_text(strip=True)
        country = location_div.find('a', title=lambda value: value and "city" not in value).get_text(strip=True)
        neutral = 'FALSE'

        # Append the formatted data to the formatted_data list as a tuple
        formatted_data.append((date, home_team, away_team, home_score, away_score, tournament, city, country, neutral))

    return formatted_data

def save_to_csv(data, output_file):
    # Convert the data to a DataFrame
    data_df = pd.DataFrame(data, columns=['date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament', 'city', 'country', 'neutral'])

    # Save the data to a CSV file named 'ongoing_tournament_data.csv'
    data_df.to_csv(output_file, index=False)

# URL to scrape table data
url = 'https://en.wikipedia.org/wiki/2023_FIFA_Women%27s_World_Cup'  # Replace this with the URL of the webpage containing the data
scraped_data = scrape_table_data(url)

if scraped_data is not None:
    ongoing_tournament_csv_file = 'ongoing_tournament_data.csv'
    save_to_csv(scraped_data, ongoing_tournament_csv_file)
