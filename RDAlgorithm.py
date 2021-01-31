#%%
import numpy as np
import pandas as pd
from TestProblem import TestProblem
from RedDeer import RedDeer
from Population import Population
#%%
def red_deer_algorithm():
    pass

#%%
'''
deafult hyper parameters
n_pop = 20
n_hind = 12
gamma = 0.4
alpha = 0.8
beta = 0.3
'''
pop = Population()
#%%
pop.initialize()
pop.hind_selection()
pop.roaring()
pop.commander_selection()

# %%


# %%
