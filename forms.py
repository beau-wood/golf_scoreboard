import pandas as pd
import scoreboard

PLAYERS = scoreboard.getPlayers()
COURSES = scoreboard.getCourses()


def buildPlayerScoreForm():
    form = """
    <form action="/player-scores-entered" method = "POST" class="mystyle">
        <label for="name">Name:</label>
        <select class="mystyle" id="name" name="name">
    """
    for n in PLAYERS:
        form += '<option class="mystyle" value="{name}" required>{name}</option>'.format(name=n)
    form += '</select><br><br>'
    form += '<label for="course">Course:</label> <select class="mystyle" id="course" name="course">'
    for c in COURSES:
        form += '<option class="mystyle" value="{course}" required>{course}</option>'.format(course=c)
    form += '</select><br><br>'

    form += """
        <label for="score">Score:</label>
        <input class="mystyle" type="text" id="score" name="score" required><br><br>
        <label for="score_net">Score (Net):</label>
        <input class="mystyle" type="text" id="score" name="score_net" required><br><br>
        <input class="mystyle" type="submit"></form></body></html>
    """


    html = """
    <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="/static/df_style.css"/>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Golf Courses Registration</title>
        </head>
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
        <div class="form-container">
        """

    html += form

    html += """
            </div>
        </body>
        </html>
    """

    return html


def storePlayerScores(formData):
    df = pd.read_csv('data/playerScores.csv')
    player = formData['name']
    course = formData['course']
    score = formData['score']
    score_net = formData['score_net']
    df.set_index('player', inplace=True)
    df.loc[player, course] = score
    df.loc[player, course + '_net'] = score_net

    # calc totals
    courses = [x for x in df.columns if (x not in ['player', 'team', 'hcp', 'Total', 'Total_net']) and (not x.endswith('_net'))]
    coursesNet = [x for x in df.columns if x.endswith('_net')]
    df[courses] = df[courses].astype(float)
    df[coursesNet] = df[coursesNet].astype(float)
    df.loc[player, 'Total'] = df.loc[player, courses].sum()
    df.loc[player, 'Total_net'] = df.loc[player, coursesNet].sum()

    df.to_csv('data/playerScores.csv', index=True)


def buildTeamPointsForm():
    form = """
        <form action="/team-points-entered" method = "POST" class="mystyle">
            <label for="course">Course:</label>
            <select class="mystyle" id="course" name="course">
        """
    for c in COURSES:
        form += '<option class="mystyle" value="{course}" required>{course}</option>'.format(course=c)
    form += '</select><br><br>'

    form += """
            <h4> Match 1</h4>
            <label for="team1-m1">Team 1:</label>
            <input class="mystyle" type="text" id="team1-m1" name="team1-m1" required><br><br>
            <label for="team1-m1-points">Team 1 Points:</label>
            <input class="mystyle" type="text" id="team1-m1-points" name="team1-m1-points" required><br><br>
            
            <label for="team2-m1">Team 2:</label>
            <input class="mystyle" type="text" id="team2-m1" name="team2-m1" required><br><br>
            <label for="team2-m1-points">Team 2 Points:</label>
            <input class="mystyle" type="text" id="team2-m1-points" name="team2-m1-points" required><br><br>
            
            <h4> Match 2</h4>
            <label for="team1-m2">Team 1:</label>
            <input class="mystyle" type="text" id="team1-m2" name="team1-m2" required><br><br>
            <label for="team1-m2-points">Team 1 Points:</label>
            <input class="mystyle" type="text" id="team1-m2-points" name="team1-m2-points" required><br><br>
            
            <label for="team2-m2">Team 2:</label>
            <input class="mystyle" type="text" id="team2-m2" name="team2-m2" required><br><br>
            <label for="team2-m2-points">Team 2 Points:</label>
            <input class="mystyle" type="text" id="team2-m2-points" name="team2-m2-points" required><br><br>
            
            
            <input class="mystyle" type="submit"></form></body></html>
        """

    html = """
        <!DOCTYPE html>
            <html>
            <head>
                <link rel="stylesheet" type="text/css" href="/static/df_style.css"/>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Golf Courses Registration</title>
            </head>
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
            <div class="form-container">
            """

    html += form

    html += """
                </div>
            </body>
            </html>
        """

    return html

def storeTeamPoints(formData):
    course = formData['course']

    m1 = (formData['team1-m1'], formData['team1-m1-points'], formData['team2-m1'], formData['team2-m1-points'])
    m2 = (formData['team1-m2'], formData['team1-m2-points'], formData['team2-m2'], formData['team2-m2-points'])

    df = pd.DataFrame([m1, m2], columns=['Team1', 'Team 1 Points', 'Team 2', 'Team 2 Points'])
    df.to_csv('data/course_{}.csv'.format(course), index=False)

