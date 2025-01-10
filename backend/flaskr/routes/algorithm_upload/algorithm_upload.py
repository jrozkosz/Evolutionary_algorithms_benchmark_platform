from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
import os
import multiprocessing
from flaskr.models import db, Algorithm, ProposedResults, CECResults, ClassicResults, AlgorithmRunningResults, User, export_json_cec_data
from .microVM_launch import run_microVM, reboot_microVM
import threading

bp = Blueprint('algorithm', __name__, url_prefix='/algorithm')

@bp.route("/algorithms_rankings", methods=["GET"])
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


@bp.route("/upload/progress", methods=["GET"])
def display_progress():
    try:  
        user_id = session.get("user_id")
        
        response = {'algorithms': []}
        
        algorithms = Algorithm.query.filter_by(user_id=user_id).all()
        
        for algorithm in algorithms:
            if algorithm.error_occurred:
                response['algorithms'].append({'id': algorithm.id, 'name': algorithm.name, 'error': algorithm.error_occurred, 'progress': 0})
            if algorithm.finished:
                response['algorithms'].append({'id': algorithm.id, 'name': algorithm.name, 'error': algorithm.error_occurred, 'progress': 100})
            elif algorithm.running:
                try:
                    with open(f'running_files/progress_file_{algorithm.name}.txt', 'r') as f:
                        progress = float(f.read())
                        algorithm.running_progress = progress
                        db.session.commit()
                        response['algorithms'].append({'id': algorithm.id, 'name': algorithm.name, 'error': algorithm.error_occurred, 'progress': progress}) 
                except Exception:
                    response['algorithms'].append({'id': algorithm.id, 'name': algorithm.name, 'error': algorithm.error_occurred, 'progress': 0})
                    
        return jsonify(response), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while fetching algorithms progress", "details": str(e)}), 500
        

@bp.route("/upload", methods=["POST"])
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

@bp.route("/delete_algorithm", methods=["POST"])
def delete_algorithm():
    try:
        algorithm_id = request.json["algorithm_id"]
        algorithm = Algorithm.query.filter_by(id=algorithm_id).first()

        if algorithm is None:
            return jsonify({"error": "Algorithm not found"}), 404
        
        if algorithm.microVM_IP_addr:
            thread = threading.Thread(target=reboot_microVM, args=(algorithm.microVM_IP_addr,))
            thread.start()

        if os.path.exists(f'running_files/running_results_{algorithm.name}.json'):
            os.remove(f'running_files/running_results_{algorithm.name}.json')
        if os.path.exists(f'running_files/progress_file_{algorithm.name}.txt'):
            os.remove(f'running_files/progress_file_{algorithm.name}.txt')
        if os.path.exists(f'running_files/running_logs_{algorithm.name}.txt'):
            os.remove(f'running_files/running_logs_{algorithm.name}.txt')

        if algorithm.cec_results_id is not None:
            cec_results = CECResults.query.filter_by(id=algorithm.cec_results_id).first()
            db.session.delete(cec_results)
        if algorithm.proposed_results_id is not None:
            proposed_results = ProposedResults.query.filter_by(id=algorithm.proposed_results_id).first()
            db.session.delete(proposed_results)
        if algorithm.classic_results_id is not None:
            classic_results = ClassicResults.query.filter_by(id=algorithm.classic_results_id).first()
            db.session.delete(classic_results)
        alg_running_results = AlgorithmRunningResults.query.filter_by(algorithm_id=algorithm_id).first()
        if alg_running_results is not None:
            db.session.delete(alg_running_results)
        
        db.session.delete(algorithm)
        db.session.commit()
        
        return jsonify({"message": "Successfully deleted algorithm."}), 200

    except Exception as e:
        db.session.rollback()
        print("\n\n\n ERROR DETAILS: ", str(e), "\n\n\n")
        return jsonify({"error": "An error occurred while deleting algorithm.", "details": str(e)}), 500