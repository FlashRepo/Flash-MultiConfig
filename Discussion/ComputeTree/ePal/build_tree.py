
import os,sys,math
# parentdir = os.path.dirname("/Users/viveknair/GIT/MOLearner")
# sys.path.insert(0,parentdir)
sys.path.append("/Users/viveknair/GIT/MOLearner")

from utility import read_file, lessismore, ranges


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
                temp.append(-1 * rd[i])
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




c_folder = "./Data/Data/"
gt_folder = "/Users/viveknair/GIT/MOLearner/ComputeTree/Ground_Truth/"

# result_folders = [folder[0] + "/" for folder in os.walk(c_folder) if c_folder not in folder]
result_folders = [
                 './Data/Data/results_llvm/', './Data/Data/results_noc_cm/', './Data/Data/results_rs-6d-c3/',
                  './Data/Data/results_sort_256/', './Data/Data/results_wc+rs-3d-c4/',
                  './Data/Data/results_wc+sol-3d-c4/',
                  './Data/Data/results_wc+wc-3d-c4/',
                  './Data/Data/results_wc-3d-c4/', './Data/Data/results_wc-5d-c5/', './Data/Data/results_wc-6d-c1/',
                  './Data/Data/results_wc-c1-3d-c1/', './Data/Data/results_wc-c3-3d-c1/']


for folder in result_folders:
    files = [folder + f for f in os.listdir(folder) if "_0.3" in f]
    name = files[0].split('/')[3].replace('results_', '')
    gt_file = gt_folder + name + ".csv"
    objectives_dict = {}
    data = read_file(gt_file)
    for d in data:
        key = ",".join(map(str, map(int, map(float, d.decisions))))
        objectives_dict[key] = d.objectives

    for file in files:
        print ">> ", file
        rep_no = file.split('/')[-1].split('_')[2]
        epsilon = file.split('/')[-1].split('_')[3][:-4]
        indep = []
        dep = []
        content = open(file).readlines()
        for c in content:
            indep.append(map(int, map(float, c.strip().split(';'))))
            temp = ",".join(map(str, map(int, map(float, c.strip().split(';')))))
            try:
                dep.append(objectives_dict[temp])
            except:
                import pdb
                pdb.set_trace()
        assert(len(indep) == len(dep)), "Something is wrong"

        # appropriate key for lessismore
        keys = lessismore.keys()
        if name == 'wc-3d-c4': key = "./Data/wc-3d-c4.csv"
        else:
            key = [k for k in keys if name in k.lower()]
            try:
                assert(len(key) == 1), "Something is wrong"
            except:
                import pdb
                pdb.set_trace()
            key = key[0]
        transformed_training_dep = get_cdom_values(dep, lessismore[key])
        assert(len(dep) == len(transformed_training_dep)), "Something is wrong"

        from sklearn.tree import DecisionTreeRegressor, export_graphviz
        model = DecisionTreeRegressor(min_samples_leaf=2)
        model.fit(indep, transformed_training_dep)
        tree_name = "./tree/" + name + "_" + epsilon + "_" + rep_no + '.dot'
        export_graphviz(model, out_file=tree_name)
        print tree_name






    # import pdb
    # pdb.set_trace()