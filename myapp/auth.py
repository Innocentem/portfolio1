from werkzeug.utils import secure_filename
import os
from flask import current_app
from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        image = request.files.get('image')

        # Debugging output to check form data
        print(f"Name: {name}, Email: {email}, Password: {password}, Image: {image}")

        if not name or not email or not password or not image:
            return "Please fill out all fields and upload an image."

        user = User.query.filter_by(email=email).first()
        if user:
            return "Email address already exists"

        filename = secure_filename(image.filename)
        filepath = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        image.save(filepath)

        try:
            new_user = User(
                email=email,
                name=name,
                password=generate_password_hash(password, method='pbkdf2:sha256'),
                image_url=filename  # Save image filename to user
            )
            db.session.add(new_user)
            db.session.commit()

            # Log in the user by setting the session
            session['user_id'] = new_user.id

            return redirect(url_for('main.in_user'))  # Redirect to profile page
        except Exception as e:
            print(f"Error creating new user: {e}")
            return "An error occurred while creating a new user."

    return render_template('signup.html')


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Debugging output to check form data
        print(f"Email: {email}, Password: {password}")

        user = User.query.filter_by(email=email).first()
        print(f"User found: {user}")

        if not user or not check_password_hash(user.password, password):
            return "Invalid credentials"

        session['user_id'] = user.id
        return redirect(url_for('main.user'))  # Redirect to main.index after successful login
    return render_template("login.html")

@auth.route('/signout', methods=["GET"])
def signout():
    session.pop('user_id', None)  # Clear user session
    return redirect(url_for('main.home'))  # Redirect to the main page or wherever you want after signout
