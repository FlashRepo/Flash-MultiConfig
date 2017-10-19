from __future__ import division
from non_dominated_sort import non_dominated_sort
import os
import csv


lessismore = {}
lessismore["results_SS-L/"] = [False, False]
lessismore["results_SS-H/"] = [False, False]
lessismore["results_SS-B/"] = [False, False]
lessismore["results_SS-J/"] = [False, True]
lessismore["results_SS-D/"] = [False, True]
lessismore["results_SS-E/"] = [False, True]
lessismore["results_SS-I/"] = [False, True]
lessismore["results_SS-K/"] = [False, True]
lessismore["results_SS-A/"] = [False, True]
lessismore["results_SS-C/"] = [False, True]
lessismore["results_SS-G/"] = [False, True]
lessismore["results_SS-F/"] = [False, True]

ePAL_data_folder = "./Data/"
raw_data_folder = "../Data/"

result_folders = [f+'/' for f in os.listdir(ePAL_data_folder) if '.md' not in f]
print result_folders

for result_folder in result_folders:
    print "--- " * 10
    print result_folder

    # generate a dict to assign objective values
    objective_dict = {}
    raw_filename = raw_data_folder + result_folder.replace('results_', '').replace('/', '')  + '.csv'
    assert(os.path.isfile(raw_filename) is True), "Something is wrong"

    # Read content of the raw files from raw_data_folder
    content = open(raw_filename).readlines()
    duplicate_count = 0
    for i, line in enumerate(content):
        if i == 0: continue  # Skip the first line which contains headers
        line_values = map(float, [v for v in line.strip().split(',')])
        independent_values = map(int, line_values[:-2])  # Since we only consider problems with two objectives
        dependent_values = line_values[-2:]  # Since we only consider problems with two objectives
        assert(len(independent_values) + len(dependent_values) == len(line_values)), "Something is wrong"

        independent_key = ",".join(map(str, independent_values))
        if independent_key in objective_dict.keys(): duplicate_count += 1
        objective_dict[independent_key] = dependent_values

    actual_dependent_values = [objective_dict[key] for key in objective_dict.keys()]
    actual_pf_indexes = non_dominated_sort(actual_dependent_values, lessismore[result_folder])
    actual_pf = sorted([actual_dependent_values[index] for index in actual_pf_indexes], key=lambda x:x[1], reverse=True)

    # Store Actual Pareto Data
    pf_store_filename = "./Actual_Frontier/" + result_folder.replace('results_', '').replace('/', '')  + '.csv'
    with open(pf_store_filename, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(actual_pf)


