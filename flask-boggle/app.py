from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "verySecretSurveyKey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

boggle_game = Boggle()

# ==============================================================================
@app.before_request
def before_request():
    session.permanent = True

# Initialize the list of valid words in the session
@app.before_first_request
def before_first_request():
    session.setdefault("valid_words", [])
    session.setdefault("score", 0)

# ==============================================================================
@app.route('/')
def play_game():
    """Generates the board onscreen."""
    print("Total Number of Words:", boggle_game.total_words)
    board = boggle_game.make_board()

    if 'first_load' not in session:
        session['first_load'] = True
        print('Page loaded')
    else: 
        session.pop('first_load', None)  # Remove the session variable
        print('Page loaded successfully')
        # session['valid_words'] = []  # Empty the valid_words list
        # session['score'] = 0  # Reset the score to 0

    session["board"] = board
    score = session["score"]
    return render_template("index.html",
                           board=board,
                           score=score)
    
@app.route("/check_word")
def check_word():
    """Check to see if word is inside the dictionary.

    If the word is there, it adds points based on how many 
    letters are in that word. """

    word = request.args["word"]
    board = session["board"]
    valid_words = session["valid_words"]
    score = session["score"]
    result = boggle_game.check_valid_word(board, word)
    
    if result == "ok" and word not in valid_words:
        print(f"The length of this word is: " + str(len(word)))
        valid_words.append(word) 
    score = sum(len(word) for word in valid_words)
    print(valid_words)
    session["valid_words"] = valid_words # Update the valid_words in the session
    session["score"] = score # Update the score in the session        

    return jsonify({"Result": result, "Score": score, "UpdatedScore": True})


@app.route("/get_score")
def get_score():
    score = session.get("score", 0)
    return jsonify({"Score": score, "UpdatedScore": False})

# ==============================================================================
if __name__ == '__main__':
    app.run(debug=True)

# Need to refresh score once user has reloaded the page.