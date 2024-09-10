#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import random

def getPlayerScores():
    df = pd.read_csv('data/playerScores.csv')
    return df

def getPlayerScoresHtml():
    df = pd.read_csv('data/playerScores.csv')
    # combine gross/net
    columns = df.columns
    courses = [x for x in columns if (x not in ['player', 'team', 'hcp'] and not x.endswith('_net'))]
    df = df.sort_values(['Total_net'])
    for c in courses:
        df[c] = df[c].astype(int).astype(str) +' / ' + df[c+'_net'].astype(int).astype(str)

    df = df[['player', 'hcp'] + courses]
    return df.to_html(index=False, classes="mystyle")

def getCourses():
    df = pd.read_csv('data/playerScores.csv')
    # combine gross/net
    columns = df.columns
    courses = [x for x in columns if (x not in ['player', 'team', 'hcp'] and not x.endswith('_net'))]
    return courses

def getPlayers():
    df = pd.read_csv('data/playerScores.csv')
    return list(df['player'].unique())

def getCoursesHtml():
    files = os.listdir('data')
    courseFiles = [x for x in files if x.startswith('course_')]
    courses = [x.split('course_')[-1].replace('.csv', '') for x in courseFiles]
    html = ""
    team1Score = 0
    team2Score = 0
    for i, c in enumerate(courses):
        newTable = "<h2>{}</h2>".format(c)
        df = pd.read_csv('data/{}'.format(courseFiles[i]))
        team1Score += df['Team 1 Points'].sum()
        team2Score += df['Team 2 Points'].sum()
        df.columns = ['Team Sean', 'Points', 'Team JJ', 'Points']
        newTable += df.to_html(index=False, classes="mystyle")
        html += newTable
    return html, team1Score, team2Score

def getTeamScores():
    files = os.listdir('data')
    courseFiles = [x for x in files if x.startswith('course_')]
    courses = [x.split('course_')[-1].replace('.csv', '') for x in courseFiles]


def buildScoreboards():
    playerScoresHtml = getPlayerScoresHtml()
    matchesHtml, team1Score, team2Score = getCoursesHtml()

    HTML = """
        <html>
          <head><title>Rudy's Cup 2024</title></head>
          <link rel="stylesheet" type="text/css" href="/static/df_style.css"/>
          <body>
          <div class="header">
              <a href="/" class="logo">Rudy's Cup 2024</a>
              <br>
              <div class="header-right">
                <a class="active" href="/enter-player-score">Enter Player Score</a>
                <br>
                <a class="active" href="/enter-team-points">Enter Team Points</a>
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
            <br>
            {playerTable}
            {matches}
            <a class="active" href="/final-matchups">Final Matchups</a>
          </body>
        </html>
        """.format(team1_score=team1Score, team2_score=team2Score, playerTable=playerScoresHtml,
                   matches=matchesHtml)

    return HTML

def buildFinalMatchups():
    df = pd.read_csv('data/playerScores.csv')
    team1 = df[df['team'].isin(['1', 1])].sort_values('Total_net').reset_index()[['player']]
    team2 = df[df['team'].isin(['2', 2])].sort_values('Total_net').reset_index()[['player']]
    matches = team1.join(team2, lsuffix='_t1', rsuffix='_t2')
    matches.columns = ['Team Sean', 'Team JJ']
    matchesHtml = matches.to_html(index=False, classes="mystyle")
    HTML = """
            <html>
              <head><title>Rudy's Cup 2024</title></head>
              <link rel="stylesheet" type="text/css" href="/static/df_style.css"/>
              <body>
              <div class="header">
                  <a href="/" class="logo">Rudy's Cup 2024</a>
                  <br>
                  <div class="header-right">
                    <a class="active" href="/enter-player-score">Enter Player Score</a>
                    <br>
                    <a class="active" href="/enter-team-points">Enter Team Points</a>
                  </div>
              </div>

                <h2>Final Matchups</h2>        
                {matches}
              
              </body>
            </html>.
            """.format(matches=matchesHtml)

    return HTML