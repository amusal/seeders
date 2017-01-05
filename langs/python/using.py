import itertools

"""
C(items, nums)
    items: item list
    nums: numbers of items to pick
"""
def iter_combination(items, nums):
    return itertools.combinations(items, nums)


"""
P(items, nums)
    items: item list
    nums: numbers of items to pick
"""
def iter_permutations(items, nums):
    return itertools.permutations(items, nums)