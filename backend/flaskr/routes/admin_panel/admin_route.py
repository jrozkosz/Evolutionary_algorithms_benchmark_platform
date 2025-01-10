from flask import (
    Blueprint, request, jsonify
)
from flaskr.models import db, Algorithm, AlgorithmRunningResults, User, CECResults, ProposedResults, ClassicResults
import os
from sqlalchemy import desc

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route("/display_users", methods=["GET"])
def display_users():
    try:
        users = User.query.all()
        users_array = []
        latest_run_percent = 0
        if users:
            for user in users:
                if user.is_confirmed:
                    algorithms = Algorithm.query.filter_by(user_id=user.id).order_by(desc(Algorithm.added_date)).all()
                    if algorithms:
                        latest_run_percent = algorithms[0].running_progress
                    for algorithm in algorithms:
                        if os.path.isfile(f'running_files/progress_file_{algorithm.name}.txt'):
                            with open(f'running_files/progress_file_{algorithm.name}.txt', 'r') as f:
                                progress = float(f.read())
                                algorithm.running_progress = progress
                                db.session.commit()

                    users_array.append({
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "algorithms_sent": len(algorithms),
                        "running_progress": latest_run_percent
                    })
        
        return jsonify({"users": users_array}), 200

    except Exception as e:
        print("\n\nERROR details", str(e))
        return jsonify({"error": "An error occurred while fetching users", "details": str(e)}), 500


@bp.route("/delete_user", methods=["POST"])
def delete_user():
    try:
        user_id = request.json["user_id"]
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404

        Algorithm.query.filter_by(user_id=user_id).delete()

        User.query.filter_by(id=user_id).delete()
        
        AlgorithmRunningResults.query.filter_by(user_id=user_id).delete()

        db.session.commit()
        return jsonify({"message": "Successfully deleted user"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting user", "details": str(e)}), 500