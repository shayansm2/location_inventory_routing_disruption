import numpy as np
def  pmx_crossover(parent1, parent2):

    p1 = list(parent1)
    p2 = list(parent2)
    cuts = np.random.randint(0,len(p1),size=2)
    low = min(cuts) 
    high = max(cuts) 
    c1 = p2[:low] + p1[low:high+1] + p2[high+1:] 
    # c2 = p1[:low] + p2[low:high+1] + p1[high+1:] 
    swath_p1 = p1[low:high+1]
    # swath_p2 = p2[low:high+1]
    for i in range(low, high + 1):
        if p2[i] not in swath_p1:
            position = i
            while ((position >= low) and (position <= high)):
                position = p2.index(p1[position])
            c1[position] = p2[i]
    # for i in range(low, high + 1):
    #     if p1[i] not in swath_p2:
    #         position = i
    #         while ((position >= low) and (position <= high)):
    #             position = p1.index(p2[position])
    #         c2[position] = p1[i]
    return np.array(c1)