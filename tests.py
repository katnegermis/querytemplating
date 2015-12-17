from classes import *


def test_num_combinations():
    from functools import reduce
    import operator

    mult = lambda xs: reduce(operator.mul, xs, 1)
    variablecombinations = lambda q: mult(len(q.variables[k]) for k in q.variables)

    setups = [QueryTemplate(variables={'c1': [1, 2, 3], 'c2': [4, 5, 6, 4]}, name="", sql="")]
    query = QueryTemplate(variables={'a': [1, 2], 'b': [3, 4]}, setupqueries=setups, sql="", name="")

    combinations = variablecombinations(query) * sum(variablecombinations(s) for s in setups)
    assert combinations == 48, combinations

if __name__ == "__main__":
    test_num_combinations()
