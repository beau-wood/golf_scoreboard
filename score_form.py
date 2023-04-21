import pandas as pd
import scoreboard

Players = scoreboard.getPlayers()
Courses = scoreboard.Courses


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

    # Winner?
    # Courses
    formItems.append('<label for="winner">Result:</label>')
    formItems.append('<select class="mystyle" id="winner" name="winner">')
    for c in ['Loss', 'Win']:
        formItems.append('<option class="mystyle" value="{winner}" required>{winner}</option>'.format(winner=c))
    formItems.append('</select><br><br>')

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
          <a href="/" class="logo">Rudy's Cup 2023</a>
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
    print(formData)
    df = pd.read_csv('Scoreboard.csv')
    df.loc[df['Name'] == formData['name'], formData['course']] = int(formData['score'])
    df.loc[df['Name'] == formData['name'], formData['course']+'_Pts'] = 1 if formData['winner'] == 'Win' else 0
    df = df.fillna(0)
    df['Total'] = df['Turtle'] + df['Ocean'] + df['Osprey']
    #df[['Turtle', 'Ocean', 'Osprey']] = df[['Turtle', 'Ocean', 'Osprey']].astype(int)
    df.to_csv('Scoreboard.csv', index=False)