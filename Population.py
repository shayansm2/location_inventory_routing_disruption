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
        pass