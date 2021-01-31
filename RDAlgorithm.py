#%%
import numpy as np
import pandas as pd
from TestProblem import TestProblem
from RedDeer import RedDeer
from Population import Population
import matplotlib.pyplot as plt
#%%
def red_deer_algorithm(n_iter):
    """
    deafult hyper parameters
    n_pop = 20
    n_hind = 12
    gamma = 0.4
    alpha = 0.8
    beta = 0.3
    n_iter = 30
    """
    print("choose the test problem")
    pop = Population()
    pop.initialize()
    best_solutions = [pop.return_best_answer()]

    for _ in range(n_iter):

        pop.hind_selection()
        pop.roaring()
        pop.commander_selection()
        pop.form_harem()
        pop.inner_harem_mate()
        pop.outer_harem_mate()
        pop.get_harem_childs()
        pop.stag_mate()
        pop.new_generation()

        best_solutions.append(pop.return_best_answer())

    return best_solutions

# %%
n_iter = 30
solutions = red_deer_algorithm(n_iter)
print("best solution :\n" ,  solutions[-1])
x = range(n_iter+1)
y = [solution.objective_function for solution in solutions]
plt.plot(x,y)

# %%
