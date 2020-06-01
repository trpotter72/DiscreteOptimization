from typing import List, Dict
from HeuristicUtil import safeValAdjust, pruneDensityKeepSmall, density
from Item import Item
import numpy as np
from GreedySolvers import valueDensity
from numba import jit, njit
from math import floor
from collections import deque, namedtuple


def BranchBound(capacity:int, items:List[Item], debug:bool = False)-> (int, List[int]):
    '''
    (1) Find upper limit estimator via fractional relaxing
    (2) Create supporting framework for search
    (3) Search
    '''
    taken = [0] * len(items)
    sortDescendingDensity(items)
    best = [0]        
    val = DFSearch(capacity, 0, items, 0, best, taken, 0, debug)
    return val, taken

@njit
def DFSearch(capacity:int, curr_val:int, sortedItems:List[Item], i:int, best:List[int], taken:List[int], depth:int, debug:bool = False)->int:

    if i >= len(sortedItems):
        if curr_val > best[0] and capacity >= 0:
            best[0] = curr_val
            return curr_val
        else:
            return -1

    if capacity < 0:
        # if debug: treePrint(depth, {"Over Capacity":""})
        return -1

    
    # Create upper-bound estimate
    estimate = curr_val + upper_bound(capacity, sortedItems, i)
    # if debug: treePrint(depth, {"V":sortedItems[i].value, "W":sortedItems[i].weight, "Val":curr_val, "Est":estimate, "Best":best[0]})
    if estimate < best[0]:
        return -1 #stop search if better solution exists
    
    #Recursive calls return zero if they don't beat the global best
    taken_val   = DFSearch(capacity-sortedItems[i].weight, curr_val + sortedItems[i].value, sortedItems, i+1, best, taken, depth+1, debug=debug)
    untaken_val = DFSearch(capacity, curr_val, sortedItems, i+1, best, taken, depth+1, debug=debug)
    
    if taken_val == -1 and untaken_val == -1:
        return -1 #don't change the taken array
    elif taken_val > untaken_val:
        taken[sortedItems[i].index] = 1
        return taken_val
    else:
        taken[sortedItems[i].index] = 0
        return untaken_val

@njit
def upper_bound(capacity:int, sortedItems, i):
    val = 0
    for index in range(i, len(sortedItems)):
        item = sortedItems[index]
        if capacity > item.weight:
            val += item.value
            capacity -= item.weight
        else:
            val += (capacity/item.weight)*item.value
            break
    return floor(val)

def sortDescendingDensity(items:List[Item])->List[Item]:
    return items.sort(key=lambda i: i.value/i.weight, reverse=True)

def treePrint(depth, d:Dict) -> None:
    s = "| "*max(depth,0) + "|-"
    for k,v in d.items():
        s += str(k) + ": " + str(v) + " "
    print(s)