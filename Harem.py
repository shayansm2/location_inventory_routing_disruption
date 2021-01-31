#%%
import numpy as np
import pandas as pd
from RedDeer import RedDeer
import random
#%%
class Harem (object):


    def __init__(self, commander, hinds, alpha, beta):

        self.commander = commander
        self.hinds = hinds
        self.n_inner_mate = int(np.round(alpha * len(hinds)))
        self.n_outer_mate = int(np.round(beta * len(hinds)))
        self.childs = []
    

    def inner_harem_mate(self):
        
        random.shuffle(self.hinds)
        for hind in self.hinds[:self.n_inner_mate]:

            child = self.commander.mating(hind)
            self.childs.append(child)


    def outer_harem_mate(self, other_commander):
        
        random.shuffle(self.hinds)
        for hind in self.hinds[:self.n_outer_mate]:

            child = other_commander.mating(hind)
            self.childs.append(child)


    def return_childs(self):
        
        return self.childs

# %%
