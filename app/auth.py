from flask import Blueprint, flash
from flask import Flask, render_template, redirect, request, url_for, request
from app import db
from app import Session
from werkzeug.urls import url_parse
from app.models import User
from .forms import LoginForm
from flask_login import current_user, login_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        username = current_user.username
        return redirect(url_for('client', client_id = str(username)))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный пароль или логин')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        username = current_user.username
        print(username)


        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('client', client_id = str(username))
        return redirect(next_page)
    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('hello'))