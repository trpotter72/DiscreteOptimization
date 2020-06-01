from solver import openFile, solve_it, parseInput
from DynamicProgramming import DP
from GreedySolvers import valueDensity, mostValue
from time import perf_counter
import sys

def test(file_name):
    rawData = openFile(file_name)
    capacity, items = parseInput(rawData)
    names = [DP, valueDensity, mostValue]
    for name in names:
        start = perf_counter()
        value, _ = name(capacity, items)
        elapsed = perf_counter() - start
        print(name.__name__ + "\t"+ str(value) + "\t" + '%f1'%elapsed)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        test(file_name)
    else:
        print("Please provide a test file")
    