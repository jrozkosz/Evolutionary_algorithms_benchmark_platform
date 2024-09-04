# author: Jakub Rozkosz

import os
import numpy as np
import random

UPPER_BOUND = 100
DIMENSIONALITY = 10

def evolutionary_algorithm(obj_function, dimension, rand_seed, best_individual):
    random.seed(rand_seed)
    # population creation
    pop_size = 30
    pop = np.array([])
    for i in range(pop_size):
        x = np.random.uniform(-UPPER_BOUND, UPPER_BOUND, size=dimension)
        pop = np.append(pop, x, axis=0)
    pop = pop.reshape(pop_size, dimension)

    evol = Evolutionary(dimension)
    evol.evolutionary_alg(obj_function, pop, pop_size, 2, 25, best_individual)

class Evolutionary:
    def __init__(self, dimension):
        self.dimension = dimension

    def evolutionary_alg(self, fun_q, P_pop, pop_size, sigma, elite_num, best_individual):
        # print("INIT X: ", best_individual[0])
        tmax = 100000000/pop_size
        t = 0
        eval = []
        for coord in P_pop:
            eval.append((fun_q(coord), coord))
        eval.sort()
        ev_best, x_best = eval[0]
        while (t < tmax):
            R_pop = self.tournament_selection(P_pop, pop_size, fun_q)
            M_pop = self.gaussian_mutation(R_pop, sigma)
            eval_m = []
            for coord in M_pop:
                eval_m.append((fun_q(coord), coord))
            eval_m.sort()
            ev_t, x_t = eval_m[0]
            if ev_t <= ev_best:
                ev_best = ev_t
                x_best = x_t
            P_pop = self.elite_succession(P_pop, M_pop, elite_num, fun_q)
            t += 1

            best_individual[0] = x_best


    def tournament_selection(self, P, pop_size, fun_q):
        R_pop = []
        for i in range(pop_size):
            chosen1 = random.randint(0, pop_size-1)
            chosen2 = random.randint(0, pop_size-1)
            first = P[chosen1]
            second = P[chosen2]
            if fun_q(first) > fun_q(second):
                R_pop.append(second)
            else:
                R_pop.append(first)

        return R_pop

    def gaussian_mutation(self, R_pop, sigma):
        M_pop = []
        for x in R_pop:
            x = x + sigma*(np.random.normal(size=self.dimension))
            M_pop.append(x)

        return M_pop

    def elite_succession(self, P_pop, M_pop, elite_num, fun_q):
        new_pop = []
        eval = []
        for coord in P_pop:
            eval.append((fun_q(coord), coord))
        eval.sort()
        for i in range(elite_num):
            new_pop.append(eval[i][1])
        for x in M_pop:
            new_pop.append(x)
        worst = []
        for coord in new_pop:
            worst.append((fun_q(coord), coord))
        worst.sort()
        worst_coord = [i[1] for i in worst]
        new_pop = worst_coord[:len(P_pop)]

        return new_pop