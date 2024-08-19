from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT
from flask_migrate import Migrate
from uuid import uuid4
from datetime import datetime
import json, os

db = SQLAlchemy()
migrate = Migrate(db)

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    username = db.Column(db.String(345), unique=True, nullable=False)
    email = db.Column(db.String(345), unique=True, nullable=False)
    password = db.Column(db.String(345), unique=True, nullable=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

class WallInformation(db.Model):
    __tablename__ = "wall_information"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    text = db.Column(LONGTEXT, nullable=False)
    added_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    is_crucial = db.Column(db.Boolean, default=False, nullable=False)
    
# class Contest(db.Model):
#     __tablename___ = "contest"
#     id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
#     starting_date = db.Column(db.DateTime, nullable=False)
#     ending_date = db.Column(db.DateTime, nullable=False)
    

class Algorithm(db.Model):
    __tablename__ = "algorithms"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    # name = db.Column(db.String(345), unique=True, nullable=False)
    # username = db.Column(db.String(345), unique=True, nullable=False)
    user_id = db.Column(db.String(32), unique=True, nullable=False)
    running = db.Column(db.Boolean, nullable=False, default=False)
    finished = db.Column(db.Boolean, nullable=False, default=False)
    running_progress = db.Column(db.Float, default=0.0)
    microVM_IP_addr = db.Column(db.String(15), nullable=True)
    
    cec_score = db.Column(db.Float, nullable=True)
    proposed_score = db.Column(db.Float, nullable=True)
    proposed_optimum_factor = db.Column(db.Float, nullable=True)
    proposed_thresholds_factor = db.Column(db.Float, nullable=True)
    proposed_budget_factor = db.Column(db.Float, nullable=True)
    classic_score_average = db.Column(db.Float, nullable=True)
    classic_score_median = db.Column(db.Float, nullable=True)
    

class AlgorithmRunningResults(db.Model):
    __tablename__ = "AlgorithmRunningResults"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    user_id = db.Column(db.String(32), unique=True, nullable=False)
    json_data = db.Column(db.JSON, nullable=False)

class CurrentlyRunningAlgorithm(db.Model):
    __tablename__ = "currently_running_algorithms"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    algorithm_name = db.Column(db.String(345), unique=True, nullable=False)
    microVM_IP_addr = db.Column(db.String(15), nullable=False)
    
    
def export_json_cec_data(file_path):
    try:
        record = AlgorithmRunningResults.query.first()
        
        if record:
            json_data = record.json_data

            with open(file_path, 'w') as file:
                json.dump(json_data, file, indent=4)
            print(f"Data has been written to {file_path}.")
        else:
            if not os.path.isfile(file_path):
                with open(file_path, 'w') as f:
                    json.dump({}, f, indent=4)
    except Exception as e:
        print(f"An error occurred: {e}")