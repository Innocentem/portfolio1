from flask import Blueprint, render_template, url_for, session, redirect

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html")
@main.route("/user")
def user():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template("u_inside.html")

@main.route("/sell")
def sell():
    return 'This is where items to sell will go'

@main.route("/buy")
def buy():
    return "This is a buyer's page"