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

    # old code for reference:
    # global responses
    # pulls in global variable responses
    # responses.clear()
    # print('This is responses after empty', responses)
    # ^ doesn't work for now

    title = survey.title
    instructions = survey.instructions

    # can just pass in survey obj into survery_start
    # can use survey.title and survey.instructions in survey_start.html

    return render_template(
        "survey_start.html",
        title=title,
        instructions=instructions
    )
    # ^ more professional syntax structure



@app.post('/begin')
def handle_form_submit():
    """
    Handles form submit from survey_start and redirects user to
    /questions/0
    """

    # clear out responses here
    responses.clear()

    return redirect('/questions/0')



@app.get('/questions/<int:num>')
def handle_questions(num):
# GET request should be more get-verb ie get_questions
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
# POST request should have a more post-verb ie handle_answer
    """Gets answer from submitted form; appends answer to response list;
    redirects to either the next question or to thank you.
    """

    # if num == 0:
    #     responses = []

    answer = request.form["answer"]

    responses.append(answer)
    print('This is responses', responses)

    num += 1

    # Pseudocode for reference:
    # check if anymore questions, if no more questions, return a redirect to
    # thank you page


    # check if the number is 0, then you want to assign response object
    # to equal to an empty list. If not 0, just won't reassign


    # splicing response list to whatever current question we're on if repeat
    # of question survey


    if num < len(survey.questions):
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