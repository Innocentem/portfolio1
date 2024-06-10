from functools import wraps
from flask import redirect, url_for, session

def login_required(f):
    """
    Decorator to ensure a user is logged in before accessing a route.
    
    This decorator wraps the given function and checks if the 'user_id' is present 
    in the session. If not, it redirects the user to the login page.
    
    :param f: The function to be wrapped.
    :return: The wrapped function or a redirect to the login page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in by verifying the 'user_id' in the session
        if 'user_id' not in session:
            # Redirect to the login page if the user is not logged in
            return redirect(url_for('auth.login'))
        # Proceed with the original function if the user is logged in
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator to ensure a user is an admin before accessing a route.
    
    This decorator wraps the given function and checks if the 'is_admin' flag is present 
    and true in the session. If not, it redirects the user to the home page.
    
    :param f: The function to be wrapped.
    :return: The wrapped function or a redirect to the home page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is an admin by verifying the 'is_admin' flag in the session
        if 'is_admin' not in session or not session['is_admin']:
            # Redirect to the home page if the user is not an admin
            return redirect(url_for('main.home'))
        # Proceed with the original function if the user is an admin
        return f(*args, **kwargs)
    return decorated_function
