from typing import List
from itertools import islice
from Item import Item
from math import ceil, floor

def pruneOnDensity(items: List[Item], items_returned: int) -> List:
    dens_list = map(lambda i : (density, i), items)
    top_n = islice(sorted(dens_list, reverse=True), items_returned)
    just_items = map(lambda i: i[1], top_n)
    return list(just_items)

def pruneDensityKeepSmall(items: List[Item], items_returned:int, smallest_ratio:float) -> List[Item]:
    #grab the smallest out
    if items_returned >= len(items):
        return items
    take = floor(items_returned*smallest_ratio)
    items.sort(key=lambda i: i.weight)
    smallest = items[:take]
    rest = items[take:]
    rest = pruneOnDensity(rest, ceil(items_returned*(1-smallest_ratio)))
    return smallest + rest

def adjustedValAndCapacity(items: List[Item], curr_cap:int, target_cap:int, debug:bool=False) -> (int, List[Item]):
    if(curr_cap <= target_cap):
        return curr_cap, items
    reduction_factor = curr_cap / target_cap # >1
    new_items = list(map(lambda i : Item(i.index, i.value, ceil(i.weight/reduction_factor)), items))
    new_cap = floor(curr_cap/reduction_factor)
    new_cap = floor(new_cap*(getMinError(items, new_items, reduction_factor)+1))
    if debug:
        print("Careless adjust analysis\n")
        changeAnalysis(items, new_items, curr_cap, new_cap, reduction_factor)
    return new_cap, new_items

def safeValAdjust(items: List[Item], curr_cap:int, target_cap:int, debug:bool=False) -> (int, List[Item]):
    """
    Insight:
        Let's look at the minimum gap between weight entries.  We can then make
        this minimum gap our new unit element for the weight.  In order to preserve
        correctness and ordering, we'll always need to round-up to the next integer.

    """
    biggest_gap = curr_cap
    items.sort(key= lambda i: i.weight)
    for i in range(1, len(items)):
        if items[i].weight != items[i-1].weight:
            biggest_gap = min(items[i].weight - items[i-1].weight, biggest_gap)
    new_cap = floor(curr_cap/biggest_gap)
    new_items = list(map(lambda i : Item(i.index, i.value, ceil(i.weight/biggest_gap)), items))
    new_cap = floor(new_cap*(getMinError(items, new_items, biggest_gap)+1))
    if(debug):
        print("Safe weight adjust analysis\n")
        changeAnalysis(items, new_items, curr_cap, new_cap, biggest_gap)
    if new_cap > target_cap:
        new_cap, new_items = adjustedValAndCapacity(items, new_cap, target_cap, debug=debug)
    return new_cap, new_items

def density(item:Item):
    return item.value/item.weight

def changeAnalysis(items:List[Item], new_items:List[Item], curr_cap:int, new_cap:int, reduction_factor:float) -> None:
        print("-"*50 + "\n new_cap: " + str(new_cap) + "\told_cap: " + str(curr_cap) +  "\treduction_factor " + str(reduction_factor) + "\n" + "-"*50)
        print("Capacity Change\ni\tOld\tNew\tChange\tFactor\tIdeal\t\tError\n")
        for i in range(len(new_items)):
            old = items[i].weight
            new = new_items[i].weight
            stat = str(i) + "\t" #Index
            stat += str(old) + "\t" #Old
            stat += str(new) + "\t" #New
            stat += str(old - new) + "\t" #Change
            stat += '%.1f'%(old / new) + "\t" #Factor
            stat += str((old/reduction_factor)) + "\t\t" #Ideal
            stat += "%.4f"%((new - old/reduction_factor)/new) #Error
            print(stat + "\n")

def getMinError(items:List[Item], new_items:List[Item], reduction_factor:float)->float:
    min_err = 1
    for i in range(len(new_items)):            
        old = items[i].weight
        new = new_items[i].weight
        min_err = min((new - old/reduction_factor)/new, min_err)
    return min_err
