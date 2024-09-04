from flask import Flask, render_template, request, redirect, url_for
import scoreboard
import score_form
import admin

application = app = Flask(__name__)


@app.route('/')
def scoreboardPage():  # put application's code here
    return scoreboard.buildScoreboards()

@app.route('/enter', methods=['POST', 'GET'])
def enterScoresPage():
    return score_form.buildHTML()

@app.route('/entered', methods=['POST', 'GET'])
def scoresEnteredPage():
    if request.method == 'POST':
        print(request.form)
        form_data = request.form
        out = score_form.storeScores(form_data)
        # todo reroute to scoreboard
        return redirect(url_for('scoreboardPage'))
    else:
        print("NOT A POST?")


@app.route('/players', methods=['POST', 'GET'])
def adminPlayers():
    return admin.buildPlayers()

@app.route('/players-entered', methods=['POST', 'GET'])
def playersEnteredPage():
    if request.method == 'POST':
        print(request.form)
        form_data = request.form
        out = admin.storePlayers(form_data)
        # todo reroute to scoreboard
        return redirect(url_for('scoreboardPage'))
    else:
        print("NOT A POST?")

@app.route('/courses', methods=['POST', 'GET'])
def adminCourses():
    return admin.buildCourses()

@app.route('/courses-entered', methods=['POST', 'GET'])
def coursesEnteredPage():
    if request.method == 'POST':
        print(request.form)
        form_data = request.form
        out = admin.storeCourses(form_data)
        # todo reroute to scoreboard
        return redirect(url_for('scoreboardPage'))
    else:
        print("NOT A POST?")

@app.route('/matchups', methods=['POST', 'GET'])
def adminMatchups():
    return admin.buildMatchups()

@app.route('/matchups-entered', methods=['POST', 'GET'])
def matchupsEnteredPage():
    if request.method == 'POST':
        print(request.form)
        form_data = request.form
        out = admin.storeMatchups(form_data)
        # todo reroute to scoreboard
        return redirect(url_for('scoreboardPage'))
    else:
        print("NOT A POST?")

@app.route('/team-scores', methods=['POST', 'GET'])
def adminTeamScores():
    return admin.buildTeamScores()

@app.route('/team-scores-entered', methods=['POST', 'GET'])
def teamScoresEnteredPage():
    if request.method == 'POST':
        print(request.form)
        form_data = request.form
        out = admin.storeTeamScores(form_data)
        # todo reroute to scoreboard
        return redirect(url_for('scoreboardPage'))
    else:
        print("NOT A POST?")

@app.route('/indi-scores', methods=['POST', 'GET'])
def adminIndiScores():
    return admin.buildIndiScores()

@app.route('/indi-scores-entered', methods=['POST', 'GET'])
def indiScoresEnteredPage():
    if request.method == 'POST':
        print(request.form)
        form_data = request.form
        out = admin.storeIndiScores(form_data)
        # todo reroute to scoreboard
        return redirect(url_for('scoreboardPage'))
    else:
        print("NOT A POST?")

if __name__ == '__main__':
    app.run()
