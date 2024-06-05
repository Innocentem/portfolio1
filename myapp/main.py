from flask import Blueprint, render_template, url_for, session, redirect, request, flash, current_app
from werkzeug.utils import secure_filename
import os
from .models import db, Item, User
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
@login_required
def sell():
    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        contact = request.form.get('contact')  # Add this line to retrieve contact number
        image = request.files.get('image')

        if not title or not description or not location or not contact or not image:
            flash("All fields are required!")
            return redirect(request.url)

        filename = secure_filename(image.filename)
        filepath = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        image.save(filepath)

        new_item = Item(title=title, description=description, location=location, contact=contact, image_url=filename, user_id=session['user_id'])
        db.session.add(new_item)
        db.session.commit()

        return redirect(url_for('main.user'))
    
    return render_template("sell.html")

@main.route("/buy")
@login_required
def buy():
    items = Item.query.all()  # Fetch all items from the database
    return render_template("listing.html", items=items)

@main.route("/in_user")
@login_required
def in_user():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    return render_template("profile.html", user=user)

@main.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        telegram_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        send_telegram_message(telegram_message)

        flash("Thank you for your message. We'll get back to you shortly.", "success")
        return render_template("contact.html", submitted=True)

    return render_template("contact.html", submitted=False)

@main.route("/profile")
def profile():
    return render_template("profile.html")

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
        flash(f"An error occurred while sending your message: {response.text}", "danger")
