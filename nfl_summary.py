import json
from datetime import datetime
import os
import shutil

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return json.load(infile)

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def get_fanduel_data(sites):
    for site in sites:
        if site['site_key'] == 'fanduel':
            return site['odds']
    return None

def generate_daily_summary(nfl_h2h, nfl_spreads, nfl_totals):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    daily_summary = f"Today's NFL games and betting odds as of {current_datetime}:\n\n"

    for sport, h2h, spreads, totals in [('NFL', nfl_h2h, nfl_spreads, nfl_totals)]:
        daily_summary += f"{sport} - Fanduel Sportsbook\n"
        seen_games = set()
        for i in range(len(h2h['data'])):
            game = tuple(h2h['data'][i]['teams'])
            if game in seen_games:
                continue
            seen_games.add(game)
            h2h_odds = get_fanduel_data(h2h['data'][i]['sites'])
            spreads_odds = get_fanduel_data(spreads['data'][i]['sites'])
            totals_odds = get_fanduel_data(totals['data'][i]['sites'])
            if h2h_odds and spreads_odds and totals_odds:
                away_team, home_team = h2h['data'][i]['teams']
                away_odds, home_odds = h2h_odds['h2h']
                away_spread, home_spread = spreads_odds['spreads']['points']
                total_points = totals_odds['totals']['points'][0]
                daily_summary += f"{away_team} at {home_team}\n"
                daily_summary += f"- {away_team} ({away_odds}), ({away_spread})\n"
                daily_summary += f"- {home_team} ({home_odds}), ({home_spread})\n"
                daily_summary += f"Total: {total_points}\n\n"
    
    return daily_summary

if __name__ == "__main__":
    # Get the current date
    current_date = datetime.now().strftime('%Y_%m_%d')

    # Move old summary to the old directory
    if os.path.exists(f'data/nfl_scratchpad_{current_date}.txt'):
        if not os.path.exists('data/old'):
            os.makedirs('data/old')
        shutil.move(f'data/nfl_scratchpad_{current_date}.txt', f'data/old/nfl_scratchpad_{current_date}.txt')

    nfl_h2h = open_file(f'data/nfl_fanduel_h2h_data_{current_date}.json')
    nfl_spreads = open_file(f'data/nfl_fanduel_spreads_data_{current_date}.json')
    nfl_totals = open_file(f'data/nfl_fanduel_totals_data_{current_date}.json')

    daily_summary = generate_daily_summary(nfl_h2h, nfl_spreads, nfl_totals)
    save_file(f'data/nfl_scratchpad_{current_date}.txt', daily_summary)