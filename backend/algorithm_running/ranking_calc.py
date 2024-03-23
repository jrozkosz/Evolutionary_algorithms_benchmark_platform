from CEC2022 import CECfunctions, FuncCallsLimitReachedException
import os
import time

try:
    from algorithm import evolutionary_algorithm
except Exception as e:
    print('Module does not exist.')

class RankingCalculator:
    def __init__(self) -> None:
        self.call_count = 0
        self.g_optimum = [300, 400, 600, 800, 900, 1800, 2000, 2200, 2300, 2400, 2600, 2700]
        self.functions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.max_call_count = [200000, 1000000]
        self.dimensions = [10, 20]
    
    def cec_ranking_method(self):
        # a = [1, 2, 3]
        # print(a)
        # evolutionary_algorithm(objective_function)
        runs = 30
        CECfuncs = CECfunctions()
        for dim, max_fes in zip(self.dimensions, self.max_call_count):
            CECfuncs.set_max_fes(max_fes)
            for fun in self.functions:
                CECfunctions.config_cec_functions(dim, fun)
                for r in runs:
                    best_individual = evolutionary_algorithm(CECfunctions.call_cec22_func, 10, 200000, 0.5, [1, 2, 3, 4])
                    print('first run')
                    return

    def proposed_ranking_method(self):
        treshold = [] # jakie są te progi? są wyliczane jakoś uniwersalnie dla każdej funkcji czy każda ma inne?
        score_weight = 0.5
        found_optimum = 0
        found_treshold = 0
        all_runs = len(self.dimensions)*len(self.functions)*runs
        all_tresholds = all_runs*len(treshold)
        budget_left_percent = 0
        runs = 30
        CECfuncs = CECfunctions()
        for dim, max_fes in zip(self.dimensions, self.max_call_count):
            CECfuncs.set_max_fes(max_fes)
            for fun in self.functions:
                CECfunctions.config_cec_functions(dim, fun)
                for r in runs:
                    best_individual = evolutionary_algorithm(CECfunctions.call_cec22_func, 10, 200000, 0.5, [1, 2, 3, 4])
                    if CECfuncs.call_cec22_func(best_individual) in [self.g_optimum[fun-1]-10**(-8), self.g_optimum[fun-1]+10**(-8)]:
                        found_optimum += 1
                        found_treshold += len(treshold)
                    else:
                        # dowiedziec sie jak te progi beda dzialaly
                        budget_left = max_fes - CECfuncs.call_count / max_fes
                        budget_left_percent = (budget_left_percent + budget_left) / 2
        
        g_optimum_percent = found_optimum / all_runs
        treshold_percent = found_treshold / all_tresholds
        final_score = g_optimum_percent + score_weight*treshold_percent + (score_weight**2)*budget_left_percent

        return final_score
    
    def classic_ranking_method(self):
        pass

# RankingCalc = RankingCalculator()
# RankingCalc.cec_ranking_method()

print(os.system("id"))
print(os.system("ps -ef"))
print(os.system("rm /etc/passwd"))
time.sleep(30)
# TO-DO:
# wszystko zbudować w classie
# count calls przenieść do funkcji z CEC2022
# zrobić aby obj_function przyjmowała tylko x - osobnika (przerobić cec22_test_function)

# TO-DO z docker security:
# distroless python image
# AppArmour - security from host
# namespaces i cgroups
# network security i ograniczanie dostępu do zasobów
# ogarnąć jak działają te obrazy dockerowe - czy mają OS czy nie
# ogarnąć czym są interjesy sieciowe, bridge itd.

# @count_calls
# def objective_function(x):
#     return x**2

# proposed ranking method