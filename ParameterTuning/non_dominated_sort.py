from __future__ import division
from utility import read_file
from collections import defaultdict
# from utility import r
import sys


def binary_domination(one, two, mins=None, maxs=None):
    """
    Binary Domination: We are trying to minimize both SLA and cost
    :param one: First solution
    :param two: Second solution
    :return: True if one dominates two; False otherwise
    """
    assert(len(one) == len(two)), "Something is wrong"
    not_equal = False
    for o, t in zip(one, two):
        if o < t:
            not_equal = True
        elif t < o:
            return False
    return not_equal

def normalize(x, min, max):
    tmp = float((x - min)) / (max - min + 0.000001)
    if tmp > 1: return 1
    elif tmp < 0: return 0
    else: return tmp

def loss(x1, x2, mins=None, maxs=None):
    import math
    # normalize if mins and maxs are given
    if mins and maxs:
        x1 = [normalize(x, mins[i], maxs[i]) for i, x in enumerate(x1)]
        x2 = [normalize(x, mins[i], maxs[i]) for i, x in enumerate(x2)]

    o = min(len(x1), len(x2))  # len of x1 and x2 should be equal
    # print x1, x2
    return sum([-1*math.exp((x2i - x1i) / o) for x1i, x2i in zip(x1, x2)]) / o


def continious_domination(one, two, mins, maxs):
    if loss(one, two, mins, maxs) < loss(two, one, mins, maxs):
        return True
    else:
        return False



def non_dominated_sort(raw_dependents, lessismore, mins, maxs, domination=binary_domination):
    assert(len(raw_dependents[0]) == len(lessismore)), "Something is wrong"
    dependents = []
    for rd in raw_dependents:
        temp = []
        for i in xrange(len(lessismore)):
            # if lessismore[i] is true - Minimization else Maximization
            if lessismore[i] is False:
                temp.append(-1*rd[i])
            else:
                temp.append(rd[i])
        dependents.append(temp)

    non_dominated_indexes = []
    dominating_fits = defaultdict(int)
    for first_count, f_individual in enumerate(dependents):
        for second_count, s_individual in enumerate(dependents):
            if first_count != second_count:
                if domination(f_individual, s_individual, mins, maxs) is True:
                    dominating_fits[second_count] += 1
                elif domination(s_individual, f_individual, mins, maxs) is True:
                    dominating_fits[first_count] += 1
                    break

        if dominating_fits[first_count] == 0:
            # print ". ", dependents[first_count]
            # sys.stdout.flush()
            non_dominated_indexes.append(first_count)

    return non_dominated_indexes


if __name__ == "__main__":
    data = read_file("./Data/Sac1_2.csv")
    dependents = [d.objectives for d in data]
    pf_indexes = non_dominated_sort(dependents, [False, True])
    pf = [dependents[i] for i in pf_indexes]
    pf = sorted(pf, key=lambda x:x[0])

    # import matplotlib.pyplot as plt
    # plt.scatter([d[0] for d in dependents], [d[1] for d in dependents], color='r')
    # plt.plot([p[0] for p in pf], [p[1] for p in pf], color='green', marker='o')
    # plt.show()