from flask import Flask, request, abort, jsonify, session, Response, make_response
from flask_bcrypt import Bcrypt
from models import db, Migrate, User, Algorithm, export_json_cec_data, AlgorithmRunningResults, WallInformation, CECResults, ProposedResults, ClassicResults
from ranking_calculator import RankingCalculator
from config import ApplicationConfig
from flask_session import Session
from flask_cors import CORS, cross_origin
from conf_token import confirm_token
from conf_email import send_confirmation_email
from flask_mail import Mail
import subprocess
import multiprocessing
import os
from uuid import uuid4
import json
import pymysql
from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': "http://localhost:3000"}}, supports_credentials=True) 
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
server_session = Session(app)
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    # db.drop_all()
    db.create_all()
    
    admin_exists = User.query.filter_by(username='admin').first() is not None
    if not admin_exists:
        hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
        user = User(username='admin', email='admin', password=hashed_password, is_confirmed=True, is_admin=True)
        db.session.add(user)
        db.session.commit()

mail = Mail(app)

@app.route("/@me")
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


@app.route("/register", methods=["POST", "GET"])
def register_user():
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

    send_confirmation_email(app, mail, email, "http://localhost:3000")
    return jsonify({"info": "confirm email"})


@app.route("/confirm/<token>", methods=["POST"])
def confirm_email(token):
    try:
        email = confirm_token(app, token)
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
        return jsonify({"info": "You have confirmed your account. Thanks!"})


@app.route("/login", methods=["POST"])
def login_user():
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
    return response

@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"


def run_microVM(alg_name, IPaddrs_significant_num: int):
    command = [
            "./launch_microVM.sh",
            f"tap{IPaddrs_significant_num}",
            f"/tmp/firecracker{IPaddrs_significant_num}.socket",
            f"172.16.{IPaddrs_significant_num}.2",
            f"172.16.{IPaddrs_significant_num}.1",
            "./ubuntu-22.04.id_rsa",
            f"{alg_name}.py",
            "CEC2022.py", 
            "algorithm_running.py",
            f"{alg_name}"
        ]
        
    with open("logs.txt", "w") as log_file:
        result = subprocess.run(command, cwd="microVM", stdout=log_file, stderr=subprocess.STDOUT)
    
    try:
        engine = create_engine("mysql+pymysql://root:!Mysql2001@localhost:3306/alg_ranking_db", echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        if result.returncode == 0:
            currentAlgorithm = session.query(Algorithm).filter_by(name=alg_name).first()
            currentAlgorithm.running = False
            currentAlgorithm.finished = True
            session.commit()

            algorithmRunningResults = update_algorithm_running_results(currentAlgorithm, session)
            
            # CALCULATE RANKINGS
            calculate_rankings(algorithmRunningResults, currentAlgorithm, session)
        else:
            currentAlgorithm = session.query(Algorithm).filter_by(name=alg_name).first()
            currentAlgorithm.error_occurred = True
            currentAlgorithm.running = False
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()
        engine.dispose()


def update_algorithm_running_results(currentAlgorithm, session):
    with open(f'running_files/running_results_{currentAlgorithm.name}.json', 'r') as file:
        json_data = json.load(file)

    algRunningResults = AlgorithmRunningResults(algorithm_id=currentAlgorithm.id, user_id=currentAlgorithm.user_id,
                                                json_data=json_data)
    session.add(algRunningResults)
    session.commit()
    
    with open(f'running_files/progress_file_{currentAlgorithm.name}.txt', 'r') as f:
        progress = float(f.read())
        currentAlgorithm.running_progress = progress
        session.commit()
    
    # os.remove(f'running_files/running_results_{currentAlgorithm.name}.json')
    # os.remove(f'running_files/progress_file_{currentAlgorithm.name}.txt')
    # os.remove(f'running_files/running_logs_{currentAlgorithm.name}.txt')
    
    return algRunningResults

def calculate_rankings(runningResults, currentAlgorithm, session):
    # cec
    algRunningResults = session.query(AlgorithmRunningResults).all()
    all_data = {}
    for algorithm in algRunningResults:
        all_data.update({f"{algorithm.algorithm_id}": algorithm.json_data})
    rankingCalc = RankingCalculator()
    
    cec_score = rankingCalc.cec_ranking_method(all_data) # dict
    for alg in cec_score:
        alg_to_update = session.query(Algorithm).filter_by(id=alg).first()
        if alg_to_update.cec_results_id not in (None, ''):
            results_to_update = session.query(CECResults).filter_by(id=alg_to_update.cec_results_id).first()
            results_to_update.score = cec_score[alg]
        else:
            results_to_update = CECResults(score=cec_score[alg])
            session.add(results_to_update)
            session.commit()
            alg_to_update.cec_results_id = results_to_update.id
            session.commit()
    
    # proposed
    proposed_score = rankingCalc.proposed_ranking_method(runningResults.json_data) # dict
    proposed_results = ProposedResults(score=proposed_score['final_score'], optimum_factor=proposed_score['optimum'],
                                       thresholds_factor = proposed_score['threshold'], budget_factor=proposed_score['budget'])
    session.add(proposed_results)
    session.commit()
    currentAlgorithm.proposed_results_id = proposed_results.id
    session.commit()
    
    # classic
    average_error, median_error, std_dev_error, best_error, worst_error = rankingCalc.classic_ranking_method(runningResults.json_data)
    classic_results = ClassicResults(average=average_error, median=median_error, std_dev=std_dev_error, 
                                      best_one=best_error, worst_one=worst_error)
    session.add(classic_results)
    session.commit()
    currentAlgorithm.classic_results_id = classic_results.id
    session.commit()

@app.route("/algorithms_rankings", methods=["GET"])
def display_rankings():    
    algRunningResults = AlgorithmRunningResults.query.all()
    
    data = {'cec_ranking': [], 'proposed_ranking': [], 'classic_ranking': []}
    
    finished_algorithms = Algorithm.query.filter_by(finished=True).all()
    if finished_algorithms is not None:
        for algorithm in finished_algorithms:
            user = User.query.filter_by(id=algorithm.user_id).first()
            cec_results = CECResults.query.filter_by(id=algorithm.cec_results_id).first()
            proposed_results = ProposedResults.query.filter_by(id=algorithm.proposed_results_id).first()
            classic_results = ClassicResults.query.filter_by(id=algorithm.classic_results_id).first()
            data['cec_ranking'].append({'username': user.username, 'algorithm': algorithm.name, 'score': cec_results.score})
            data['proposed_ranking'].append({'username': user.username, 'algorithm': algorithm.name, 'score': proposed_results.score, 'optimum': proposed_results.optimum_factor, 
                                            'threshold': proposed_results.thresholds_factor, 'budget': proposed_results.budget_factor})
            data['classic_ranking'].append({'username': user.username, 'algorithm': algorithm.name, 'average': classic_results.average, 'median': classic_results.median,
                                            'std_dev': classic_results.std_dev, 'best': classic_results.best_one, 'worst': classic_results.worst_one})

        data['cec_ranking'].sort(key=lambda x: x['score'], reverse=True)
        data['proposed_ranking'].sort(key=lambda x: x['score'], reverse=True)
        data['classic_ranking'].sort(key=lambda x: x['average'])
    
    return jsonify(data), 200



@app.route("/upload/progress", methods=["GET"])
def display_progress():
    try:  
        user_id = session.get("user_id")
        algorithm = Algorithm.query.filter_by(user_id=user_id).first()
        if algorithm is not None:
            if algorithm.error_occurred:
                return jsonify({'error': "An error occurred when processing the algorithm"}), 400
            if algorithm.finished:
                return jsonify({'progress': 100})
            elif algorithm.running:
                # microVM_IP_addr = algorithm.microVM_IP_addr
                
                # subprocess.run(["scp", "-i", "/microVM/ubuntu-22.04.id_rsa", "-o", "StrictHostKeyChecking=no", f"root@{microVM_IP_addr}:/root/progress_file.txt", "."]) 
                try:
                    with open(f'running_files/progress_file_{algorithm.name}.txt', 'r') as f:
                        progress = float(f.read())
                        algorithm.running_progress = progress
                        db.session.commit()
                        return jsonify({"progress": progress}), 200
                except Exception:
                    return jsonify({"progress": 0}), 200
            
        return jsonify({"error": "Algorithm has not yet been uploaded"}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting user", "details": str(e)}), 500
        

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return 'No file in a request', 400

    file = request.files['file']
    if file.filename == '':
        return 'Empty file name', 400

    try:
        runningAlgorithms = Algorithm.query.filter_by(running=True).all()
        if len(runningAlgorithms) > 0:
            IPaddrs_being_used = [algorithm.microVM_IP_addr for algorithm in runningAlgorithms]
            IPaddrs_being_used.sort()
            IPaddrs_significant_num = int(IPaddrs_being_used[-1].split('.')[-2]) + 1
        else:
            IPaddrs_significant_num = 1      
        
        algorithms_uploaded = Algorithm.query.all()
        user_id = session.get("user_id")
        algorithm_name = f"{file.filename[:-3]}_{len(algorithms_uploaded)+1}"
        file.save(f"microVM/{algorithm_name}.py")
        
        if not os.path.exists('running_files'):
            os.makedirs('running_files')
        export_json_cec_data(f'running_files/running_results_{algorithm_name}.json')
        
        currentAlgorithm = Algorithm(user_id=user_id, name=algorithm_name, running=True, microVM_IP_addr=f"172.16.{IPaddrs_significant_num}.2")
        db.session.add(currentAlgorithm)
        db.session.commit()
        
        process = multiprocessing.Process(target=run_microVM, args=(algorithm_name, IPaddrs_significant_num,))
        process.start()
        
        return jsonify({"message": "Sandbox created successfully."}), 200
    except Exception as e:
        currentAlgorithm.running = False
        db.session.commit()
        return jsonify({"error": str(e)})


@app.route("/information", methods=["GET"])
def display_info():
    information = WallInformation.query.order_by(desc(WallInformation.is_crucial), desc(WallInformation.added_date)).all()

    texts = [
        {"id": info.id, "text": info.text, "is_crucial": info.is_crucial, "added_date": info.added_date}
        for info in information
    ]

    return jsonify({"texts": texts}), 200

@app.route("/add_info", methods=["POST"])
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


@app.route("/delete_info", methods=["POST"])
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

@app.route("/display_users", methods=["GET"])
def display_users():
    try:
        users = User.query.all()
        users_array = []
        if users:
            for user in users:
                if user.is_confirmed:
                    algorithm = Algorithm.query.filter_by(user_id=user.id).first()
                    if algorithm is not None:
                        if os.path.isfile(f'running_files/progress_file_{algorithm.name}.txt'):
                            with open(f'running_files/progress_file_{algorithm.name}.txt', 'r') as f:
                                progress = float(f.read())
                                algorithm.running_progress = progress
                                db.session.commit()
                            
                    users_array.append({
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "finished_running": algorithm.finished if algorithm else False,
                        "running_progress": algorithm.running_progress if algorithm else 0
                    })
        
        return jsonify({"users": users_array}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred while fetching users", "details": str(e)}), 500


@app.route("/delete_user", methods=["POST"])
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

    

# @cli.command("create_admin")

if __name__ == "__main__":
    app.run(debug=False)
    
