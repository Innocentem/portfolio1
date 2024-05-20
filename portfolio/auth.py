from flask import Flask, render_template, url_for, Blueprint,request

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
       user = request.form["name", "email", "password"]
       return url_for("login")
    else:
        return render_template("signup.html")

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/<usr>")
def user(usr):
    return render_template("login.html")
