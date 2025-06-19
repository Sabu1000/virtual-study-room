from flask import url_for, current_app
from flask_mail import Message
from app.extensions import mail 
from app.utils.token import generate_reset_token  
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
    
def send_reset_email(user):
    token = generate_reset_token(user.email)
    reset_url = url_for('auth.reset_token', token=token, _external=True)

    msg = Message(
    subject="Password Reset Request",
    sender=current_app.config['MAIL_DEFAULT_SENDER'],
    recipients=[user.email],
    body=f"""Hello {user.username},

To reset your password, click the following link:
{reset_url}

If you did not request this, simply ignore this email.

This link will expire in 1 hour.
"""
    )

    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

