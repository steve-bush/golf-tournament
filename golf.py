import pandas as pd

rounds = 4
par = 72
filename = 'players.csv'

# Scrape espn
table = pd.read_html('https://www.espn.com/golf/leaderboard')
results = table[0]
# Drop uneeded data
results = results.drop(['POS', 'TO PAR', 'TOT', 'EARNINGS', 'FEDEX PTS'], axis=1)
# Create a dictionary of lists of columns
results_dict = results.to_dict(orient='list')

# Create a dictionary of golfer scores
golfer_scores = {}
for i in range(len(results_dict['R1'])):
    name = results_dict['PLAYER'][i]
    if ' (a)' in name:
        name = name[:-4]
    r1 = int(results_dict['R1'][i]) if results_dict['R1'][i] != '--' else 0
    r2 = int(results_dict['R2'][i]) if results_dict['R2'][i] != '--' else 0
    r3 = int(results_dict['R3'][i]) if results_dict['R3'][i] != '--' else 0
    r4 = int(results_dict['R4'][i]) if results_dict['R4'][i] != '--' else 0
    scores = [r1, r2, r3, r4]
    score = 0
    for j in range(rounds):
        # If player has made the cut
        if scores[j] != 0:
            # Add the par score
            score += scores[j] - par
        # If player missed the cut
        else:
            # Add the worst par score
            score += max(scores) - par
    # Add score and golfer to dictionary
    golfer_scores[name] = score

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
        player_score += golfer_scores[golfer]
    players.append(player)
    player_scores.append(player_score)

# Sort the players by score in reverse
sorted_players = sorted(zip(players, player_scores), reverse=True)

# Put the sorted list into pandas for output and showing
player_df = pd.DataFrame(sorted_players, columns=['Name', 'Score'], index=range(1,len(players)+1))
player_df.to_csv('scores.csv')
print(player_df)
