import os.path
import pandas as pd
from sympy.codegen.ast import continue_

import scoreboard

Players = scoreboard.getAllPlayers()
Courses = scoreboard.getCourses()


# TODO:
# - individual scores table
# - 1v1 handling (create matchups looking at scores for all except 1v1 course scores)

def buildPlayers():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Golf Team Form</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            .form-container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #f9f9f9;
            }
            .form-group {
                margin-bottom: 15px;
            }
            .form-group label {
                display: block;
                margin-bottom: 5px;
            }
            .form-group input {
                width: 100%;
                padding: 8px;
                box-sizing: border-box;
            }
            .team-section {
                margin-bottom: 20px;
            }
            .team-section h2 {
                margin-top: 0;
            }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h1>Golf Team Registration</h1>
            <form action="/players-entered" method="post">
                <!-- Team 1 -->
                <div class="team-section">
                    <h2>Team 1</h2>
                    <div class="form-group">
                        <label for="team1-golfer1-name">Golfer 1 Name:</label>
                        <input type="text" id="team1-golfer1-name" name="team1_golfer1_name" required>
                    </div>
                    <div class="form-group">
                        <label for="team1-golfer1-handicap">Golfer 1 Handicap:</label>
                        <input type="number" id="team1-golfer1-handicap" name="team1_golfer1_handicap" step="0.1" required>
                    </div>
                    <!-- Repeat for other golfers in Team 1 -->
                    <div class="form-group">
                        <label for="team1-golfer2-name">Golfer 2 Name:</label>
                        <input type="text" id="team1-golfer2-name" name="team1_golfer2_name" required>
                    </div>
                    <div class="form-group">
                        <label for="team1-golfer2-handicap">Golfer 2 Handicap:</label>
                        <input type="number" id="team1-golfer2-handicap" name="team1_golfer2_handicap" step="0.1" required>
                    </div>
                    <div class="form-group">
                        <label for="team1-golfer3-name">Golfer 3 Name:</label>
                        <input type="text" id="team1-golfer3-name" name="team1_golfer3_name" required>
                    </div>
                    <div class="form-group">
                        <label for="team1-golfer3-handicap">Golfer 3 Handicap:</label>
                        <input type="number" id="team1-golfer3-handicap" name="team1_golfer3_handicap" step="0.1" required>
                    </div>
                    <div class="form-group">
                        <label for="team1-golfer4-name">Golfer 4 Name:</label>
                        <input type="text" id="team1-golfer4-name" name="team1_golfer4_name" required>
                    </div>
                    <div class="form-group">
                        <label for="team1-golfer4-handicap">Golfer 4 Handicap:</label>
                        <input type="number" id="team1-golfer4-handicap" name="team1_golfer4_handicap" step="0.1" required>
                    </div>
                </div>
    
                <!-- Team 2 -->
                <div class="team-section">
                    <h2>Team 2</h2>
                    <div class="form-group">
                        <label for="team2-golfer1-name">Golfer 1 Name:</label>
                        <input type="text" id="team2-golfer1-name" name="team2_golfer1_name" required>
                    </div>
                    <div class="form-group">
                        <label for="team2-golfer1-handicap">Golfer 1 Handicap:</label>
                        <input type="number" id="team2-golfer1-handicap" name="team2_golfer1_handicap" step="0.1" required>
                    </div>
                    <!-- Repeat for other golfers in Team 2 -->
                    <div class="form-group">
                        <label for="team2-golfer2-name">Golfer 2 Name:</label>
                        <input type="text" id="team2-golfer2-name" name="team2_golfer2_name" required>
                    </div>
                    <div class="form-group">
                        <label for="team2-golfer2-handicap">Golfer 2 Handicap:</label>
                        <input type="number" id="team2-golfer2-handicap" name="team2_golfer2_handicap" step="0.1" required>
                    </div>
                    <div class="form-group">
                        <label for="team2-golfer3-name">Golfer 3 Name:</label>
                        <input type="text" id="team2-golfer3-name" name="team2_golfer3_name" required>
                    </div>
                    <div class="form-group">
                        <label for="team2-golfer3-handicap">Golfer 3 Handicap:</label>
                        <input type="number" id="team2-golfer3-handicap" name="team2_golfer3_handicap" step="0.1" required>
                    </div>
                    <div class="form-group">
                        <label for="team2-golfer4-name">Golfer 4 Name:</label>
                        <input type="text" id="team2-golfer4-name" name="team2_golfer4_name" required>
                    </div>
                    <div class="form-group">
                        <label for="team2-golfer4-handicap">Golfer 4 Handicap:</label>
                        <input type="number" id="team2-golfer4-handicap" name="team2_golfer4_handicap" step="0.1" required>
                    </div>
                </div>
    
                <div class="form-group">
                    <button type="submit">Submit</button>
                </div>
            </form>
        </div>
    </body>
    </html>
    """

    return html


def storePlayers(formData):
    # team1-golfer1-name
    # team1-golfer1-handicap
    team1 = [(formData['team1_golfer1_name'], formData['team1_golfer1_handicap']),
             (formData['team1_golfer2_name'], formData['team1_golfer2_handicap']),
             (formData['team1_golfer3_name'], formData['team1_golfer3_handicap']),
             (formData['team1_golfer4_name'], formData['team1_golfer4_handicap'])]

    team2 = [(formData['team2_golfer1_name'], formData['team2_golfer1_handicap']),
             (formData['team2_golfer2_name'], formData['team2_golfer2_handicap']),
             (formData['team2_golfer3_name'], formData['team2_golfer3_handicap']),
             (formData['team2_golfer4_name'], formData['team2_golfer4_handicap'])]

    team1df = pd.DataFrame(team1, columns=['Name', 'Handicap'])
    team2df = pd.DataFrame(team2, columns=['Name', 'Handicap'])

    team1df.to_csv('data/team1.csv', index=False)
    team2df.to_csv('data/team2.csv', index=False)


def buildCourses():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Golf Courses Registration</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            .form-container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #f9f9f9;
            }
            .form-group {
                margin-bottom: 15px;
            }
            .form-group label {
                display: block;
                margin-bottom: 5px;
            }
            .form-group input,
            .form-group select {
                width: 100%;
                padding: 8px;
                box-sizing: border-box;
            }
            .course-section {
                margin-bottom: 20px;
            }
            .course-section h2 {
                margin-top: 0;
            }
            .remove-course {
                color: red;
                cursor: pointer;
                display: block;
                margin-top: 5px;
            }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h1>Golf Courses Registration</h1>
            <form action="/courses-entered" method="post">
                <!-- Golf Courses Section -->
                <div class="course-section">
                    <h2>Golf Courses</h2>
                    <div id="courses-container">
                        <div class="form-group course-group">
                            <label for="course1-name">Course Name:</label>
                            <input type="text" id="course1-name" name="course_name[]" required>
                            
                            <label for="course1-format">Format:</label>
                            <select id="course1-format" name="course_format[]" required>
                                <option value="1v1">1v1 format</option>
                                <option value="2v2">2v2 format</option>
                            </select>
                            <span class="remove-course" onclick="removeCourse(this)">Remove</span>
                        </div>
                    </div>
                    <button type="button" onclick="addCourse()">Add Another Course</button>
                </div>
    
                <div class="form-group">
                    <button type="submit">Submit</button>
                </div>
            </form>
        </div>
    
        <script>
            let courseCount = 1;
    
            function addCourse() {
                courseCount++;
                const coursesContainer = document.getElementById('courses-container');
                const courseGroup = document.createElement('div');
                courseGroup.className = 'form-group course-group';
                courseGroup.innerHTML = `
                    <label for="course${courseCount}-name">Course Name:</label>
                    <input type="text" id="course${courseCount}-name" name="course_name[]" required>
                    
                    <label for="course${courseCount}-format">Format:</label>
                    <select id="course${courseCount}-format" name="course_format[]" required>
                        <option value="1v1">1v1 format</option>
                        <option value="2v2">2v2 format</option>
                    </select>
                    <span class="remove-course" onclick="removeCourse(this)">Remove</span>
                `;
                coursesContainer.appendChild(courseGroup);
            }
    
            function removeCourse(element) {
                const courseGroup = element.parentElement;
                courseGroup.remove();
            }
        </script>
    </body>
    </html>
    """

    return html


def storeCourses(formData):
    players = list(scoreboard.getAllPlayers().keys())
    courses = []
    for i, course in enumerate(zip(formData.getlist('course_name[]'), formData.getlist('course_format[]'))):
        courses.append(course)
    df = pd.DataFrame(courses, columns=['course', 'format'])
    df.to_csv('data/courses.csv', index=False)

    # add indiScores file
    if len(df[df['format'] == '1v1']) > 0:
        indiCourses = []
        for course in df[df['format'] == '1v1']['course'].unique():
            indiCourses.append([course] + [0]*len(players))
        df = pd.DataFrame(indiCourses, columns=['course'] + players)
        df.to_csv('data/indiScores.csv', index=False)

    # add playerScores file
    rows = []
    coursesWithNets = []
    for c in courses:
        coursesWithNets.append(c[0])
        coursesWithNets.append(c[0] + '_net')
    for p in players:
        rows.append([p] + [0]*len(coursesWithNets))
    df = pd.DataFrame(rows, columns=['player'] + coursesWithNets)
    df.to_csv('data/playerScores.csv', index=False)

def buildMatchups():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Golf Team Form</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            .form-container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #f9f9f9;
            }
            .form-group {
                margin-bottom: 15px;
            }
            .form-group label {
                display: block;
                margin-bottom: 5px;
            }
            .form-group input {
                width: 100%;
                padding: 8px;
                box-sizing: border-box;
            }
            .team-section {
                margin-bottom: 20px;
            }
            .team-section h2 {
                margin-top: 0;
            }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h1>Matchups</h1>
            <form action="/matchups-entered" method="post">
    """
    courses = scoreboard.getCourses()

    courseForms = []
    for course, value in courses.items():
        if value['format'] == '1v1':
            continue
        courseHtml = """
        <!-- Team 1 -->
            <h2>{course}</h2>
            <div class="matchup-group">
                <h4>Match 1</h4>
                <div class="form-group">
                    <label for="team1-m1-{course}">Team 1:</label>
                    <input type="text" id="team1-m1-{course}" name="team1-m1-{course}" required>
                </div>
                <div class="form-group">
                    <label for="team2-m1-{course}">Team 2:</label>
                    <input type="text" id="team2-m1-{course}" name="team2-m1-{course}" required>
                </div>
            </div>
            <div class="matchup-group">
                <h4>Match 2</h4>
                <div class="form-group">
                    <label for="team1-m2-{course}">Team 1:</label>
                    <input type="text" id="team1-m2-{course}" name="team1-m2-{course}" required>
                </div>
                <div class="form-group">
                    <label for="team2-m2-{course}">Team 2:</label>
                    <input type="text" id="team2-m2-{course}" name="team2-m2-{course}" required>
                </div>
            </div>
        """.format(course=course)
        courseForms.append(courseHtml)

    courses = ''.join(courseForms)
    html += courses

    html += """
                <div class="form-group">
                    <button type="submit">Submit</button>
                </div>
            </form>
        </div>
    </body>
    </html>
    """
    return html


def storeMatchups(formData):
    courses = scoreboard.getCourses()
    matchups = []
    for course, value in courses.items():
        if value['format'] == '1v1':
            continue
        matches = [(course, formData['team1-m1-{}'.format(course)], formData['team2-m1-{}'.format(course)],
                            formData['team1-m2-{}'.format(course)], formData['team2-m2-{}'.format(course)])]
        matchups.extend(matches)

    df = pd.DataFrame(matchups, columns=['course', 'team1-m1', 'team2-m1', 'team1-m2', 'team2-m2'])
    df.to_csv('data/matchups.csv', index=False)

    # also create teamScores.csv if doesnt exist
    if not os.path.isfile('data/teamScores.csv'):
        teamScores = []
        for course, value in courses.items():
            if value['format'] == '1v1':
                continue
            teamScores.append((course, 0,0,0,0))
        df = pd.DataFrame(teamScores, columns=['course', 'team1-m1', 'team2-m1', 'team1-m2', 'team2-m2'])
        df.to_csv('data/teamScores.csv', index=False)


def buildTeamScores():
    matchups = scoreboard.getMatchups().to_dict('records')

    html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Golf Team Form</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                }
                .form-container {
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    background-color: #f9f9f9;
                }
                .form-group {
                    margin-bottom: 15px;
                }
                .form-group label {
                    display: block;
                    margin-bottom: 5px;
                }
                .form-group input {
                    width: 100%;
                    padding: 8px;
                    box-sizing: border-box;
                }
                .team-section {
                    margin-bottom: 20px;
                }
                .team-section h2 {
                    margin-top: 0;
                }
            </style>
        </head>
        <body>
            <div class="form-container">
                <h1>Matchups</h1>
                <form action="/team-scores-entered" method="post">
        """

    matchupForms = []
    for matchup in matchups:
        matchup = """
            <!-- Team 1 -->
                <div class="matchup-group">
                    <h2>{course}</h2>
                    <div class="form-group">
                        <label for="team1-m1-{course}-score">{team1_m1}:</label>
                        <input type="text" id="team1-m1-{course}-score" name="team1-m1-{course}-score">
                    </div>
                    <div class="form-group">
                        <label for="team2-m1-{course}">{team2_m1}:</label>
                        <input type="text" id="team2-m1-{course}-score" name="team2-m1-{course}-score">
                    </div>
                    <div class="form-group">
                        <label for="team1-m2-{course}-score">{team1_m2}:</label>
                        <input type="text" id="team1-m2-{course}-score" name="team1-m2-{course}-score">
                    </div>
                    <div class="form-group">
                        <label for="team2-m2-{course}">{team2_m2}:</label>
                        <input type="text" id="team2-m2-{course}-score" name="team2-m2-{course}-score">
                    </div>
                </div>
                
            """.format(course=matchup['course'], team1_m1=matchup['team1-m1'], team2_m1=matchup['team2-m1'],
                                                 team1_m2=matchup['team1-m2'], team2_m2=matchup['team2-m2'])
        matchupForms.append(matchup)

    matchupTotal = ''.join(matchupForms)
    html += matchupTotal

    html += """
                    <div class="form-group">
                        <button type="submit">Submit</button>
                    </div>
                </form>
            </div>
        </body>
        </html>
        """
    return html

def storeTeamScores(formData):
    teamScores = pd.read_csv('data/teamScores.csv')
    teamScores.set_index('course', inplace=True)
    matchups = scoreboard.getMatchups().to_dict('records')
    print(formData)
    for match in matchups:
        scoreTeam1M1 = formData['team1-m1-{}-score'.format(match['course'])]
        scoreTeam2M1 = formData['team2-m1-{}-score'.format(match['course'])]
        scoreTeam1M2 = formData['team1-m2-{}-score'.format(match['course'])]
        scoreTeam2M2 = formData['team2-m2-{}-score'.format(match['course'])]

        if scoreTeam1M1 != '':
            teamScores.loc[match['course'], 'team1-m1'] = scoreTeam1M1
        if scoreTeam2M1 != '':
            teamScores.loc[match['course'], 'team2-m1'] = scoreTeam2M1
        if scoreTeam1M2 != '':
            teamScores.loc[match['course'], 'team1-m2'] = scoreTeam1M2
        if scoreTeam2M2 != '':
            teamScores.loc[match['course'], 'team2-m2'] = scoreTeam2M2

    teamScores.to_csv('data/teamScores.csv')


def buildIndiScores():
    players = list(scoreboard.getAllPlayers().keys())
    courses = scoreboard.getCourses()
    courses = [k for k,v in courses.items() if v['format'] == '1v1']

    coursesHtml = ""
    for c in courses:
        coursesHtml += '<option class="mystyle" value="{name}" required>{name}</option>'.format(name=c)
    playersHtml = ""
    for p in players:
        playersHtml += '<option class="mystyle" value="{name}" required>{name}</option>'.format(name=p)

    html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Golf Team Form</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                }
                .form-container {
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    background-color: #f9f9f9;
                }
                .form-group {
                    margin-bottom: 15px;
                }
                .form-group label {
                    display: block;
                    margin-bottom: 5px;
                }
                .form-group input {
                    width: 100%;
                    padding: 8px;
                    box-sizing: border-box;
                }
                .team-section {
                    margin-bottom: 20px;
                }
                .team-section h2 {
                    margin-top: 0;
                }
            </style>
        </head>
        
        """

    html += """
        <body>
            <div class="form-container">
                <h1>Matchups</h1>
                <form action="/indi-scores-entered" method="post">
                <div class="form-group">
                    <label for="course">Course:</label>
                    <select class="mystyle" id="course" name="course">
                        {courses}
                    </select>
                </div>
                <div class="form-group">
                    <label for="player">Player:</label>
                    <select class="mystyle" id="player" name="player">
                        {players}
                    </select>
                </div>
                <div class="form-group">
                    <label for="points">Points:</label>
                    <input type="text" id="points" name="points">
                </div>
                <div class="form-group">
                    <button type="submit">Submit</button>
                </div>
                </form>
            </div>
        </body>
        </html>
        """.format(courses=coursesHtml, players=playersHtml)
    return html


def storeIndiScores(formData):
    teamScores = pd.read_csv('data/indiScores.csv')
    teamScores.set_index('course', inplace=True)
    course = formData['course']
    player = formData['player']
    points = formData['points']
    teamScores.loc[course, player] = points
    print(teamScores)
    teamScores.to_csv('data/indiScores.csv', index=True)
