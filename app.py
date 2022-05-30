import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Add the user's entry into the database
        # we take the input values and sanitize them a bit
        name = request.form.get("name").capitalize()
        day = int(request.form.get("day"))
        month = int(request.form.get("month"))

        # save the values in the database if they are ok
        if day > 0 and day < 32 and month > 0 and month < 13 and len(name) > 0 and name.isalpha():
            db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)

        return redirect("/")

    else:

        # Display the entries in the database on index.html
        # we select the people's data from the database
        people = db.execute("SELECT id, name, month, day FROM birthdays")

        # we render the template using the selected data
        return render_template("index.html", people=people)


@app.route("/delete", methods=["POST"])
def delete():
    id = request.form.get("id")
    db.execute("DELETE FROM birthdays WHERE id = ?", id)

    return redirect("/")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # save the edited birthday into the database
        id = request.form.get("id")
        name = request.form.get("name").capitalize()
        day = int(request.form.get("day"))
        month = int(request.form.get("month"))

        if day > 0 and day < 32 and month > 0 and month < 13 and len(name) > 0 and name.isalpha():
            db.execute("UPDATE birthdays SET name = ?, day = ?, month = ? WHERE id = ?", name, day, month, id)
            return redirect("/")

    else:
        # display the form to edit the birthday
        id = request.args.get("id")
        people = db.execute("SELECT id, name, month, day FROM birthdays WHERE id = ?", id)

        return render_template("edit.html", people=people)


