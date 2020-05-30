from typing import List
from math import gcd

def DP(capacity, items: List):
    # weights_gcd = listGCD( list(map(lambda i : i.weight, items)) + [capacity])
    # new_weights = list(map(lambda i: i.weight//weights_gcd, items))
    # capacity = capacity//weights_gcd
    dp2d = []
    taken = [0] * len(items)
    for _ in range(len(items)+1):
        dp2d.append([0]*(capacity+1))

    #populate 2d dynamic array
    for i in range(1,len(dp2d)):
        for j in range(len(dp2d[0])):
            dp2d[i][j] = dp2d[i-1][j]
            if j >= items[i-1].weight:
                dp2d[i][j] = max(
                    dp2d[i-1][j],
                    dp2d[i-1][j-items[i-1].weight] + items[i-1].value
                )
    value = dp2d[-1][-1]

    #Back-track to fill the taken array
    j = capacity
    for i in range(len(dp2d)-1, 0, -1):
        if dp2d[i][j] != dp2d[i-1][j]: #means this was taken
            taken[i-1] = 1
            j -= items[i-1].weight

    return value, taken


def listGCD(nums:List):
    ans = gcd(nums[0],nums[1])
    for i in nums:
        ans = gcd(ans,i)
    return ans