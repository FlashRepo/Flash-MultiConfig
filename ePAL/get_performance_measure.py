from __future__ import division
import os
import sys
import pandas as pd
sys.path.append("/Users/viveknair/GIT/Flash-MultiConfig/")
from utility import generational_distance, inverted_generational_distance, container

ranges = {}
# ranges[filename] = [[min(obj1), max(obj2)], [min(obj2), max(obj2)]]
ranges["SS-A"] =  [[288.56, 23075.0], [148.88, 9421.0]]
ranges["SS-B"] =  [[7.087462841, 16.24881706], [2.858160813, 14.71664238]]
ranges["SS-C"] =  [[121.5, 11930.0], [247.45, 57645.0]]
ranges["SS-D"] =  [[3964.2, 65823.0], [2.0815, 105000.0]]
ranges["SS-E"] =  [[5042.6, 95094.0], [1.2994, 94553.0]]
ranges["SS-F"] =  [[4275.4, 72394.0], [1.9243, 99722.0]]
ranges["SS-G"] =  [[3983.3, 63734.0], [2.1844, 93904.0]]
ranges["SS-H"] =  [[6.144515496, 9.965784285], [4.309193816, 5.123159887]]
ranges["SS-I"] =  [[2122.2, 20591.0], [47.387, 405.5]]
ranges["SS-J"] =  [[68.062, 232000.0], [1.9, 34733.0]]
ranges["SS-K"] =  [[72.75, 34740.0], [3.3172, 55209.0]]
ranges["SS-L"] =  [[199.68, 270.4], [11.0, 29.0]]


def get_evals(folder):
    """To extract the number of point in the predicted frontier and number of evaluations"""
    subfolders = [folder + subfolder + "/" for subfolder in os.listdir(folder) if os.path.isdir(folder + subfolder)]
    eval_filename = "prediction_error.csv"
    all_data = {}
    for subfolder in subfolders:
        data_dict = {}
        files = [subfolder + f for f in os.listdir(subfolder) if eval_filename not in f and 'stop' not in f and ".csv" in f]
        for file in files:
            # Extract the filename in the file path
            filename = file.split('/')[-1]
            # remove predicted_pareto from the filename
            filename = filename.replace('predicted_pareto_', '')
            # remove .csv from the filename
            filename = filename.replace('.csv', '')
            # extract the repeat number
            repeat_no = filename.split('_')[0]
            epsilon_value = filename.split('_')[1]
            content = open(file).readlines()
            number_of_lines = sum([1 for _ in content])
            if epsilon_value not in data_dict.keys():
                data_dict[epsilon_value] = container(subfolder, epsilon_value)
            data_dict[epsilon_value].append_pfs(number_of_lines)

        eval_filepath = subfolder + eval_filename
        evals_df = pd.read_csv(eval_filepath, header=None)
        # This is the format of the eval_filname: rep_iter, epsilon,num_evaluations,avg_epsilon_perc_obj1,state.
        # total_time,pop_sampled.num_entries
        repeats = evals_df[0].unique().tolist()
        epsilons = evals_df[1].unique().tolist()
        for epsilon in epsilons:
            temp_df = evals_df[evals_df[1] == epsilon]
            data_dict[str(epsilon)].set_evals(temp_df[2].tolist())

        all_data[subfolder] = data_dict

    return all_data



def process(epsilon_value, predicted_sub_folder, actual_pareto_file, range, data_dict):
    key = [k for k in data_dict.keys() if predicted_sub_folder.split('/')[-2] in k]
    assert(len(key) == 1), "Something is wrong"
    key = key[-1]
    true_pf = [map(float, line.strip().split(',')) for line in open(actual_pareto_file).readlines()]
    files = [predicted_sub_folder + f for f in os.listdir(predicted_sub_folder)]
    filtered_files = [f for f in files if str(epsilon_value) in f]
    data = {}
    data['evals'] = data_dict[key][str(epsilon_value)].evals
    data['gen_dist'] = []
    data['igd'] = []
    for f_file in filtered_files:
        predicted_pf = [map(float, line.strip().split(',')) for line in open(f_file).readlines()]
        data['gen_dist'].append(generational_distance(true_pf, predicted_pf, range))
        data['igd'].append(inverted_generational_distance(true_pf, predicted_pf, range))
    return data



if __name__ == "__main__":

    # This is to capture the number of evaluations
    folder = "./Data/"
    evals = get_evals(folder)

    # Capture the performance metrics of the solutions evaluated by ePAL.
    all_data = {}
    actual_folder = "./Actual_Frontier/"
    predicted_folder = "./Predicted_Frontier/"
    predicted_sub_folders = [predicted_folder + f + "/" for f in os.listdir(predicted_folder) if
                             "DS_Store" not in f]
    epsilon_values = [0.01, 0.2, 0.02, 0.3, 0.04, 0.08, 0.12, 0.16]
    for predicted_sub_folder in predicted_sub_folders:
        system_name = predicted_sub_folder.replace('./Predicted_Frontier/results_','').replace('/','')
        all_data[system_name] = {}
        for epsilon_value in epsilon_values:
            print ". ",
            sys.stdout.flush()
            all_data[system_name][epsilon_value] = process(epsilon_value, predicted_sub_folder,
                                                            actual_folder + system_name + '.csv',
                                                            ranges[system_name], evals)

        print
    import pickle
    pickle.dump(all_data, open('epal.p', 'w'))
