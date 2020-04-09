import os
import sqlite3
from app.dbmodels import Users
from app import app, db, login_manager
from app.forms import LoginForm, RegistrationForm
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for, render_template, request, session, flash

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return Users.query.get(user_id)
    return None

@app.route('/')
def index():
    if current_user.is_authenticated:
        username = session['Username']
        return redirect(url_for('auth_index'))
    else:
        return redirect(url_for('login'))

@app.route('/index')
def auth_index():
    return redirect(url_for('login'))

@app.route('/login', methods=['Get', 'Post'])
def login():

    form = LoginForm(request.form)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user:
            if user.check_password(password=password):
                login_user(user)
                session['Username'] = user.username
                session['Email'] = user.email
                next = request.args.get('next')
                return 'Logged In', 200
            else:
                return "Invalid Password", 404
        else:
            return 'Username Does Not Exist', 404
    return render_template('login.html', form=form)

@app.route('/signup', methods=['Get', 'Post'])
def signup():
    reg_form = RegistrationForm(request.form)
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_conf = request.form['password_conf']
        existing_user = Users.query.filter_by(username=username).first()
        existing_email = Users.query.filter_by(email=email).first()
        if existing_user is None:
            if existing_email is None:
                user = Users(username, email, generate_password_hash(password, 'sha256'))
                db.session.add(user)
                db.session.commit()
                db.create_all()
                return 'Account Created', 200
            else:
                return 'A User Already Exists With That Email Address', 404
        else:
            return 'A User Already Exists With That Username', 404
    else:
        return render_template('signup.html', reg_form=reg_form)

@app.route("/favicon.ico")
def favicon():
    return ""