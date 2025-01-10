
import subprocess
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from flaskr.models import Algorithm, ProposedResults, CECResults, ClassicResults, AlgorithmRunningResults
from .ranking_calculator import RankingCalculator
import subprocess

def run_microVM(alg_name, IPaddrs_significant_num: int):
    command = [
            "./microVM/launch_microVM.sh",
            f"tap{IPaddrs_significant_num}",
            f"/tmp/firecracker{IPaddrs_significant_num}.socket",
            f"172.16.{IPaddrs_significant_num}.2",
            f"172.16.{IPaddrs_significant_num}.1",
            "microVM/ubuntu-22.04.id_rsa",
            f"{alg_name}.py",
            "CEC2022.py", 
            "algorithm_running.py",
            "ranking_config.json",
            f"{alg_name}"
        ]
        
    with open("logs.txt", "w") as log_file:
        result = subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)
    
    try:
        engine = create_engine(f'mysql+pymysql://{os.environ["MYSQL_USER"]}:{os.environ["MYSQL_PASSWORD"]}@localhost:{os.environ["MYSQL_PORT"]}/{os.environ["MYSQL_DB_NAME"]}', echo=True)
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

def reboot_microVM(microVM_IP_addr):
    subprocess.run(["ssh", "-i", "microVM/ubuntu-22.04.id_rsa", 
                    "-o", "StrictHostKeyChecking=no", 
                    f"root@{microVM_IP_addr}", "reboot"])


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
    
    os.remove(f'running_files/running_results_{currentAlgorithm.name}.json')
    os.remove(f'running_files/progress_file_{currentAlgorithm.name}.txt')
    os.remove(f'running_files/running_logs_{currentAlgorithm.name}.txt')
    
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