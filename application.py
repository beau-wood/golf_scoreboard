from flask import Flask, render_template, request, redirect, url_for
import scoreboard
import score_form

application = app = Flask(__name__)


@app.route('/')
def scoreboardPage():  # put application's code here
    return scoreboard.buildHTML()

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

if __name__ == '__main__':
    app.run()
