# project/email.py

from flask_mail import Message
from flask import render_template, url_for, current_app
from conf_token import generate_confirmation_token

def send_email(app, mail, to, subject, template):
    # with app.app_context():
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

def send_confirmation_email(app, mail, user_email, frontend_url):
    try:
        # with app.app_context():
        token = generate_confirmation_token(app, user_email)
        # confirm_url = url_for('confirm_email', token=token, _external=True)
        confirm_url = f"{frontend_url}/confirm/{token}"
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(app, mail, user_email, subject, html)
    except:
        return False    
    return True