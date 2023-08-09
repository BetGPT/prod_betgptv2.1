import requests
import json
import os
import shutil
from datetime import datetime

# Your API key
api_key = 'c4e6eeb7833693cf5fce826376ea1a79'

# NFL markets
nfl_markets = ['h2h', 'spreads', 'totals', 'outrights']

# Bookmakers
bookmakers = ['fanduel', 'draftkings']

# Create the data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Create the old data directory if it doesn't exist
if not os.path.exists('data/old'):
    os.makedirs('data/old')

# Move old data to the old directory
for filename in os.listdir('data'):
    if filename.endswith('.json'):
        shutil.move(f'data/{filename}', f'data/old/{filename}')

# Get the current date
current_date = datetime.now().strftime('%Y_%m_%d')

# Loop through the bookmakers
for bookmaker in bookmakers:
    # Loop through the markets
    for market in nfl_markets:
        # The endpoint URL
        url = f'https://api.the-odds-api.com/v3/odds/?apiKey={api_key}&sport=americanfootball_nfl&region=us&bookmaker={bookmaker}&mkt={market}&oddsFormat=american'

        # Send the GET request
        response = requests.get(url)

        # Parse the JSON data from the response
        data = response.json()

        # Save the data to a file in the 'data' directory with the current date in the filename
        with open(f'data/nfl_{bookmaker}_{market}_data_{current_date}.json', 'w') as f:
            json.dump(data, f, indent=4)