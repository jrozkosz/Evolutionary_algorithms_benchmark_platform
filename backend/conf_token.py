# project/token.py

from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_confirmation_token(app, email):
    # with app.app_context():
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(app, token, expiration=3600):
    # with app.app_context():
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    # try:
    email = serializer.loads(
        token,
        salt=app.config['SECURITY_PASSWORD_SALT'],
        max_age=expiration
    )
    # except:
    #     return False
    return email