from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

# Create a Blueprint for authentication
bp = Blueprint('auth', __name__)

# Register function for user registrationg
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Create a RegisterForm instance
    register = RegisterForm()
    
    if register.validate_on_submit() == True:
        uname = register.user_name.data
        pwd = register.password.data
        email = register.email_id.data
        
        # Check if the username already exists
        user = db.session.scalar(db.select(User).where(User.name == uname))
        if user:
            flash('User name already exists, please login')
            return redirect(url_for('auth.login'))
        
        # Generate a password hash
        pwd_hash = generate_password_hash(pwd)
        
        # Create a new user and add them to the database
        new_user = User(name=uname, password_hash=pwd_hash, emailid=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        return render_template('user.html', form=register, heading='Register')

# Login function
@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit() == True:
        user_name = login_form.user_name.data
        password = login_form.password.data
        
        # Query the user by their username
        user = db.session.scalar(db.select(User).where(User.name == user_name))
        if user is None:
            error = "Incorrect user name"
        elif not check_password_hash(user.password_hash, password):
            error = "Incorrect password"
        if error is None:
            # Log in the user
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

# Logout function
@bp.route('/logout')
@login_required
def logout():
    # Log the user out
    logout_user()
    # return 'You have been logged out'
    return render_template('logout.html', heading='Loginout')
