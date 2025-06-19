from flask import render_template
from flask_login import login_required, current_user
from . import main_bp

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return f"Welcome, {current_user.username}! You are logged in."
