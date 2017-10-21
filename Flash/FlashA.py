from __future__ import division
from random import shuffle
import sys
from non_dominated_sort import non_dominated_sort
import math
import time
sys.path.append("/Users/viveknair/GIT/Flash-MultiConfig/")
from utility import generational_distance, inverted_generational_distance, container



lessismore = {}
lessismore["results_SS-A/"] = [False, True]
lessismore["results_SS-B/"] = [False, False]
lessismore["results_SS-C/"] = [False, True]
lessismore["results_SS-D/"] = [False, True]
lessismore["results_SS-E/"] = [False, True]
lessismore["results_SS-F/"] = [False, True]
lessismore["results_SS-G/"] = [False, True]
lessismore["results_SS-H/"] = [False, False]
lessismore["results_SS-I/"] = [False, True]
lessismore["results_SS-J/"] = [False, True]
lessismore["results_SS-K/"] = [False, True]
lessismore["results_SS-L/"] = [False, False]
lessismore["results_SS-M/"] = [True, True]
lessismore["results_SS-N/"] = [True, True]
lessismore["results_SS-O/"] = [True, True]


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


def normalize(x, min, max):
    tmp = float((x - min)) / (max - min + 0.000001)
    if tmp > 1: return 1
    elif tmp < 0: return 0
    else: return tmp


def loss(x1, x2, mins=None, maxs=None):
    # normalize if mins and maxs are given
    if mins and maxs:
        x1 = [normalize(x, mins[i], maxs[i]) for i, x in enumerate(x1)]
        x2 = [normalize(x, mins[i], maxs[i]) for i, x in enumerate(x2)]

    o = min(len(x1), len(x2))  # len of x1 and x2 should be equal
    # print x1, x2
    return sum([-1*math.exp((x2i - x1i) / o) for x1i, x2i in zip(x1, x2)]) / o


def get_cdom_values(objectives, lessismore):
    dependents = []
    for rd in objectives:
        temp = []
        for i in xrange(len(lessismore)):
            # if lessismore[i] is true - Minimization else Maximization
            if lessismore[i] is False:
                temp.append(1/rd[i])
            else:
                temp.append(rd[i])
        dependents.append(temp)

    maxs = []
    mins = []
    for i in xrange(len(objectives[0])):
         maxs.append(max([o[i] for o in dependents]))
         mins.append(min([o[i] for o in dependents]))

    cdom_scores = []
    for i, oi in enumerate(dependents):
        sum_store = 0
        for j, oj in enumerate(dependents):
            if i!=j:
                # print oi, oj, loss(oi, oj, mins, maxs), loss(oj, oi, mins, maxs)
                if loss(oi, oj, mins, maxs) < loss(oj, oi, mins, maxs):
                    sum_store += 1
        cdom_scores.append(sum_store)
    return cdom_scores


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
    for i, j in zip(predicted_objectives[0], predicted_objectives[1]):
        merged_predicted_objectves.append([i, j])
    assert(len(merged_predicted_objectves) == len(predicted_objectives[0])), "Something is wrong"

    # Find Non-Dominated Solutions
    pf_indexes = non_dominated_sort(merged_predicted_objectves, lessismore['results_' + filename + '/'])
    # print "Number of ND Solutions: ", len(pf_indexes)

    return [testing_indep[i] for i in pf_indexes], [merged_predicted_objectves[i] for i in pf_indexes]


def same_list(list1, list2):
    assert(len(list1) == len(list2)), "Something is wrong"
    for i, j in zip(list1, list2):
        if i!=j: return False
    return True


def get_training_sequence(file, training_indep, training_dep, testing_indep, index=0):
    # build a model and get the predicted non dominated solutions
    return_nd_independent, predicted_objectives = get_nd_solutions(file, training_indep, training_dep, testing_indep)
    # For ordering purposes: Add summation of continious domination
    cdom_scores = get_cdom_values(predicted_objectives, lessismore['results_' + file + '/'])
    assert(len(cdom_scores) == len(predicted_objectives)), "Something is wrong"
    training_sequence = [i[0] for i in sorted(enumerate(cdom_scores), key=lambda x:x[1], reverse=True)]
    assert(len(training_sequence) == len(cdom_scores)), "Something is wrong"
    return training_sequence, return_nd_independent


def not_in_cache(list, listoflist):
    for l in listoflist:
        if same_list(list, l) is True:
            return False
    return True

if __name__ == "__main__":
    from utility import read_file, split_data, build_model
    files = ['SS-A', 'SS-B', 'SS-C', 'SS-D', 'SS-E', 'SS-F', 'SS-G', 'SS-H', 'SS-I', 'SS-J', 'SS-K', 'SS-L', 'SS-M',
             'SS-N', 'SS-O']


    initial_sample_size = 20
    for file in files:
        all_data = {}
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


        def get_objective_score(independent):
            key = ",".join(map(str, independent))
            return objectives_dict[key]


        actual_dependent = [get_objective_score(d) for d in [d.decisions for d in data]]
        true_pf_indexes = non_dominated_sort(actual_dependent, lessismore['results_' + file + '/'])
        true_pf = sorted([actual_dependent[i] for i in true_pf_indexes], key=lambda x: x[0])

        evals = []
        pfs = []
        initial_time = time.time()
        for rep in xrange(20):
            print ". ",
            sys.stdout.flush()
            shuffle(data)

            lives = 10
            training_indep = [d.decisions for d in data[:initial_sample_size]]
            testing_indep = [d.decisions for d in data[initial_sample_size:]]
            evaluation_count = 0
            previous_pf = []

            while True:
                training_dep = [get_objective_score(r) for r in training_indep]

                training_sequence, return_nd_independent = get_training_sequence(file, training_indep, training_dep, testing_indep)
                assert(len(training_sequence) == len(return_nd_independent)), "Soemthing is wrong"

                # Since we evaluate the whole population we need to choose a point which is not
                next_point = testing_indep[training_sequence[0]]
                # print
                next_point_dependent = get_objective_score(next_point)

                # Add it to training set and see if it is a dominating point
                before_pf_indexes = non_dominated_sort(training_dep, lessismore['results_' + file + '/'])
                before_pf = [training_dep[i] for i in before_pf_indexes]

                added_training = training_indep + [next_point]

                after_pf_indexes = non_dominated_sort(training_dep + [next_point_dependent], lessismore['results_' + file + '/'])
                after_pf = [(training_dep + [next_point_dependent])[i] for i in after_pf_indexes]

                import itertools
                after_pf.sort()
                after_pf = [k for k, _ in itertools.groupby(after_pf)]

                # See if the new point is a dominant point
                previously_seen = []
                previously_not_seen = []
                for cr in after_pf:
                    seen = False
                    for pr in before_pf:
                        # Previously Seen
                        if same_list(pr, cr):
                            seen = True
                            previously_seen.append(cr)
                            continue
                    if seen is False:
                        previously_not_seen.append(cr)

                if len(previously_not_seen) == 0:
                    lives -= 1

                training_indep = training_indep + [next_point]
                del testing_indep[training_sequence[0]]

                if lives == 0: break

            # print "Size of the frontier = ", len(training_indep), " Evals: ", len(training_indep),
            # Calculate the True ND
            training_dependent = [get_objective_score(r) for r in training_indep]
            pf_indexes = non_dominated_sort(training_dependent, lessismore['results_' + file + '/'])
            current_pf = [training_dependent[i] for i in pf_indexes]
            all_data[file]['evals'].append(len(training_dependent))


            current_pf = sorted(current_pf, key=lambda x:x[0])
            from utility import draw_pareto_front
            # draw_pareto_front(actual_dependent, true_pf, current_pf)
            all_data[file]['gen_dist'].append(generational_distance(true_pf, current_pf, ranges[file]))
            all_data[file]['igd'].append(inverted_generational_distance(true_pf, current_pf, ranges[file]))

        time_required = time.time() - initial_time
        print " Time Required: ", time_required
        all_data[file]['time'] = time_required
        import pickle
        pickle.dump(all_data, open('./PickleLocker/' + file + '.p', 'w'))


        #
        #     print " GD: ",  all_data[file]['gen_dist'][-1],
        #     print " IGD: ",  all_data[file]['igd'][-1]
        #
        #
        # print [round(x, 5) for x in all_data[file]['evals']]
        # print [round(x, 5) for x in all_data[file]['gen_dist']]
        # print [round(x, 5) for x in all_data[file]['igd']]


