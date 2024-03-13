from dotenv import load_dotenv
import os
import redis

load_dotenv()

class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://jakub_rozkosz:!Jakub01@localhost:3306/alg_ranking_db'

    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True # jezeli nie wykorzystuje secret_key to to dać na false
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")

    # CORS_HEADERS = 'Content-Type'