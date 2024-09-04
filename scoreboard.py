#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import random

def getCourses():
    df = pd.read_csv('data/courses.csv')
    courses = df.set_index('course').to_dict('index')
    # 'Sand Valley': {'format': '2v2'}
    return courses

def getTeam(team=[1,2][0]):
    if team == 1:
        df = pd.read_csv('data/team1.csv')
        team = df.set_index('Name').to_dict('index')
    else:
        df = pd.read_csv('data/team2.csv')
        team = df.set_index('Name').to_dict('index')
    return team

def getAllPlayers():
    team1 = getTeam(1)
    team2 = getTeam(2)
    players = {**team1, **team2}
    # 'Sean ODonovan': {'Handicap': 18.1}
    return players

def getMatchups():
    df = pd.read_csv('data/matchups.csv')
    return df

def getPlayerScores():
    df = pd.read_csv('data/playerScores.csv')
    return df

def getTeamScores():
    df = pd.read_csv('data/teamScores.csv')
    return df

def getIndiScores():
    df = pd.read_csv('data/indiScores.csv')
    return df

def get1v1Matchups():
    return

def buildScoreboards():
    courses = getCourses()
    team1 = getTeam(1)
    team2 = getTeam(2)
    players = getAllPlayers()
    matchups = getMatchups()
    playerScores = getPlayerScores()
    teamScores = getTeamScores()
    indiScores = getIndiScores()

    # Team Scores
    team1Score, team2Score = getTeamTotalScores()

    # Player Score Table
    playerTableHtml = getPlayerTableHtml()

    # Team Tables
    teamTableHtml = ""
    for c, value in courses.items():
        if value['format'] != '1v1':
            teamTableHtml += buildCourseHtml(c)

    # Individual tables
    indiTableHtml = ""
    for c, value in courses.items():
        if value['format'] == '1v1':
            indiTableHtml += buildIndiCourseHtml(c)

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
                <a class="active" href="/enter">Enter Player Score</a>
                <br>
                <a class="active" href="/team-scores">Enter 2v2 Points</a>
                <br>
                <a class="active" href="/indi-scors">Enter 1v1 Points</a>
              </div>
          </div>

            <h2>Team Scores</h2>        
            <table class='mystyle'>
              <tr>
                <td><img src="static/sean_throwback.jpg" alt="Sean" style='width: 160px'></td>
                <td>{team1_score}</td>
                <td><img src="static/jj_ravens.jpg" alt="JJ" style='width: 160px'></td>
                <td>{team2_score}</td>
              </tr>
            </table>
            {playerTable}
            
            {team_tables}
            
            {indi_tables}

          </body>
        </html>.
        """.format(team1_score=team1Score, team2_score=team2Score, playerTable=playerTableHtml,
                   team_tables=teamTableHtml, indi_tables=indiTableHtml)

    return HTML


def getTeamTotalScores():
    team1Score = 0
    team2Score = 0
    courses = getCourses()
    for c, value in courses.items():
        if value['format'] == '2v2':
            table = buildCourseTable(c)
        elif value['format'] == '1v1':
            table = buildIndiCourseTable(c)
        else:
            raise
        table.columns = ['Team1', 'Team1_Score', 'Team2', 'Team2_Score']
        team1Score += table['Team1_Score'].sum()
        team2Score += table['Team2_Score'].sum()

    return team1Score, team2Score


def getPlayerTableHtml():
    players = getAllPlayers()
    playerScores = getPlayerScores()
    courses = getCourses()

    playerScores.set_index('player', inplace=True)
    playerTableRows = []
    for player in list(players.keys()):
        playerRow = [player]
        playerTotal = 0
        playerTotalNet = 0
        for course in list(courses.keys()):
            playerTotal += playerScores.loc[player, course]
            playerTotalNet += playerScores.loc[player, course + '_net']
            playerScore = playerScores.loc[player, course].astype(str) + ' / ' + playerScores.loc[
                player, course + '_net'].astype(str)
            playerRow.append(playerScore)
        playerRow.append(''.join([str(playerTotal), ' / ', str(playerTotalNet)]))
        playerTableRows.append(playerRow)
    print(playerTableRows)
    playerTable = pd.DataFrame(playerTableRows, columns=['Name'] + list(courses.keys()) + ['Total'])
    playerTable.sort_values(['Total'], ascending=True, inplace=True, key=lambda x: x.str.split('/ ').str[-1].astype(float))
    playerTableHtml = playerTable.to_html(index=False, classes="mystyle")
    return playerTableHtml


def buildCourseTable(course):
    matchups = getMatchups()
    teamScores = getTeamScores()

    teamScores.set_index('course', inplace=True)
    scores = teamScores.loc[course]
    matchups.set_index('course', inplace=True)
    matchups = matchups.loc[course]
    row1 = [matchups.loc['team1-m1'], scores.loc['team1-m1'], matchups.loc['team2-m1'], scores.loc['team2-m1']]
    row2 = [matchups.loc['team1-m2'], scores.loc['team1-m2'], matchups.loc['team2-m2'], scores.loc['team2-m2']]

    table = pd.DataFrame([row1, row2], columns=['Team 1', 'Score', 'Team 2', 'Score'])
    return table

def buildCourseHtml(course):
    table = buildCourseTable(course)
    tableHtml = "<h2>{}</h2>".format(course)
    tableHtml += table.to_html(index=False, classes="mystyle")

    return tableHtml

def buildIndiCourseTable(course):
    indiScores = getIndiScores()
    indiScores.set_index('course', inplace=True)
    indiScores = indiScores.loc[course]
    # calc indi matchups by looking at total net score and aligning between teams
    playerScores = getPlayerScores()
    courses = getCourses()
    team1 = getTeam(1)
    team2 = getTeam(2)
    countedCourses = [k + '_net' for k, v in courses.items() if v['format'] == '2v2']
    playerScores = playerScores[['player'] + countedCourses].set_index(['player'])
    playerScores['total'] = playerScores.sum(axis=1)
    team1 = playerScores.loc[list(team1.keys())].sort_values(['total'])
    team2 = playerScores.loc[list(team2.keys())].sort_values(['total'])
    matchups = []
    for m in zip(team1.index.values, team2.index.values):
        matchups.append(m)

    # build table
    rows = []
    for m in matchups:
        rows.append([m[0], indiScores.loc[m[0]], m[1], indiScores.loc[m[1]]])
    table = pd.DataFrame(rows, columns=['Team1', 'Score', 'Team2', 'Score'])
    return table

def buildIndiCourseHtml(course):
    table = buildIndiCourseTable(course)
    tableHtml = "<h2>{}</h2>".format(course)
    tableHtml += table.to_html(index=False, classes="mystyle")
    return tableHtml





