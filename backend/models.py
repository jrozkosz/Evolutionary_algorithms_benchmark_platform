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
    admin_id = db.Column(db.String(32), nullable=False)
    text = db.Column(LONGTEXT, nullable=False)
    added_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    is_crucial = db.Column(db.Boolean, default=False, nullable=False)

class Algorithm(db.Model):
    __tablename__ = "algorithms"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    # name = db.Column(db.String(345), unique=True, nullable=False)
    # username = db.Column(db.String(345), unique=True, nullable=False)
    user_id = db.Column(db.String(32), unique=True, nullable=False)
    running = db.Column(db.Boolean, nullable=False, default=False)
    finished = db.Column(db.Boolean, nullable=False, default=False)
    error_occurred = db.Column(db.Boolean, nullable=False, default=False)
    running_progress = db.Column(db.Float, default=0.0)
    microVM_IP_addr = db.Column(db.String(15), nullable=True)
    
    cec_results_id = db.Column(db.String(32))
    proposed_results_id = db.Column(db.String(32))
    classic_results_id = db.Column(db.String(32))

class CECResults(db.Model):
    __tablename__ = "cec_results"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    score = db.Column(db.Float, nullable=True)

class ProposedResults(db.Model):
    __tablename__ = "proposed_results"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    score = db.Column(db.Float, nullable=True)
    optimum_factor = db.Column(db.Float, nullable=True)
    thresholds_factor = db.Column(db.Float, nullable=True)
    budget_factor = db.Column(db.Float, nullable=True)

class ClassicResults(db.Model):
    __tablename__ = "classic_results"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    average = db.Column(db.Float, nullable=True)
    median = db.Column(db.Float, nullable=True)
    std_dev = db.Column(db.Float, nullable=True)
    best_one = db.Column(db.Float, nullable=True)
    worst_one = db.Column(db.Float, nullable=True)

class AlgorithmRunningResults(db.Model):
    __tablename__ = "algorithm_running_results"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    algorithm_id = db.Column(db.String(32), unique=True, nullable=False)
    json_data = db.Column(db.JSON, nullable=False)
    
    
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