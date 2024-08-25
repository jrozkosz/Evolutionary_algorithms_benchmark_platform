from ranking_calculator import RankingCalculator
import json

with open('tests/algorithm_ranking/test_data_alg1.json', 'r') as f:
    test_alg1 = json.load(f)
    
with open('tests/algorithm_ranking/test_data_alg2.json', 'r') as f:
    test_alg2 = json.load(f)
    

def test_classic_ranking():
    RCalc = RankingCalculator()
    RCalc.set_parameters([1, 2], [2000, 10000], [10, 20], 4)
    average, median, std_dev, best, worst = RCalc.classic_ranking_method(test_alg1)
    assert average == 90.18005616863134
    assert median == 37.639277742375
    assert std_dev == 127.45605020149917
    assert best == 1e-07
    assert worst == 404.74722124547

def test_proposed_ranking():
    RCalc = RankingCalculator()
    RCalc.set_parameters([1, 2], [2000, 10000], [10, 20], 4)
    results = RCalc.proposed_ranking_method(test_alg1)
    assert results['final_score'] == 0.34308072916666665
    assert results['optimum'] == 0.1875
    assert results['threshold'] == 0.29375
    assert results['budget'] == 0.03482291666666667

def test_cec_ranking():
    RCalc = RankingCalculator()
    RCalc.set_parameters([1, 2], [2000, 10000], [10, 20], 4)
    
    all_data = {}
    all_data.update({"alg1": test_alg1})
    all_data.update({"alg2": test_alg2})
    
    results = RCalc.cec_ranking_method(all_data)
    
    assert results['alg1'] == 29.0
    assert results['alg2'] == 35.0
    
    
