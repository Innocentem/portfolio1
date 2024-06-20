from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
import os
from .models import db, Item, User
from .decorators import login_required, admin_required
import requests

# Define a Blueprint for the main routes
main = Blueprint('main', __name__)

@main.route("/")
def home():
    """
    Route for the homepage.
    Renders the index.html template.
    """
    return render_template("index.html")

@main.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """
    Route for selling an item. Only accessible to logged-in users.
    
    GET: Renders the sell.html template.
    POST: Handles the form submission for selling an item.
    """
    if request.method == "POST":
        # Retrieve form data
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        contact = request.form.get('contact')  # Retrieve contact number
        image = request.files.get('image')

        # Validate form data
        if not title or not description or not location or not contact or not image:
            flash("All fields are required!")
            return redirect(request.url)

        # Secure the filename and save the uploaded image
        filename = secure_filename(image.filename)
        filepath = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        image.save(filepath)

        # Create a new item and add it to the database
        new_item = Item(title=title, description=description, location=location, contact=contact, image_url=filename, user_id=session['user_id'])
        db.session.add(new_item)
        db.session.commit()

        # Redirect to the user's profile page after successfully adding the item
        return redirect(url_for('main.in_user'))
    
    # Render the sell template for GET requests
    return render_template("sell.html")

@main.route("/buy")
@login_required
def buy():
    """
    Route for viewing items available for purchase. Only accessible to logged-in users.
    
    Renders the listing.html template with all items from the database.
    """
    items = Item.query.all()  # Fetch all items from the database
    return render_template("listing.html", items=items)

@main.route("/in_user")
@login_required
def in_user():
    """
    Route for viewing the user's profile. Only accessible to logged-in users.
    
    Renders the profile.html template with the user's information and items.
    """
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    items = Item.query.filter_by(user_id=user_id).all()
    return render_template("profile.html", user=user, items=items)

@main.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Route for the contact page.
    
    GET: Renders the contact.html template.
    POST: Handles the form submission for contact messages.
    """
    if request.method == "POST":
        # Retrieve form data
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Create a message string for Telegram
        telegram_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        send_telegram_message(telegram_message)

        flash("Thank you for your message. We'll get back to you shortly.", "success")
        return render_template("contact.html", submitted=True)

    # Render the contact template for GET requests
    return render_template("contact.html", submitted=False)

def send_telegram_message(message):
    """
    Sends a message to a Telegram chat using a bot.
    
    :param message: The message to be sent.
    """
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

@main.route('/mark_sold/<int:item_id>')
def mark_sold(item_id):
    """
    Route to mark an item as sold.
    
    :param item_id: The ID of the item to be marked as sold.
    """
    item = Item.query.get_or_404(item_id)
    item.sold = True  # Update the sold attribute to True
    db.session.commit()  # Commit the changes to the database
    flash('Item marked as sold!', 'success')
    return redirect(url_for('main.home'))

@main.route("/delete_item/<int:item_id>", methods=["POST"])
@admin_required  # Ensure only administrators can access this route
def delete_item(item_id):
    """
    Route to delete an item. Only accessible to administrators.
    
    :param item_id: The ID of the item to be deleted.
    """
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Item deleted successfully!", "success")
    return redirect(url_for('main.admin'))

@main.route("/admin")
@admin_required
def admin():
    """
    Route for the admin page. Only accessible to administrators.
    
    Renders the admin.html template.
    """
    items = Item.query.all()
    return render_template("admin.html", items=items)
