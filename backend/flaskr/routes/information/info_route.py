from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flaskr.models import db, WallInformation
from sqlalchemy import desc

bp = Blueprint('info', __name__, url_prefix='/info')

@bp.route("/information", methods=["GET"])
def display_info():
    information = WallInformation.query.order_by(desc(WallInformation.is_crucial), desc(WallInformation.added_date)).all()

    texts = [
        {"id": info.id, "text": info.text, "is_crucial": info.is_crucial, "added_date": info.added_date}
        for info in information
    ]

    return jsonify({"texts": texts}), 200

@bp.route("/add_info", methods=["POST"])
def add_info():
    try:
        text = request.json["infoText"]
        if text == "":
            return jsonify({"error": "Text is empty"}), 400
        
        is_crucial = request.json["isCrucial"]
        admin_id = session.get("user_id")
        new_info = WallInformation(text=text, admin_id=admin_id, is_crucial=is_crucial)
        db.session.add(new_info)
        db.session.commit()
        
        return jsonify({"message": "Successfully added info"}), 200

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "An error occurred while adding info", "details": str(e)}), 500
    

@bp.route("/delete_info", methods=["POST"])
def delete_info():
    try:
        info_id = request.json["info_id"]
        info = WallInformation.query.filter_by(id=info_id).first()

        if info is None:
            return jsonify({"error": "Info not found"}), 404

        db.session.delete(info)
        db.session.commit()
        return jsonify({"message": "Successfully deleted info"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting info", "details": str(e)}), 500