from flask import Blueprint, render_template, url_for, session, redirect, request, flash, current_app
from werkzeug.utils import secure_filename
import os
from .models import db, Item
from .decorators import login_required
import requests

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/user")
def user():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template("u_inside.html")

@main.route("/sell", methods=["GET", "POST"])
def sell():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')
        image = request.files.get('image')

        if not title or not description or not image:
            flash("All fields are required!")
            return redirect(request.url)

        filename = secure_filename(image.filename)
        filepath = os.path.join('static/uploads', filename)
        image.save(filepath)

        new_item = Item(title=title, description=description, image_url=filepath, user_id=session['user_id'])
        db.session.add(new_item)
        db.session.commit()

        return redirect(url_for('main.user'))
    
    return render_template("sell.html")

@main.route("/buy")
def buy():
    return "This is a buyer's page"

@main.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        telegram_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        send_telegram_message(telegram_message)

        flash("Thank you for your message. We'll reply by e-mail shortly.", "success")
        return redirect(url_for("main.contact"))

    return render_template("contact.html")

def send_telegram_message(message):
    token = current_app.config['TELEGRAM_BOT_TOKEN']
    chat_id = current_app.config['TELEGRAM_CHAT_ID']
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        flash(f"Oopsie daisie! Can't reach Telegram: {response.text}", "danger")
