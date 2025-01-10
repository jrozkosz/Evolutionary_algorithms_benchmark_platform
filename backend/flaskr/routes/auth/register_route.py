from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flaskr.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from .conf_token import confirm_token
from .conf_email import send_confirmation_email

bp = Blueprint('auth', __name__, url_prefix='/auth')

bcrypt = Bcrypt()

@bp.route("/@me")
def get_current_user():
    print("Session in @ME: ", session)
    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({"error": "Anauthorized"}), 401
    
    user = User.query.filter_by(id=user_id).first()

    return jsonify({
        "id": user.id,
        "email": user.email,
        "is_admin": user.is_admin
    })

@bp.route("/register", methods=["POST", "GET"])
def register_user():
    try:
        username = request.json["username"]
        email = request.json["email"]
        password = request.json["password"]
        
        if username == '' or email == '' or password == '':
            return jsonify({"error": "Empty values"}), 401

        user_exists = User.query.filter_by(username=username).first() is not None
        email_exists = User.query.filter_by(email=email).first() is not None

        if user_exists or email_exists:
            return jsonify({"error": "User already exists"}), 409
        
        hashed_password = bcrypt.generate_password_hash(password=password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        send_confirmation_email(mail, email, "http://localhost:3000")
        return jsonify({"info": "confirm email"}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred while signing up a user", "details": str(e)}), 500


@bp.route("/confirm/<token>", methods=["POST"])
def confirm_email(token):
    try:
        try:
            email = confirm_token(token)
        except:
            return jsonify({"error": "The confirmation link is invalid or has expired."})
        # user = User.query.filter_by(email=email).first_or_404()
        user = User.query.filter_by(email=email).first()
        if user is None:
            return jsonify({"error": "Such user does not exist."}), 401
        
        if user.is_confirmed:
            return jsonify({"info": "Account already confirmed."})
        else:
            user.is_confirmed = True
            # user.confirmed_on = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            return jsonify({"info": "You have confirmed your account. Thanks!"}), 200
    
    except Exception as e:
        return jsonify({"error": "An error occurred while confirming a user", "details": str(e)}), 500


@bp.route("/login", methods=["POST"])
def login_user():
    try:
        email = request.json["email"]
        password = request.json["password"]
        user = User.query.filter_by(email=email).first()
        
        if user is None:
            return jsonify({"error": "Anauthorized"}), 401
        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({"error": "Anauthorized"}), 401
        if not user.is_confirmed:
            return jsonify({"error": "The account has not been confirmed."}), 403
        
        session["user_id"] = user.id
        session["username"] = user.username
        
        response = jsonify({
            "id": user.id,
            "email": user.email
        })
        return response, 200

    except Exception as e:
        return jsonify({"error": "An error occurred while sigining in a user", "details": str(e)}), 500

@bp.route("/logout", methods=["POST"])
def logout_user():
    try:
        session.pop("user_id")
        return "200"

    except Exception as e:
        return jsonify({"error": "An error occurred while confirming a user", "details": str(e)}), 500