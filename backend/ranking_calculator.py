import json
import numpy as np
import os
import random

class RankingCalculator:
    def __init__(self) -> None:
        self.call_count = 0
        if os.path.exists("ranking_config.json"):
            with open("ranking_config.json", 'r') as f:
                params = json.load(f)
            self.g_optimum = params["g_optimum"]
            self.functions = params["functions"]
            self.max_call_count = params["max_call_count"]
            self.dimensions = params["dimensions"]
            self.runs = params["runs"]
    
    def set_parameters(self, functions, max_call_count, dimensions, runs):
        self.functions = functions
        self.max_call_count = max_call_count
        self.dimensions = dimensions
        self.runs = runs
            
    def cec_ranking_method(self, data_file_all_algorithms):
        data = data_file_all_algorithms
        cec_scores = {}
        for dim, max_fes in zip(self.dimensions, self.max_call_count):
            for fun in self.functions:
                final_scores = {}
                all_algs_fun_trials = []
                for alg in data:
                    # alg_results = [(alg, float(res)) for res in (data[alg][f"function_{fun}"][f"dim_{dim}"]).split(',')]
                    alg_results = [(alg, (data[alg][f"function_{fun}"][f"dim_{dim}"][f"trial_{run_num}"])) for run_num in range(self.runs)]
                    all_algs_fun_trials.extend(alg_results)
                
                # calculating algorithms ratings
                sorted_results = sorted(all_algs_fun_trials, key=lambda x: (x[1][0], x[1][1]))
                function_points = {}
                for idx, sr in enumerate(sorted_results):
                    if sr[0] in function_points:
                        function_points[sr[0]] = function_points[sr[0]] + len(sorted_results)-idx
                    else:
                        function_points[sr[0]] = len(sorted_results)-idx
                # print("FUNCTION_POINTS: ", function_points)
                for alg_name in function_points:
                    if alg_name in final_scores:
                        final_scores[alg_name] = final_scores[alg_name] + function_points[alg_name] - self.runs*(self.runs+1)/2
                    else:
                        final_scores[alg_name] = function_points[alg_name] - self.runs*(self.runs+1)/2
                for alg_name in final_scores:
                    if alg_name in cec_scores:
                        cec_scores[alg_name] = cec_scores[alg_name] + final_scores[alg_name]
                    else:
                        cec_scores[alg_name] = final_scores[alg_name]
                    # print(f"DIM{dim}", cec_scores[alg_name])
            
        # print(cec_scores)
        return cec_scores

    def proposed_ranking_method(self, data_file):
        data = data_file
        length_out = 51
        threshold = 10**np.linspace(np.log10(1e3), np.log10(1e-8), length_out)[:-1]
        score_weight = 0.5
        found_optimum = 0
        found_threshold = 0
        budget_left = 0
        all_runs = len(self.dimensions)*len(self.functions)*self.runs
        all_thresholds = all_runs*len(threshold)
        all_budget = (all_runs/2)*self.max_call_count[0] + (all_runs/2)*self.max_call_count[1]
        for dim, max_fes in zip(self.dimensions, self.max_call_count):
            for fun in self.functions:
                for r in range(self.runs):
                    # alg_results = [(alg, float(res)) for res in (data[alg][f"function_{fun}"][f"dim_{dim}"]).split(',')]
                    results = data[f"function_{fun}"][f"dim_{dim}"][f"trial_{r}"]
                    error, calls_count = results            
                    if error <= 10e-8:  #1e8:
                        found_optimum += 1
                        found_threshold += len(threshold)
                        budget_left += max_fes - calls_count
                    else:
                        thresholds_reached = self.find_no_of_thresholds_reached(threshold, error)
                        found_threshold += thresholds_reached
        
        g_optimum_percent = found_optimum / all_runs
        print("Optimum percent: ", g_optimum_percent)
        threshold_percent = found_threshold / all_thresholds
        print("Threshold percent: ", threshold_percent)
        budget_left_percent = budget_left / all_budget
        print("Budget percent: ", budget_left_percent)
        final_score = (g_optimum_percent + score_weight*threshold_percent + (score_weight**2)*budget_left_percent)
        print(final_score)
        proposed_scores = {"final_score": final_score, "optimum": g_optimum_percent, "threshold": threshold_percent, "budget": budget_left_percent}

        return proposed_scores

    def find_no_of_thresholds_reached(self, threshold, error):
        num = 0
        for th in threshold:
            if error > th:
                return num
            num += 1
    
    # did execution time comparison and it is not beneficial for that small size of thresholds array, it is getting better for a size of houndres/thousands 
    def find_thresholds_reached_divide_and_conquer(self, threshold, error):
            if len(threshold) == 1:
                return threshold[0]
            if threshold[int(len(threshold)/2)] > error:
                return self.find_thresholds_reached_divide_and_conquer(threshold[int(len(threshold)/2):], error)
            if threshold[int(len(threshold)/2)] < error:
                return self.find_thresholds_reached_divide_and_conquer(threshold[:int(len(threshold)/2)], error)
    
    def classic_ranking_method(self, data_file):
        data = data_file
        errors = []
        all_runs = len(self.dimensions)*len(self.functions)*self.runs
        for dim, max_fes in zip(self.dimensions, self.max_call_count):
            for fun in self.functions:
                for r in range(self.runs):
                    # alg_results = [(alg, float(res)) for res in (data[alg][f"function_{fun}"][f"dim_{dim}"]).split(',')]
                    results = data[f"function_{fun}"][f"dim_{dim}"][f"trial_{r}"]
                    error, calls_count = results   
                    errors.append(error)
        
        # print("errors: ", errors)
        avg_error = np.sum(errors) / all_runs
        print(avg_error)
        median_error = np.median(errors)
        print(median_error)
        std_dev = np.std(errors)
        print(std_dev)
        best_one = np.min(errors)
        worst_one = np.max(errors)
        return avg_error, median_error, std_dev, best_one, worst_one
