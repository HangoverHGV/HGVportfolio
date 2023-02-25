import os
from dotenv import load_dotenv
from flask import Blueprint, render_template, request, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

load_dotenv()


auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    context = {}
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()

        if user:
            alert = 'Emai already exists.'
        elif len(username) < 4:
            alert = 'Email must be greater that 3 characters.'
        elif len(name) < 2:
            alert = 'First name must be greater than 1 character.'
        elif password1 != password2:
            alert = 'Passwords don`t match.'
        elif len(password1) < 7:
            alert = 'Password must be at least 7 characters.'
        else:
            new_user = User(username=username, name=name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login', user=current_user))
        context = {'message': alert}
    return render_template('signup.html', user=current_user, context=context)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    context = {}
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                alert = 'Incorect password, try again.'
        else:
            alert = 'E-mail doesn`t exist!'
        context = {'message': alert}

    return render_template('login.html', user=current_user, context=context)


# --------------------Log OUT-----------------------------

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

