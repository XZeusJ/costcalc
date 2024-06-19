from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from costcalc.extensions import db
from costcalc.models import User
from costcalc.forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('products.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.validate_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('products.index'))
    return render_template('auth/login.html', title='Sign In', form=form)


@auth_bp.route('/guest_login')
def guest_login():
    guest_user = User.query.filter_by(username='guest').first()
    login_user(guest_user)
    return redirect(url_for('products.index'))

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('products.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)  # 自动登录用户
        flash('Congratulations, you are now a registered user and logged in!', 'success')
        return redirect(url_for('products.index'))  # 重定向到目标页面
    return render_template('auth/register.html', title='Register', form=form)
