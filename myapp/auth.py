from werkzeug.utils import secure_filename
import os
from flask import current_app
from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# Define a Blueprint for the authentication routes
auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        # Retrieve form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        image = request.files.get('image')

        # Debugging output to check form data
        print(f"Name: {name}, Email: {email}, Password: {password}, Image: {image}")

        # Validate form data
        if not name or not email or not password or not image:
            return "Please fill out all fields and upload an image."

        # Check if the user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            return "Email address already exists"

        # Secure the filename and save the uploaded image
        filename = secure_filename(image.filename)
        filepath = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        image.save(filepath)

        try:
            # Create a new user
            new_user = User(
                email=email,
                name=name,
                password=generate_password_hash(password, method='pbkdf2:sha256'),
                image_url=filename,
                is_admin=False  # Set is_admin to False by default
            )
            # Add and commit the new user to the database
            db.session.add(new_user)
            db.session.commit()

            # Log in the user by setting the session
            session['user_id'] = new_user.id
            session['is_admin'] = new_user.is_admin  # Set the is_admin flag in the session

            # Redirect to the profile page
            return redirect(url_for('main.in_user'))
        except Exception as e:
            # Handle exceptions and provide feedback
            print(f"Error creating new user: {e}")
            return "An error occurred while creating a new user."

    # Render the signup template for GET requests
    return render_template('signup.html')

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Retrieve form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Debugging output to check form data
        print(f"Email: {email}, Password: {password}")

        # Query the user by email
        user = User.query.filter_by(email=email).first()
        print(f"User found: {user}")

        # Validate user credentials
        if not user or not check_password_hash(user.password, password):
            return "Invalid credentials"

        # Log in the user by setting the session
        session['user_id'] = user.id
        session['is_admin'] = user.is_admin  # Set the is_admin flag in the session

        # Redirect to the main.index after successful login
        return redirect(url_for('main.in_user'))
    
    # Render the login template for GET requests
    return render_template("login.html")

@auth.route('/signout', methods=["GET"])
def signout():
    # Clear user session
    session.pop('user_id', None)
    session.pop('is_admin', None)  # Clear the is_admin flag in the session

    # Redirect to the main page or wherever you want after signout
    return redirect(url_for('main.home'))
