"""
https://medium.com/analytics-vidhya/creating-login-page-on-flask-9d20738d9f42
https://github.com/Faouzizi/Create_LoginPage

"""
########################################################################################
######################          Import packages      ###################################
########################################################################################
from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from __init__ import create_app, db
from socket import gethostname

########################################################################################
# our main blueprint
main = Blueprint('main', __name__)

@main.route('/') # home page that return 'index'
def index():
    return render_template('index.html')

@main.route('/howto') # how to page page that returns 'how_to'
def howto():
    return render_template('howto.html')

@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/unsubscribed') # profile page that return 'profile'
def unsubscribed():
    return render_template('user_deleted.html')

app = create_app() # we initialize our flask app using the __init__.py function

if __name__ == '__main__':
    db.create_all()
    if 'liveconsole' not in gethostname(): # setup for pythonanywhere
        app.run()