from flask import Flask, render_template, request, redirect, url_for
import scoreboard
import forms

application = app = Flask(__name__)


@app.route('/')
def scoreboardPage():  # put application's code here
    return scoreboard.buildScoreboards()
@app.route('/final-matchups')
def finalMathupPage():
    return scoreboard.buildFinalMatchups()

@app.route('/enter-player-score', methods=['POST', 'GET'])
def enterPlayerScorePage():
    return forms.buildPlayerScoreForm()

@app.route('/player-scores-entered', methods=['POST', 'GET'])
def scoresEnteredPage():
    if request.method == 'POST':
        form_data = request.form
        forms.storePlayerScores(form_data)
        return redirect(url_for('scoreboardPage'))
    else:
        print("NOT A POST?")

@app.route('/enter-team-points', methods=['POST', 'GET'])
def enterTeamPointsPage():
    return forms.buildTeamPointsForm()

@app.route('/team-points-entered', methods=['POST', 'GET'])
def teamPointsEnteredPage():
    if request.method == 'POST':
        form_data = request.form
        forms.storeTeamPoints(form_data)
        return redirect(url_for('scoreboardPage'))
    else:
        print("NOT A POST?")

if __name__ == '__main__':
    app.run()