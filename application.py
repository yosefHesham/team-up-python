import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, make_response, json
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///students.db")



@app.route("/",methods=["GET"])
def index():

    return render_template("index.html")


@app.route("/students", methods=["GET", "POST"])

def students():

    formSkills = request.form.get("answers[101][selections][]")
    formName =request.form.get("name")
    print(formName)

    return render_template("students.html")




@app.route("/registration", methods=["GET", "POST"])
def registration():

    if request.method == "POST":

        req = request.get_json()
        name = req["name"]
        email = req["email"]
        skills = req["skills"]
        storedSkills= ",".join(map(str, skills))

        if not  db.execute("INSERT INTO STUDENTS ('name','email','skills') Values( :name, :email, :skills)",name=name, email=email, skills=storedSkills):

            res = make_response(jsonify({"message": "This Mail is Already Registered"}),400)

        else:

            res = make_response(jsonify({"message": "JSON RECIEVED"}), 200)

        return res

    else:

        argName = request.args.get("name")
        argSkills = request.args.get("skills")
        if argName:
            student = db.execute("select * from students where name = :name", name=argName)
            skills = db.execute("select skills from students where name =:name", name=argName)
            print(skills)
            response = app.response_class(
            response=json.dumps(student,),
            status=200,
            mimetype='application/json'
            )
            return response
        elif argSkills:
            student = db.execute("select * from students where skills = :skills", skills=argSkills)
            response = app.response_class(
            response=json.dumps(student),
            status=200,
            mimetype='application/json'
            )
            return response
        else:

            return render_template("registration.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
