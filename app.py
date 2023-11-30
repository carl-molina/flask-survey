from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get('/')
def get_survey():
    """Routes user to survey_start w/ title and instructions variables"""

    title = survey.title
    instructions = survey.instructions

    return render_template(
        "survey_start.html", title=title, instructions=instructions
        )



@app.post('/begin')
def handle_form_submit():
    """
    Handles form submit from survey_start and redirects user to
    /questions/0
    """

    return redirect('/questions/0')



@app.get('/questions/0')
def handle_questions():
    """Handles questions from redirect"""
    question_0 = survey.questions[0]
    # replace the h1 with the q0's prompt
    # pass in question instance
    # 2 radio buttons -- Jinja for loop,
        # question_0.choices[0] - first choice
        # question_0.choices[1] - 2nd choice
        #["yes", "no"]
    # 
    return render_template("question.html", question=question_0)




# TODO: add user's responses from survey to go here
responses = []