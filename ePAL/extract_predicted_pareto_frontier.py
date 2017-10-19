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

result_folders = [f for f in os.listdir(ePAL_data_folder) if '.md' not in f]
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
    pf_store_filename = "./Actual_Pareto_Data/" + result_folder.replace('results_', '').replace('/', '')  + '.csv'
    with open(pf_store_filename, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(actual_pf)
    #
    # # find the objective scores of the pareto front extracted by epal
    # pareto_files = [pareto_data_folder + result_folder + f for f in os.listdir(pareto_data_folder + result_folder) if "prediction_error" not in f and 'stop' not in f and ".csv" in f]
    # for pareto_file in pareto_files:
    #     print ". ",pareto_file
    #     sys.stdout.flush()
    #     pareto_content = open(pareto_file).readlines()
    #     assert(len(content) >= len(pareto_content)), "Something is wrong"
    #     predicted_pareto_front = []
    #     for pc in pareto_content:
    #         pc_value = map(int, map(float, pc.strip().split(';')))
    #         pareto_key = ",".join(map(str, pc_value))
    #         predicted_pareto_front.append(objective_dict[pareto_key])
    #     assert(len(predicted_pareto_front) == len(pareto_content)), "Something is wrong"
    #
    #     nd_pf_indexes = non_dominated_sort(predicted_pareto_front, lessismore[result_folder])
    #     nd_pf = sorted([predicted_pareto_front[index] for index in nd_pf_indexes], key=lambda x:x[1], reverse=True)
    #     import matplotlib.pyplot as plt
    #     plt.scatter([np.log(d[0]) for d in actual_dependent_values], [np.log(d[1]) for d in actual_dependent_values], color='r')
    #     l1, = plt.plot([np.log(p[0]) for p in nd_pf], [np.log(p[1]) for p in nd_pf], color='black', marker='x', label="Predicted-PF")
    #     l2, = plt.plot([np.log(p[0]) for p in actual_pf], [np.log(p[1]) for p in actual_pf], color='green', marker='o', label="Actual-PF")
    #     plt.xlabel('log(f1)')
    #     plt.ylabel('log(f2)')
    #     plt.legend(loc=2)
    #     figure_name = "./Figures/" +  "/".join(pareto_file.split('/')[2:])[:-3] + "jpg"
    #     intermediate_folders = "/".join(figure_name.split('/')[:-1]) + "/"
    #     try:
    #         os.makedirs(intermediate_folders)
    #     except:
    #         pass
    #     plt.savefig(figure_name)
    #     plt.cla()
    #
    #     # Store Predicted Pareto Data
    #     pf_store_filename = "./Predicted_Pareto_Data/" +  "/".join(pareto_file.split('/')[2:])
    #     intermediate_folders = "/".join(pf_store_filename.split('/')[:-1]) + "/"
    #     try:
    #         os.makedirs(intermediate_folders)
    #     except:
    #         pass
    #     with open(pf_store_filename, "wb") as f:
    #         writer = csv.writer(f)
    #         writer.writerows(nd_pf)
    #
    #
    # print

