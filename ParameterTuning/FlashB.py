from __future__ import division
import numpy as np
import os
import sys
from random import shuffle
import time
sys.path.append("/Users/viveknair/GIT/Flash-MultiConfig/")
from utility import  generational_distance, inverted_generational_distance, read_file
from non_dominated_sort import non_dominated_sort, binary_domination


lessismore = {}
lessismore["SS-A"] = [False, True]
lessismore["SS-B"] = [False, False]
lessismore["SS-C"] = [False, True]
lessismore["SS-D"] = [False, True]
lessismore["SS-E"] = [False, True]
lessismore["SS-F"] = [False, True]
lessismore["SS-G"] = [False, True]
lessismore["SS-H"] = [False, False]
lessismore["SS-I"] = [False, True]
lessismore["SS-J"] = [False, True]
lessismore["SS-K"] = [False, True]
lessismore["SS-L"] = [False, False]
lessismore["SS-M"] = [True, True]
lessismore["SS-N"] = [True, True]
lessismore["SS-O"] = [True, True]


ranges = {}
# ranges[filename] = [[min(obj1), max(obj2)], [min(obj2), max(obj2)]]
ranges["SS-A"] = [[288.56, 23075.0], [148.88, 9421.0]]
ranges["SS-B"] = [[7.087462841, 16.24881706], [2.858160813, 14.71664238]]
ranges["SS-C"] = [[121.5, 11930.0], [247.45, 57645.0]]
ranges["SS-D"] = [[3964.2, 65823.0], [2.0815, 105000.0]]
ranges["SS-E"] = [[5042.6, 95094.0], [1.2994, 94553.0]]
ranges["SS-F"] = [[4275.4, 72394.0], [1.9243, 99722.0]]
ranges["SS-G"] = [[3983.3, 63734.0], [2.1844, 93904.0]]
ranges["SS-H"] = [[6.144515496, 9.965784285], [4.309193816, 5.123159887]]
ranges["SS-I"] = [[2122.2, 20591.0], [47.387, 405.5]]
ranges["SS-J"] = [[68.062, 232000.0], [1.9, 34733.0]]
ranges["SS-K"] = [[72.75, 34740.0], [3.3172, 55209.0]]
ranges["SS-L"] = [[199.68, 270.4], [11.0, 29.0]]
ranges["SS-M"] = [[3, 501],[32.96, 18842.204]]
ranges["SS-N"] = [[15.892, 100.0],[0.0, 19320.06667]]
ranges["SS-O"] = [[0, 134],[0.39, 91.57]]


def get_nd_solutions(filename, train_indep, training_dep, testing_indep):
    no_of_objectives = len(training_dep[0])
    predicted_objectives = []
    for objective_no in xrange(no_of_objectives):
        from sklearn.tree import DecisionTreeRegressor
        model = DecisionTreeRegressor()
        model.fit(train_indep, [t[objective_no] for t in training_dep])
        predicted = model.predict(testing_indep)
        predicted_objectives.append(predicted)

    # Merge the objectives
    merged_predicted_objectves = []
    for i in xrange(len(predicted_objectives[0])):
        merged_predicted_objectves.append([predicted_objectives[obj_no][i] for obj_no in xrange(no_of_objectives)])
    assert(len(merged_predicted_objectves) == len(testing_indep)), "Something is wrong"

    # Find Non-Dominated Solutions
    pf_indexes = non_dominated_sort(merged_predicted_objectves, lessismore[filename], [r[0] for r in ranges], [r[1] for r in ranges])
    # print "Number of ND Solutions: ", len(pf_indexes)

    return [testing_indep[i] for i in pf_indexes], [merged_predicted_objectves[i] for i in pf_indexes]

def normalize(x, min, max):
    tmp = float((x - min)) / (max - min + 0.000001)
    if tmp > 1: return 1
    elif tmp < 0: return 0
    else: return tmp


def get_next_points(file, training_indep, training_dep, testing_indep, directions):
    no_of_objectives = len(training_dep[0])

    predicted_objectives = []
    for objective_no in xrange(no_of_objectives):
        from sklearn.tree import DecisionTreeRegressor
        model = DecisionTreeRegressor()
        model.fit(training_indep, [t[objective_no] for t in training_dep])
        predicted = model.predict(testing_indep)
        predicted_objectives.append(predicted)

    # Merge the objectives
    merged_predicted_objectves = []
    for i in xrange(len(predicted_objectives[0])):
        merged_predicted_objectves.append([predicted_objectives[obj_no][i] for obj_no in xrange(no_of_objectives)])
    assert (len(merged_predicted_objectves) == len(testing_indep)), "Something is wrong"


    # Convert the merged_predicted_objectives to minimization problem
    lism = lessismore[file]
    dependents = []
    for rd in merged_predicted_objectves:
        temp = []
        for i in xrange(len(lism)):
            # if lessismore[i] is true - Minimization else Maximization
            if lism[i] is False:
                temp.append(-1 * rd[i])
            else:
                temp.append(rd[i])
        dependents.append(temp)

    # Normalize objectives
    mins = [r[0] for r in ranges[file]]
    maxs = [r[1] for r in ranges[file]]

    normalized_dependents = []
    for dependent in dependents:
        normalized_dependents.append([normalize(dependent[i], mins[i], maxs[i]) for i in xrange(no_of_objectives)])
    assert(len(normalized_dependents) == len(dependents)), "Something is wrong"

    return_indexes = []
    for direction in directions:
        transformed = []
        for dependent in normalized_dependents:
            assert(len(direction) == len(dependent)), "Something is wrong"
            transformed.append(sum([i*j for i, j in zip(direction, dependent)]))
        return_indexes.append(transformed.index(min(transformed)))
    assert(len(return_indexes) == len(directions)), "Something is wrong"

    return_indexes = list(set(return_indexes))
    return return_indexes

def get_random_numbers(len_of_objectives):
    from random import random
    random_numbers = [random() for _ in xrange(len_of_objectives)]
    ret = [num/sum(random_numbers) for num in random_numbers]
    # print ret, sum(ret), int(sum(ret))==1
    # assert(int(sum(ret)) == 1), "Something is wrong"
    return ret


def run_main(files, repeat_no, stop, start_size):
    initial_time = time.time()
    all_data = {}
    initial_sample_size = start_size
    for file in files:
        all_data[file] = {}
        all_data[file]['evals'] = []
        all_data[file]['gen_dist'] = []
        all_data[file]['igd'] = []

        print file
        data = read_file('../Data/' + file + '.csv')

        # Creating Objective Dict
        objectives_dict = {}
        for d in data:
            key = ",".join(map(str, d.decisions))
            objectives_dict[key] = d.objectives

        number_of_objectives = len(data[0].objectives)
        number_of_directions = 10

        directions = [get_random_numbers(number_of_objectives) for _ in xrange(number_of_directions)]
        shuffle(data)

        training_indep = [d.decisions for d in data[:initial_sample_size]]
        testing_indep = [d.decisions for d in data[initial_sample_size:]]

        while True:
            print ". ",
            sys.stdout.flush()

            def get_objective_score(independent):
                key = ",".join(map(str, independent))
                return objectives_dict[key]

            training_dep = [get_objective_score(r) for r in training_indep]

            next_point_indexes = get_next_points(file, training_indep, training_dep, testing_indep, directions)
            # print "Points Sampled: ", next_point_indexes
            next_point_indexes = sorted(next_point_indexes, reverse=True)
            for next_point_index in next_point_indexes:
                temp = testing_indep[next_point_index]
                del testing_indep[next_point_index]
                training_indep.append(temp)
            # print len(training_indep), len(testing_indep), len(data)
            assert(len(training_indep) + len(testing_indep) == len(data)), "Something is wrong"
            if len(training_indep) >= stop: break


        print
        print "Size of the frontier = ", len(training_indep), " Evals: ", len(training_indep),
        # Calculate the True ND
        training_dependent = [get_objective_score(r) for r in training_indep]
        approx_dependent_index = non_dominated_sort(training_dependent, lessismore[file], [r[0] for r in ranges[file]],
                                             [r[1] for r in ranges[file]])
        approx_dependent = sorted([training_dependent[i] for i in approx_dependent_index], key=lambda x: x[0])
        all_data[file]['evals'].append(len(training_indep))

        actual_dependent = [d.objectives for d in data]
        true_pf_indexes = non_dominated_sort(actual_dependent, lessismore[file], [r[0] for r in ranges[file]],
                                             [r[1] for r in ranges[file]])
        true_pf = sorted([actual_dependent[i] for i in true_pf_indexes], key=lambda x: x[0])
        print "Length of True PF: " , len(true_pf),
        print "Length of the Actual PF: ", len(training_dependent),
        all_data[file]['gen_dist'].append(generational_distance(true_pf, approx_dependent, ranges[file]))
        all_data[file]['igd'].append(inverted_generational_distance(true_pf, approx_dependent, ranges[file]))

        print " GD: ", all_data[file]['gen_dist'][-1],
        print " IGD: ", all_data[file]['igd'][-1]
        all_data[file]['time'] = time.time() - initial_time

        directory = 'PickleLocker_FlashB_'+str(start_size)+'_'+str(stop)
        if not os.path.exists(directory):
            os.makedirs(directory)

        import pickle
        pickle.dump(all_data, open(directory +'/' + file + '_' + str(repeat_no) + '.p', 'w'))


if __name__ == "__main__":
    files = ['SS-A', 'SS-B', 'SS-C', 'SS-D', 'SS-E', 'SS-F', 'SS-G', 'SS-H', 'SS-I', 'SS-J', 'SS-K', 'SS-L']#, 'SS-M', 'SS-N', 'SS-O']
    # files = [ 'SS-M', 'SS-N', 'SS-O']

    import multiprocessing as mp

    times = {}
    # Main control loop
    pool = mp.Pool()
    for file in files:
        times[file] = []
        for start_size in [50]:
            for rep in xrange(50):
                pool.apply_async(run_main, ([file], rep, 50, start_size))
                # start_time = time()
                # run_main([file], rep, 50, start_size)
                # times[file].append(time() - start_time)

    pool.close()
    pool.join()
