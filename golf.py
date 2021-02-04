import pandas as pd
from bs4 import BeautifulSoup
import requests

# Variables to be set by the user
url = 'https://www.espn.com/golf/leaderboard' # Website used for scores and par
filename = 'players.csv'                      # csv file in name,player,player... format
rounds = 4                                    # Number of rounds to use in when calculating the score

# Parse espn for par
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, 'lxml')
par = int(soup.find(class_='Leaderboard__Course__Location__Detail n8 clr-gray-04').get_text()[3:5])

# Scrape espn leaderboard
table = pd.read_html(url)
results = table[0]

# Create a dictionary of lists of columns
results_dict = results.to_dict(orient='list')

# Clean the (a) from player names if needed
for i in range(len(results_dict['R1'])):
    name = results_dict['PLAYER'][i]
    if ' (a)' in name:
        results_dict['PLAYER'][i] = name[:4]

# Read in player info
player_golfers = {}
with open(filename) as f:
    for line in f:
        line = line.strip('\n')
        line_list = line.split(',')
        player_golfers[line_list[0]] = line_list[1:]

# Calculate each players score
players = []
player_scores = []
for player, golfers in player_golfers.items():
    player_score = 0
    for golfer in golfers:
        # Find index of the golfer in each list
        i = results_dict['PLAYER'].index(golfer)
        # Put the round scores into a usable format
        r1 = int(results_dict['R1'][i]) if results_dict['R1'][i] != '--' else 0
        r2 = int(results_dict['R2'][i]) if results_dict['R2'][i] != '--' else 0
        r3 = int(results_dict['R3'][i]) if results_dict['R3'][i] != '--' else 0
        r4 = int(results_dict['R4'][i]) if results_dict['R4'][i] != '--' else 0
        scores = [r1, r2, r3, r4]
        for j in range(rounds):
            # If player has made the cut
            if scores[j] != 0:
                # Add the par score
                player_score += scores[j] - par
            # If player missed the cut
            else:
                # Add the worst par score
                player_score += max(scores) - par
    players.append(player)
    player_scores.append(player_score)

# Sort the players by score in reverse
sorted_players = sorted(zip(players, player_scores), reverse=True)

# Put the sorted list into pandas for output and showing
player_df = pd.DataFrame(sorted_players, columns=['Name', 'Score'], index=range(1,len(players)+1))
player_df.to_csv('scores.csv')
print(player_df)
