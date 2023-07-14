"""
https://medium.com/analytics-vidhya/creating-login-page-on-flask-9d20738d9f42
https://github.com/Faouzizi/Create_LoginPage

"""
########################################################################################
######################          Import packages      ###################################
########################################################################################
from flask import Blueprint, render_template, redirect, url_for, request, flash, Flask
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from models import db
# from __init__ import create_app
from socket import gethostname
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import User

########################################################################################
# our main blueprint
app = Flask(__name__)
auth = Blueprint('auth', __name__) # create a Blueprint object that we name 'auth'

def create_app():
    # app = Flask(__name__) # creates the Flask instance, __name__ is the name of the current Python module
    app.config['SECRET_KEY'] = 'secret-key-goes-here' # it is used by Flask and extensions to keep data safe
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' #it is the path where the SQLite database file will be saved
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # deactivate Flask-SQLAlchemy track modifications
    db.init_app(app)
    db.app = app
    db.create_all()

    # The login manager contains the code that lets your application and Flask-Login work together
    login_manager = LoginManager() # Create a Login Manager instance
    login_manager.login_view = 'signup' # define the redirection path when login required and we attempt to access without being logged in
    login_manager.init_app(app) # configure it for login

    @login_manager.user_loader
    def load_user(user_id): #reload user object from the user ID stored in the session
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    # blueprint for auth routes in our app
    # blueprint allow you to orgnize your flask app
    app.register_blueprint(auth)
    # blueprint for non-auth parts of app
    # app.register_blueprint(main_blueprint)

# app.create_app(app)

@app.route('/') # home page that return 'index'
def index():
    return render_template('index.html')

@app.route('/howto') # how to page page that returns 'how_to'
def howto():
    return render_template('howto.html')

@app.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@app.route('/signup_success') # successful signup page
def signup_success():
    return render_template('signup_success.html')

@app.route('/unsubscribed') # profile page that return 'profile'
def unsubscribed():
    return render_template('user_deleted.html')

# app = create_app() # we initialize our flask app using the __init__.py function

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

if __name__ == '__main__':
    with app.app_context():
        create_app() # create the SQLite database
    app.run(debug=False) # debug = True if you want to run the flask app on debug mode


# if __name__ == '__main__':
#     db.create_all()
#     if 'liveconsole' not in gethostname(): # setup for pythonanywhere
#         app.run()