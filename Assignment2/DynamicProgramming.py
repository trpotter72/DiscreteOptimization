from typing import List
from math import gcd
from HeuristicUtil import safeValAdjust, pruneDensityKeepSmall
from Item import Item
import numpy as np
from GreedySolvers import valueDensity
from numba import jit, njit
#Constants for DP algorithm #
#---------------------------#
#Prune lowest value density items
max_item_count = 10000

#Divide values and capacity (rounding up) to have this overall capacity
max_iterations = 100000000

#Keep this percent of the smallest items (regardless of density)
smallest_to_keep = .05 
#___________________________#

def DP(capacity:int, items: List[Item], 
       adjust_item_count:bool = True, 
       adjust_capacity:bool = True, 
       debug:bool = False) -> (int, List[int]):
    
    if debug: print("-Starting Data Adjustments-\n")
    taken = [0] * len(items)
    if adjust_item_count:
        items = pruneDensityKeepSmall(items, max_item_count, smallest_to_keep)

    max_capacity = max_iterations // len(items)
    if adjust_capacity:
        if capacity > max_capacity:
            capacity, items = safeValAdjust(items, capacity, max_capacity, debug=debug)
    if debug: print("-End Data Adjustments-\n\n")

    dp2d = np.zeros((len(items)+1, capacity+1), dtype=int)
    
    if debug: print("-Start Array Population-\n\n")
    # # Calculate item by item 
    # for i in range(1,len(dp2d)):
    #     if debug: print("Item {}\tof {}".format(i, len(dp2d)))
    #     j = 0
    #     w = items[i-1].weight
    #     v = items[i-1].value
    #     while j <= capacity:
    #         if j >= w and (dp2d[i-1][j-w] + v > dp2d[i-1][j]):
    #             dp2d[i][j] += dp2d[i-1][j-w] + v 
    #         else:
    #             dp2d[i][j] += dp2d[i-1][j]
    #         j += 1
    # value = dp2d[-1][-1]
    @njit
    def fillGrid(dp2d, items):
        #Calculate capacity at a time
        for j in range(capacity+1):
        
            # if debug: print("Capacity {}\tof {}".format(j, capacity))
            # elif j % 100 == 0: print("{:.1f}%\t({} capacity)".format(j/capacity,capacity))
            for i in range(1,len(dp2d)):
                if j >= items[i-1].weight and (dp2d[i-1][j-items[i-1].weight] + items[i-1].value > dp2d[i-1][j]):
                    dp2d[i][j] += dp2d[i-1][j-items[i-1].weight] + items[i-1].value 
                else:
                    dp2d[i][j] += dp2d[i-1][j]
    fillGrid(dp2d, items)
    value = dp2d[-1][-1]
    if debug: print("-End Array Population-\n\n")

    #Back-track to fill the taken array
    j = capacity
    for i in range(len(dp2d)-1, 0, -1):
        if dp2d[i][j] != dp2d[i-1][j]: #means this was taken
            taken[items[i-1].index] = 1
            j -= items[i-1].weight

    return value, taken