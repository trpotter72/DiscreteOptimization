from typing import List

def mostValue(capacity, items: List):
    items.sort(key = lambda i: i.value, reverse=True)
    value = 0
    taken = [0] * len(items)
    for i in items:
        if i.weight < capacity:
            value += i.value
            capacity -= i.weight
            taken[i.index] = 1
            if capacity == 0:
                return (value, taken)
    return (value, taken)

def valueDensity(capacity, items: List):
    items.sort(key = lambda i : i.value/i.weight, reverse=True)
    value = 0
    taken = [0] * len(items)
    for i in items:
        if i.weight < capacity:
            value += i.value
            capacity -= i.weight
            taken[i.index] = 1
            if capacity == 0:
                return (value, taken)
    return (value, taken)