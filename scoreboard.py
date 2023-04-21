#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import random



Courses = ['Turtle', 'Ocean', 'Osprey']

def getPlayers():
    df = pd.read_csv('Handicaps.csv')
    players = df.set_index('Name').to_dict('index')
    for k, v in players.items():
        players[k] = v.get('Handicap')
    return players

def getMatchups():
    xlsx = pd.ExcelFile('Matchups.xlsx')
    pairings = []
    for course in Courses:
        df = pd.read_excel(xlsx, course)
        pairings.append(df.values)
    return pairings

def getTeams():
    xlsx = pd.ExcelFile('Matchups.xlsx')
    pairings = []
    df = pd.read_excel(xlsx, 'Turtle')
    mac = df['Team Mac'].values
    sam = df['Team Sam'].values
    return {'Team Mac': mac,
            'Team Sam': sam}


def buildHTML():
    players = getPlayers()
    pairings = getMatchups()
    teams = getTeams()

    # Read scoreboard from csv and serialize to html
    df = pd.read_csv('Scoreboard.csv')
    df.fillna(0, inplace=True)
    df[['Turtle', 'Ocean', 'Osprey', 'Total']] = df[['Turtle', 'Ocean', 'Osprey', 'Total']].astype(int)
    df['Total'] = df['Turtle'] + df['Ocean'] + df['Osprey']
    df['hcp'] = df['Name'].apply(lambda x: players.get(x))
    df['Turtle_Pts'] = df['Turtle_Pts'].astype(int)
    df['Ocean_Pts'] = df['Ocean_Pts'].astype(int)
    df['Osprey_Pts'] = df['Osprey_Pts'].astype(int)
    namedScores = df.set_index('Name').to_dict('index')

    df.drop(['Turtle_Pts', 'Ocean_Pts', 'Osprey_Pts'], axis=1, inplace=True)

    # create Net df
    dfNet = df.copy()
    dfNet[['Turtle', 'Ocean', 'Osprey']] = dfNet[['Turtle', 'Ocean', 'Osprey']] - dfNet[['hcp']].values
    dfNet['Turtle'] = dfNet['Turtle'].apply(lambda x: x if x >= 0 else 0)
    dfNet['Ocean'] = dfNet['Ocean'].apply(lambda x: x if x >= 0 else 0)
    dfNet['Osprey'] = dfNet['Osprey'].apply(lambda x: x if x >= 0 else 0)
    dfNet['Total'] = dfNet['Turtle'] + dfNet['Ocean'] + dfNet['Osprey']

    # add in nets
    df.set_index('Name', inplace=True)
    dfNet.set_index('Name', inplace=True)
    df['Turtle'] = df['Turtle'].astype(str) + ' / ' + dfNet['Turtle'].astype(str)
    df['Ocean'] = df['Ocean'].astype(str) + ' / ' + dfNet['Ocean'].astype(str)
    df['Osprey'] = df['Osprey'].astype(str) + ' / ' + dfNet['Osprey'].astype(str)
    df['Total'] = df['Total'].astype(str) + ' / ' + dfNet['Total'].astype(str)
    df.reset_index(inplace=True)

    df = df[['Name', 'hcp', 'Turtle', 'Ocean', 'Osprey', 'Total']]
    df.sort_values(['Total'], ascending=True, inplace=True, key=lambda x: x.str.split('/ ').str[-1].astype(int))
    scoreboardHtml = df.to_html(index=False, classes="mystyle")
    scoreboardHtml = scoreboardHtml.replace('<tr style="text-align: right;">', '<tr style="text-align: left;">')

    # Course Scoreboards
    courses = []
    for i, course in enumerate(Courses):
        frameRows = []
        for pairing in pairings[i]:
            player1 = pairing[0]
            player1Score = namedScores[player1][course] - (players[player1])
            player1Score = player1Score if player1Score > 0 else 0
            player1Score = "{} / {}".format(namedScores[player1][course], player1Score)
            player1Points = namedScores[player1][course + '_Pts']
            player2 = pairing[1]
            player2Score = namedScores[player2][course] - (players[player2])
            player2Score = player2Score if player2Score > 0 else 0
            player2Score = "{} / {}".format(namedScores[player2][course], player2Score)
            player2Points = namedScores[player2][course + '_Pts']

            frameRows.append([player1, player1Score, player1Points, player2, player2Score, player2Points])
        courseFrame = pd.DataFrame(frameRows, columns=["Team Mac", "Gross/Net", "Pts", "Team Sam", "Gross/Net", "Pts"])
        courseHtml = courseFrame.to_html(index=False, classes="mystyle").replace('<tr style="text-align: right;">', '<tr style="text-align: left;">')
        courses.append(courseHtml)

    # Build Team Scoreboard
    teamScores = {'Team Mac': 0, 'Team Sam': 0}
    for player, scores in namedScores.items():
        if player in teams['Team Mac']:
            teamScores['Team Mac'] += scores['Turtle_Pts'] + scores['Ocean_Pts'] + scores['Osprey_Pts']

    # Base HTML
    HTML = """
    <html>
      <head><title>Rudy's Cup 2023</title></head>
      <link rel="stylesheet" type="text/css" href="/static/df_style.css"/>
      <body>
      <div class="header">
          <a href="/" class="logo">Rudy's Cup 2023</a>
          <br>
          <div class="header-right">
            <a class="active" href="/">Home</a>
            <br>
            <a class="active" href="/enter">Enter Score</a>
          </div>
      </div>
      
        <h2>Team Scores</h2>        
        <table class='mystyle'>
          <tr>
            <td><img src="static/IMG_0343.jpg" alt="Mac" style='width: 160px'></td>
            <td>{mac_score}</td>
            <td><img src="static/IMG_1377.jpg" alt="Sam" style='width: 160px'></td>
            <td>{sam_score}</td>
          </tr>
        </table>
        
        <h2>Player Scores</h2> 
        {table}
        
        <h2>Turtle</h2>
        {turtle}
        
        <h2>Ocean</h2>
        {ocean}
        
        <h2>Osprey</h2>
        {osprey}
      </body>
    </html>.
    """.format(mac_score=teamScores['Team Mac'], sam_score=teamScores['Team Sam'], table=scoreboardHtml, turtle=courses[0], ocean=courses[1], osprey=courses[2])


    return HTML




