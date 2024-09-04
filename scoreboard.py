#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import random



Courses = ['Sand Valley', 'Mammoth', 'Sand Valley(2)', 'Sedge']

def getPlayers():
    df = pd.read_csv('data/Handicaps.csv')
    players = df.set_index('Name').to_dict('index')
    for k, v in players.items():
        players[k] = v.get('Handicap')
    return players

def getMatchups():
    xlsx = pd.ExcelFile('data/Matchups.xlsx')
    pairings = []
    for course in Courses:
        df = pd.read_excel(xlsx, course)
        pairings.append(df.values)
    return pairings

def getTeams():
    xlsx = pd.ExcelFile('data/Matchups.xlsx')
    pairings = []
    df = pd.read_excel(xlsx, 'Sand Valley')
    mac = df['Team Sean'].values
    sam = df['Team JJ'].values
    return {'Team Sean': mac,
            'Team JJ': sam}


def buildHTML():
    players = getPlayers()
    pairings = getMatchups()
    teams = getTeams()
    
    netCourses = [x + '_net' for x in Courses]

    # Read scoreboard from csv and serialize to html
    df = pd.read_csv('data/Scoreboard.csv')
    df.fillna(0, inplace=True)
    df[Courses + netCourses + ['Total']] = df[Courses + netCourses + ['Total']].astype(int)
    df['Total'] = df[Courses].sum(axis=1)
    df['hcp'] = df['Name'].apply(lambda x: players.get(x))
    #df['Turtle_Pts'] = df['Turtle_Pts'].astype(int)
    #df['Ocean_Pts'] = df['Ocean_Pts'].astype(int)
    #df['Osprey_Pts'] = df['Osprey_Pts'].astype(int)
    namedScores = df.set_index('Name').to_dict('index')

    df.drop([x for x in df.columns if x.endswith('_Pts')], axis=1, inplace=True)

    # create Net df
    #dfNet = df.copy()
    #totalZero = dfNet['Total'] == 0.0
    #dfNet[Courses] = dfNet[Courses] - dfNet[['hcp']].values
    #dfNet.loc[totalZero, Courses] = 0.0
    #dfNet['Total'] = dfNet[Courses].sum(axis=1)

    # add in nets
    #df.set_index('Name', inplace=True)
    #dfNet.set_index('Name', inplace=True)
    for c in Courses:
        df[c] = df[c].astype(str) + ' / ' + df[c + '_net'].astype(str)
    df['Total'] = df['Total'].astype(str) + ' / ' + df['Total_net'].astype(str)

    df = df[['Name', 'hcp'] + Courses + ['Total']]
    df.sort_values(['Total'], ascending=True, inplace=True, key=lambda x: x.str.split('/ ').str[-1].astype(float))
    scoreboardHtml = df.to_html(index=False, classes="mystyle")
    scoreboardHtml = scoreboardHtml.replace('<tr style="text-align: right;">', '<tr style="text-align: left;">')

    # Course Scoreboards
    courses = []
    for i, course in enumerate(Courses):
        frameRows = []
        for pairing in pairings[i]:
            player1 = pairing[0]
            player1Score = "{} / {}".format(namedScores[player1][course], namedScores[player1][course + '_net'])
            player1Points = namedScores[player1][course + '_Pts']
            player2 = pairing[1]
            player2Score = "{} / {}".format(namedScores[player2][course], namedScores[player2][course + '_net'])
            player2Points = namedScores[player2][course + '_Pts']

            frameRows.append([player1, player1Score, player1Points, player2, player2Score, player2Points])
        courseFrame = pd.DataFrame(frameRows, columns=["Team Sean", "Gross/Net", "Pts", "Team JJ", "Gross/Net", "Pts"])
        courseHtml = courseFrame.to_html(index=False, classes="mystyle").replace('<tr style="text-align: right;">', '<tr style="text-align: left;">')
        courses.append(courseHtml)

    # Build Team Scoreboard
    teamScores = {'Team Sean': 0, 'Team JJ': 0}
    for player, scores in namedScores.items():
        if player in teams['Team Sean']:
            teamScores['Team Sean'] += sum([scores[c + '_Pts'] for c in Courses])
        elif player in teams['Team JJ']:
            teamScores['Team JJ'] += sum([scores[c + '_Pts'] for c in Courses])


    # Base HTML
    HTML = """
    <html>
      <head><title>Rudy's Cup 2024</title></head>
      <link rel="stylesheet" type="text/css" href="/static/df_style.css"/>
      <body>
      <div class="header">
          <a href="/" class="logo">Rudy's Cup 2024</a>
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
            <td><img src="static/sean_throwback.jpg" alt="Sean" style='width: 160px'></td>
            <td>{sean_score}</td>
            <td><img src="static/jj_ravens.jpg" alt="JJ" style='width: 160px'></td>
            <td>{jj_score}</td>
          </tr>
        </table>
        
        <h2>Player Scores</h2> 
        {table}
        
        <h2>Sand Valley</h2>
        {sv}
        
        <h2>Mammoth</h2>
        {mammoth}
        
        <h2>Sand Valley (2)</h2>
        {sv2}
        
        <h2>Sedge Valley</h2>
        {sedge}
      </body>
    </html>.
    """.format(sean_score=teamScores['Team Sean'], jj_score=teamScores['Team JJ'], table=scoreboardHtml, sv=courses[0], mammoth=courses[1], sv2=courses[2], sedge=courses[3])


    return HTML




