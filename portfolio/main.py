from flask import Blueprint, render_template, url_for, session, redirect, request, flash
from werkzeug.utils import secure_filename
import os
from .models import db, Item
from .decorators import login_required

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
