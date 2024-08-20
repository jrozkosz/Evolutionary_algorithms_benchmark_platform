from dotenv import load_dotenv
import os
import redis

load_dotenv()

class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SECURITY_PASSWORD_SALT = 'my_precious_two'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{os.environ["MYSQL_PASSWORD"]}@localhost:3306/{os.environ["MYSQL_DB_NAME"]}'

    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True # jezeli nie wykorzystuje secret_key to to dać na false
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
    
    # mail settings
    MAIL_DEFAULT_SENDER = "ranking.app.auth@gmail.com"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = os.environ["EMAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
    # MAIL_DEFAULT_SENDER = "flaskapp@fastmail.com"
    # MAIL_SERVER = "smtp.fastmail.com"
    # MAIL_PORT = 465
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    # MAIL_DEBUG = False
    # MAIL_USERNAME = os.environ["EMAIL_USERNAME"]
    # MAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

    # CORS_HEADERS = 'Content-Type'