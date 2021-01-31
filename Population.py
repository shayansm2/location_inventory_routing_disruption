#%%
import numpy as np
import pandas as pd
from TestProblem import TestProblem
from RedDeer import RedDeer
from Harem import Harem
import random
#%%
class Population (object):


    def __init__(self, n_pop = 20, n_hind = 12, gamma = 0.4, alpha = 0.8, beta = 0.3):
        
        problem = TestProblem()
        RedDeer.set_problem(problem)

        self.n_pop = n_pop
        self.n_hind = n_hind
        n_male = n_pop - n_hind
        self.n_com = int(np.round(n_male*gamma))
        self.n_stag = n_male - self.n_com
        self.alpha = alpha
        self.beta = beta

        self.all_rds = []
        self.commanders = []
        self.stags = []
        self.hinds = []
        self.childs = []
        self.harems = {}


    def initialize(self):

        for _ in range(self.n_pop):
            rd = RedDeer()
            self.all_rds.append(rd)
    

    def hind_selection(self):
        
        self.all_rds.sort(key = lambda x: x.fitness, reverse = True)
        self.hinds = self.all_rds[:self.n_hind]
        self.all_rds = self.all_rds[self.n_hind:]
    

    def roaring(self):

        for rd in self.all_rds:
            rd.roaring()
    

    def commander_selection(self):

        self.all_rds.sort(key = lambda x: x.fitness, reverse = True)
        self.stags = self.all_rds[:self.n_stag]
        self.commanders = self.all_rds[self.n_stag:]
        self.all_rds = []

    
    def fighting(self):

        random.shuffle(self.commanders)
        commander_index = 0
        for stag in self.stags:

            self.commanders[commander_index].fighting(stag)
            commander_index += 1
            if commander_index == self.n_com:
                commander_index = 0
    

    def form_harem(self):
        
        v = [commander.fitness for commander in self.commanders]
        V = max(v) - v
        p = V / sum(V)

        n_harem = np.round(self.n_hind * p).astype(int)
        harem_index = np.concatenate((np.array([0]),n_harem)).cumsum()
        random.shuffle(self.hinds)

        for i in range(self.n_com):

            harem = Harem(self.commanders[i], self.hinds[harem_index[i]:harem_index[i+1]], self.alpha, self.beta)
            self.harems[self.commanders[i]] = harem


    def inner_harem_mate(self):

        for commander in self.commanders:

            self.harems[commander].inner_harem_mate()
    

    def outer_harem_mate(self):

        random.shuffle(self.commanders)
        
        for commander_index in range(-1, self.n_com - 1):

            self.harems[self.commanders[commander_index]].outer_harem_mate(self.commanders[commander_index + 1])


    def get_harem_childs(self):

        for commander in self.commanders:

            self.childs += self.harems[commander].return_childs()


    def stag_mate(self):

        for stag in self.stags:

            best_hind = self.hinds[0]
            min_distance = stag.distance(best_hind)

            for hind_index in range(1, self.n_hind):

                new_distance = stag.distance(self.hinds[hind_index])
                if new_distance < min_distance:
                    min_distance = new_distance
                    best_hind = self.hinds[hind_index]
            
            child = stag.mating(best_hind)
            self.childs.append(child)

    
    def new_generation(self):

        all_population = self.commanders + self.stags + self.hinds + self.childs
        self.commanders = []
        self.stags = []
        self.hinds = []
        self.childs = []

        tournament_selection_n = int((len(all_population) - self.n_pop) / 5)

        for i in range(self.n_pop):

            tournament = random.sample(all_population, tournament_selection_n)
            tournament.sort(key = lambda x: x.fitness)
            all_population.remove(tournament[0])
            self.all_rds.append(tournament[0])
    

    def return_best_answer(self):

        best_solution = "not found any feasible solution"
        self.all_rds.sort(key = lambda x: x.fitness)
        for rd in self.all_rds:
            if rd.penalty_function() == 0 :
                best_solution = rd
                break
        return best_solution
