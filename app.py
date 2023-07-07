import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import urllib.request, json
from functools import wraps

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///final.db")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Select games and display the users game shelf
@app.route("/")
@login_required
def index():
    games = db.execute("SELECT game_name, notes, rating FROM shelves WHERE user_id = ?", session["user_id"])
    data_list = [{'game_name': game["game_name"],
                  'notes': game["notes"],
                  'rating': game["rating"]}
                        for game in games]
    return render_template("index.html", games = data_list)


@app.route("/add_games", methods=["GET", "POST"])
@login_required
def add__games():

    if request.method == "POST":
        # Check that a game title has been entered - other fields are optional
        if not request.form.get("name"):
            return apology("You must enter a name for the game.", 400)
        else:
            gname = request.form.get("name")
            genre = request.form.get("genre")
            db.execute("INSERT INTO games (name, genre) VALUES (?, ?) ", gname, genre)

            notes = request.form.get("notes")
            rating = request.form.get("rating")
            db.execute("INSERT INTO shelves (user_id, game_name, notes, rating) VALUES (?, ?, ?, ?)", session["user_id"], gname, notes, rating)
            
            return redirect("/")

    else:
        return render_template("add_games.html")



def apology(message, code=400):   
    # Show an apology to the user with an error message and code
    return render_template("apology.html", code=code, message=message)


@app.route("/change_pass", methods=["GET", "POST"])
@login_required
def change_pass():

    # Require a user to enter their old password and ensure the new password is confirmed
    if request.method == "POST":
        if not (password := request.form.get("password")):
            return apology("Please enter your old password")

        rows = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])

        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Password incorrect")

        if not (new_password := request.form.get("new_password")):
            return apology("Please enter new password")

        if not (confirmation := request.form.get("confirmation")):
            return apology("Please confirm your new password")

        if new_password != confirmation:
            return apology("Passwords do not match")

        db.execute("UPDATE users set hash = ? WHERE id = ?;",
                   generate_password_hash(new_password), session["user_id"])

        flash("Password reset successful!")

        return redirect("/")
    else:
        return render_template("change_pass.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("You must provide a username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("You must provide a password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    # If method is post then the user has entered data (registered an account)
    if request.method == "POST":

        rows = db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("You must provide a username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("You must provide a password", 400)

        # Ensure password was validaated
        elif not request.form.get("confirmation"):
            return apology("You must retype your password", 400)

        # Check to see if their chosen username is already in use
        elif len(rows) >= 1:
            return apology("Username taken", 400)

        # Check that the passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords must match", 400)

        # Username is available and passwords match

        # Hash the password and insert data into db
        else:
            username = request.form.get("username")
            user_pass = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, user_pass)
            user_id = db.execute("SELECT id FROM users WHERE username = ?", username)
            session["user_id"] = user_id[0]["id"]

            # Redirect user to home page
            return redirect("/")

    else:
        return render_template("register.html")


@app.route("/remove_games", methods=["GET", "POST"])
@login_required
def remove_games():

    # Select the games from the users shelf to be removed
    games = db.execute("SELECT game_name, notes, rating FROM shelves WHERE user_id = ?", session["user_id"])
    data_list = [{'game_name': game["game_name"]}
                            for game in games]

    if request.method == "POST":

        # Check that all fields have data
        if not request.form.get("game"):
            return apology("Please select a game to remove.", 403)
        else:
            rgame = request.form.get("game")
            db.execute("DELETE FROM shelves WHERE user_id = ? AND game_name = ?", session["user_id"], rgame)
            return redirect("/")
        
    else:    
        return render_template("remove_games.html", games = data_list)


@app.route("/wishlist")
@login_required
def wishlist():
    # Select games from the users wishlist to display
    games = db.execute("SELECT name, platform FROM wishlist WHERE user_id = ?", session["user_id"])
    data_list = [{'name': game["name"],
                'platform': game["platform"]}
                        for game in games]
    return render_template("wishlist.html", games = data_list)



@app.route("/wishlist_add", methods=["GET", "POST"])
@login_required 
def wishlist_add():
    if request.method == "POST":

        # Check that a game title has been entered - other fields are optional
        if not request.form.get("name"):
            return apology("You must enter a name for the game.", 400)

        else:
            gname = request.form.get("name")
            platform = request.form.get("platform")
            db.execute("INSERT INTO wishlist (name, platform, user_id) VALUES (?, ?, ?) ", gname, platform, session["user_id"])
            return redirect("/wishlist")

    else:
        return render_template("wishlist_add.html")


@app.route("/wishlist_remove", methods=["GET", "POST"])
@login_required
def wishlist_remove():

    # Display options from the users wishlist as options for removal
    games = db.execute("SELECT name FROM wishlist WHERE user_id = ?", session["user_id"])
    data_list = [{'name': game["name"]}
                            for game in games]

    if request.method == "POST":

        # Check that all fields have data
        if not request.form.get("game"):
            return apology("Please select a game to remove.", 403)
        else:
            rgame = request.form.get("game")
            db.execute("DELETE FROM wishlist WHERE user_id = ? AND name = ?", session["user_id"], rgame)
            return redirect("/wishlist")
        
    else:    
        return render_template("wishlist_remove.html", games = data_list)
    

