########################################################################################
######################          Import packages      ###################################
########################################################################################
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from main import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

@app.route('/unsubscribe', methods=['GET', 'POST']) # define login page path
def unsubscribe(): # define login page fucntion
    if request.method=='GET': # if the request is a GET we return the login page
        return render_template('unsubscribe.html')
    else: # if the request is POST the we check if the user exist and with te right password
        email = request.form.get('email')

        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user:
            flash('This email doesn\'t exist')
            return redirect(url_for('signup'))

        # if the above check passes, then we know the user has an email, delete it from the db now
        db.session.delete(user)
        db.session.commit()

        return redirect(url_for('unsubscribed'))
    

@app.route('/signup', methods=['GET', 'POST'])# we define the sign up path
def signup(): # define the sign up function
    if request.method=='GET': # If the request is GET we return the sign up page and forms
        return render_template('signup.html')
    else: # if the request is POST, then we check if the email doesn't already exist and then we save data
        email = request.form.get('email')
        name = request.form.get('name')
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('signup'))
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name) #
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('signup_success'))


"""
These are the more complex endpoints with password validation, not used in first iteration!
"""

# @auth.route('/signup', methods=['GET', 'POST'])# we define the sign up path
# def signup(): # define the sign up function
#     if request.method=='GET': # If the request is GET we return the sign up page and forms
#         return render_template('signup.html')
#     else: # if the request is POST, then we check if the email doesn't already exist and then we save data
#         email = request.form.get('email')
#         name = request.form.get('name')
#         password = request.form.get('password')
#         user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
#         if user: # if a user is found, we want to redirect back to signup page so user can try again
#             flash('Email address already exists')
#             return redirect(url_for('auth.signup'))
#         # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#         new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256')) #
#         # add the new user to the database
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('main.profile'))


# @auth.route('/logout') # define logout path
# @login_required
# def logout(): #define the logout function
#     logout_user()
#     return redirect(url_for('main.index'))


# @auth.route('/login', methods=['GET', 'POST']) # define login page path
# def login(): # define login page fucntion
#     if request.method=='GET': # if the request is a GET we return the login page
#         return render_template('login.html')
#     else: # if the request is POST the we check if the user exist and with te right password
#         email = request.form.get('email')
#         password = request.form.get('password')
#         remember = True if request.form.get('remember') else False
#         user = User.query.filter_by(email=email).first()
#         # check if the user actually exists
#         # take the user-supplied password, hash it, and compare it to the hashed password in the database
#         if not user:
#             flash('Please sign up before!')
#             return redirect(url_for('auth.signup'))
#         elif not check_password_hash(user.password, password):
#             flash('Please check your login details and try again.')
#             return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
#         # if the above check passes, then we know the user has the right credentials
#         login_user(user, remember=remember)
#         return redirect(url_for('main.profile'))