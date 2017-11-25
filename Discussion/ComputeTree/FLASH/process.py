import os

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



def read_file(file, d, o):
    content = open(file).readlines()
    indep = []
    dep = []
    for c in content:
        temp = c.split(',')
        indep.append(map(float, temp[:-1*o]))
        dep.append(map(float, temp[-1*o:]))
        assert(len(indep[-1]) + len(dep[-1]) == len(temp)), "Something is wrong"
    return indep, dep

def collect_all_points(filename, decisions, objectives):
    indeps = []
    deps = []
    # print repeat
    t_indep, t_dep = read_file(filename, decisions, objectives)
    indeps += t_indep
    deps += t_dep
    return indeps, deps


def run():
    problems = [
        'llvm_input', 'noc_CM_log',
        'sort_256',
        'wc+rs-3d-c4', 'wc+sol-3d-c4', 'wc+wc-3d-c4',
        'wc-3d-c4', 'wc-5d-c5', 'wc-6d-c1', 'wc-c1-3d-c1',
        'wc-c3-3d-c1', 'rs-6d-c3'
                ]



    for problem in problems:
        print ">>> ", problem
        if problem == 'wc-3d-c4':
            files = ["./Data/" + f for f in os.listdir("./Data") if problem in f]
            files = [f for f in files if '+' not in f]
        else:
            files = ["./Data/" + f for f in os.listdir("./Data") if problem in f]
        assert(len(files) == 20), "Somethign is wrong"
        for file in files:
            # if "POM" in file:
            #     name = file.split('/')[-1].split('_')[0]
            #     indeps, deps = collect_all_points(file, 9, 3)
            # elif "xomo" in file:
            #     if "xomoo2" in file:
            #         name = "xomoo2"
            #     else:
            #         name = "_".join(file.split('/')[-1].split('_')[:2])
            #     indeps, deps = collect_all_points(file, 27, 4)
            # elif "MONRP" in file:
            #     name = "_".join(file.split('/')[-1].split('_')[:6])
            #     indeps, deps = collect_all_points(file, 50, 3)
            name = file.split('/')[-1].split('_')[0]
            indeps, deps = collect_all_points(file, None, 2)

            keys = lessismore.keys()
            if name == 'wc-3d-c4':
                key = [k for k in keys if name in k]
                key = [k for k in key if '+' not in k]
            else:
                key = [k for k in keys if name in k]
            try:
                assert (len(key) == 1), "Something is wrong"
            except:
                import pdb
                pdb.set_trace()
            key = key[0]

            transformed_training_dep = get_cdom_values(deps, lessismore[key])
            assert (len(deps) == len(transformed_training_dep)), "Something is wrong"

            from sklearn.tree import DecisionTreeRegressor, export_graphviz
            model = DecisionTreeRegressor(min_samples_leaf=2)
            model.fit(indeps, transformed_training_dep)
            tree_name = "./tree/" + file.split('/')[-1][:-4] + '.dot'
            export_graphviz(model, out_file=tree_name)
            print tree_name

run()