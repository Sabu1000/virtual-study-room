from flask import render_template, redirect, url_for, flash, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from app.models import User
from app.extensions import db
from . import auth_bp
from .forms import RegisterForm, LoginForm, PasswordResetRequestForm, ForgotPasswordForm, ResetPasswordForm, UpdatedProfileForm
from flask_login import current_user  
from flask_mail import Message
from app.extensions import mail
from app.auth.email_utils import send_reset_email
from app.utils.token import verify_reset_token, generate_reset_token
from werkzeug.utils import secure_filename
import os


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
    form = PasswordResetRequestForm()
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

@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdatedProfileForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.bio = form.bio.data

        if form.picture.data:
            picture_file = save_picture(form.picture.data) # get the path of the image
            current_user.image_file = picture_file # set current_user pfp to image path

        db.session.commit()
        flash("Your profile has been updated!", "success")
        return redirect(url_for("auth.profile"))

# check if the user is visiting the profile page, not submitting the form, and update the username and bio field
    elif request.method == "GET":
        form.username.data = current_user.username
        form.bio.data = current_user.bio
    image_url = url_for('static', filename="profile_pics/" + current_user.image_file)
    return render_template("profile.html", title="Profile", form=form, image_url=image_url, user=current_user)

# helper function to get image path
def save_picture(form_picture):
    filename = secure_filename(form_picture.filename)
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', filename)
    form_picture.save(picture_path)
    return filename
        




