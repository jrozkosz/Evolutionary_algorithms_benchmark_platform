from flask import Flask
from .models import db, Migrate, User
from .config import ApplicationConfig
from flask_session import Session
from flask_cors import CORS, cross_origin
from flask_mail import Mail

from .routes.auth import register_route
from .routes.admin_panel import admin_route
from .routes.information import info_route
from .routes.algorithm_upload import upload_route
from .routes.auth.register_route import bcrypt 

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r'/*': {'origins': "http://localhost:3000"}}, supports_credentials=True) 

    if test_config is None:
        app.config.from_object(ApplicationConfig)

    bcrypt.init_app(app)
    server_session = Session(app)

    # db.init_app(app)
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()

        # admin_exists = User.query.filter_by(username='admin').first() is not None
        # if not admin_exists:
        #     hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
        #     user = User(username='admin', email='admin', password=hashed_password, is_confirmed=True, is_admin=True)
        #     db.session.add(user)
        #     db.session.commit()
    
    migrate = Migrate(app, db)
    mail = Mail(app)

    app.register_blueprint(register_route.bp)
    app.register_blueprint(admin_route.bp)
    app.register_blueprint(upload_route.bp)
    app.register_blueprint(info_route.bp)

    return app