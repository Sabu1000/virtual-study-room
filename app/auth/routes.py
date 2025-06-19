from flask import render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from app.models import User
from app.extensions import db
from . import auth_bp
from .forms import RegisterForm, LoginForm, PasswordResetRequestForm, ForgotPasswordForm, ResetPasswordForm
from flask_login import current_user  
from flask_mail import Message
from app.extensions import mail
from app.auth.email_utils import send_reset_email
from app.utils.token import verify_reset_token


@auth_bp.route('/register', methods=['GET', 'POST']) # get shows the form. post processes the submitted form data
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first() # check if a user with the same email already exists in the database
        if existing_user:
            flash("An account with this email already exists.", "danger")
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password
        )

        db.session.add(new_user)
        db.session.commit() # save the change
        login_user(new_user) # built in function to store user ID in session

        flash("Registration successful! You are now logged in.", "success")
        return redirect(url_for('main.home'))
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash("Login successful", "success")
            return redirect(url_for('main.home'))
        else:
            flash("Invalid email or password", "danger")
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('If your email is registered, a reset link has been sent.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html', form=form)

@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = generate_reset_token(user.email)
            reset_url = url_for('auth.reset_token', token=token, _external=True)
            msg = Message('Password Reset Request',recipients=[user.email])
            msg.body = f'''To reset your password, visit the following link{reset_url}'''
            mail.send(msg)
        flash('If your email is in our system, a password reset link has been sent.', 'info')
        
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_request.html', form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    email = verify_reset_token(token)
    if not email:
        flash('That is an invalid or expired token.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    user = User.query.filter_by(email=email).first_or_404()
    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password_hash = hashed_password
        db.session.commit()
        flash('Your password has been updated. You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)
