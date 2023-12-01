from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

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



@app.get('/questions/<int:num>')
def handle_questions(num):
    """Handles questions from redirect"""

    print('This is num', num)
    question = survey.questions[num]

    # Pseudocode for reference:
    # replace the h1 with the q0's prompt
    # pass in question instance
    # 2 radio buttons -- Jinja for loop,
        # question_0.choices[0] - first choice
        # question_0.choices[1] - 2nd choice
        #["yes", "no"]
    #
    return render_template("question.html", question=question, num=num)


@app.post('/answer/<int:num>')
def get_answer(num):
    """Gets answer from submitted form; appends answer to response list;
    redirects to either the next question or to thank you.
    """

    answer = request.form["answer"]

    responses.append(answer)
    print('This is responses', responses)

    num += 1

    # Pseudocode for reference:
    # check if anymore questions, if no more questions, return a redirect to
    # thank you page

    if (num < len(survey.questions)):
        return redirect(f"/questions/{num}")
    else:
        return redirect("/thanks")


@app.get("/thanks")
def thanks():
    """Redirects user to thank you page after all questions answered"""

    prompts = [question.prompt for question in survey.questions]

    q_a = zip(prompts, responses)
    print('This is q_a', q_a)


    return render_template("completion.html", responses=q_a)