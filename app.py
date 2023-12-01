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


    session["responses"] = []

    title = survey.title
    instructions = survey.instructions

    return render_template(
        "survey_start.html",
        title=title,
        instructions=instructions
    )



@app.post('/begin')
def handle_form_submit():
    """
    Handles form submit from survey_start and redirects user to
    /questions/0
    """

    session["responses"].clear()
    print('This is session', session["responses"])

    return redirect('/questions/0')



@app.get('/questions/<int:num>')
def handle_questions(num):
    """Handles questions from redirect"""

    print('This is num', num)
    question = survey.questions[num]

    len_of_responses = len(session["responses"])
    print('This is length of responses', len_of_responses)

    if len_of_responses != num:
        print('This is num', num)
        print('This is responses', len_of_responses)
        print(f"/questions/{len_of_responses}")
        return redirect(f"/questions/{len_of_responses}")
        # NEVER FORGET TO RETURN YOUR REDIRECTS!!

    else:
        return render_template("question.html", question=question, num=num)

    # answer = bool(request.get("answer"))

    # check the session response dictionary object to see if that has that
    # question

    # number corresponds to the index of that session response list
    # if there's a value at that index, then we need to redirect them to
    # a page where there isn't an answer


    # TODO:
    # check len of response list and base the next question on how much len
    # sessions responses has in order to move to the next valid question




    # if answer:
    #     redirect(f"/questions/{num+1}")
    # else:
    # return render_template("question.html", question=question, num=num)



    # ^ get answer from page


    # if we're at a question that the previous question isn't answered yet,
    # move back to that question

    # if there isn't a question answered, it'll redirect them to the correct
    # question to answer

    # if you're at question 2, you get moved to question 3, and if the user
    # tries to go back to question 2, it says no and moves them back to question
    # 3.





@app.post('/answer/<int:num>')
def get_answer(num):
    """Gets answer from submitted form; appends answer to response list;
    redirects to either the next question or to thank you.
    """

    answer = request.form["answer"]

    # session["responses"].append(answer)
    # ^ this is a valid use of append, why NOT do this?

    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    print('This is session["responses"]', session["responses"])

    print('This is responses', responses)

    num += 1


    if num < len(survey.questions):
        return redirect(f"/questions/{num}")
    else:
        return redirect("/thanks")


@app.get("/thanks")
def thanks():
    """Redirects user to thank you page after all questions answered"""

    prompts = [question.prompt for question in survey.questions]

    responses = session["responses"]

    q_a = zip(prompts, responses)
    print('This is q_a', q_a)


    return render_template("completion.html", responses=q_a)