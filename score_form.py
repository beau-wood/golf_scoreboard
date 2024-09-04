import pandas as pd
import scoreboard

Players = scoreboard.getAllPlayers().keys()
Courses = scoreboard.getCourses().keys()


def buildHTML():

    formItems = ['<form action="/entered" method = "POST" class="mystyle">']
    # Names
    formItems.append('<label for="name">Name:</label>')
    formItems.append('<select class="mystyle" id="name" name="name">')
    for n in Players:
        formItems.append('<option class="mystyle" value="{name}" required>{name}</option>'.format(name=n))
    formItems.append('</select><br><br>')

    # Courses
    formItems.append('<label for="course">Course:</label>')
    formItems.append('<select class="mystyle" id="course" name="course">')
    for c in Courses:
        formItems.append('<option class="mystyle" value="{course}" required>{course}</option>'.format(course=c))
    formItems.append('</select><br><br>')

    # Score
    formItems.append('<label for="score">Score:</label>')
    formItems.append('<input class="mystyle" type="text" id="score" name="score" required><br><br>')
    
    # Score
    formItems.append('<label for="score_net">Score (Net):</label>')
    formItems.append('<input class="mystyle" type="text" id="score" name="score_net" required><br><br>')

    formItems.append('<input class="mystyle" type="submit"></form></body></html>')


    form = ''.join(formItems)

    html = """
    <!DOCTYPE html>
        <html>
        <head>
          <link rel="stylesheet" type="text/css" href="/static/df_style.css"/>
        </head>
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
        {form}
        
        </body>
        </html>
    """.format(form=form)

    return html



def storeScores(formData):
    df = pd.read_csv('data/playerScores.csv')
    player = formData['name']
    course = formData['course']
    score = formData['score']
    score_net = formData['score_net']
    df.set_index('player', inplace=True)
    df.loc[player, course] = score
    df.loc[player, course+'_net'] = score_net
    df.to_csv('data/playerScores.csv', index=True)
