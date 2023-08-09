import csv
import json
from sbrscrape import Scoreboard

class SbrOddsProvider:
    
    def __init__(self, sportsbook="fanduel"):
        sb = Scoreboard(sport="NFL")
        self.games = sb.games if hasattr(sb, 'games') else []
        self.sportsbook = sportsbook

    def get_odds(self):
        dict_res = {}
        for game in self.games:
            home_team_name = game['home_team']
            away_team_name = game['away_team']
            
            money_line_home_value = money_line_away_value = totals_value = None

            if self.sportsbook in game['home_ml']:
                money_line_home_value = game['home_ml'][self.sportsbook]
            if self.sportsbook in game['away_ml']:
                money_line_away_value = game['away_ml'][self.sportsbook]
            
            if self.sportsbook in game['total']:
                totals_value = game['total'][self.sportsbook]
            
            dict_res[home_team_name + ':' + away_team_name] =  { 
                'under_over_odds': totals_value,
                home_team_name: { 'money_line_odds': money_line_home_value }, 
                away_team_name: { 'money_line_odds': money_line_away_value }
            }
        return dict_res

    def save_as_csv(self, data, filename="odds.csv"):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Matchup', 'Under_Over_Odds', 'Home_Team', 'Home_Team_Odds', 'Away_Team', 'Away_Team_Odds']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for matchup, odds in data.items():
                home_team = list(odds.keys())[1]
                away_team = list(odds.keys())[2]
                writer.writerow({
                    'Matchup': matchup,
                    'Under_Over_Odds': odds['under_over_odds'],
                    'Home_Team': home_team,
                    'Home_Team_Odds': odds[home_team]['money_line_odds'],
                    'Away_Team': away_team,
                    'Away_Team_Odds': odds[away_team]['money_line_odds']
                })

    def save_as_json(self, data, filename="odds.json"):
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=4)

# Usage:
provider = SbrOddsProvider()
odds_data = provider.get_odds()
provider.save_as_csv(odds_data)
provider.save_as_json(odds_data)
