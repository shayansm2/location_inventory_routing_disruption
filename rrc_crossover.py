import numpy as np

def rrc_crossover(parent1, parent2):

    p1 = parent1.astype(bool)
    p2 = parent2.astype(bool)
    difference = np.bitwise_xor(p1,p2)
    randomize = np.random.randint(2,size = len(p1))
    c1 = np.bitwise_xor(p1, difference * randomize.astype(bool))
    c2 = np.bitwise_xor(p1, difference * (1 - randomize.astype(bool)))
    child1 = c1.astype("int32")
    child2 = c2.astype("int32")
    
    return (child1, child2)