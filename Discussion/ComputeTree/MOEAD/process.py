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
        indep.append(map(float, temp[:d]))
        dep.append(map(float, temp[d:]))
        assert(len(indep[-1]) + len(dep[-1]) == len(temp)), "Something is wrong"
    return indep, dep

def collect_all_points(subdir, decisions, objectives):
    indeps = []
    deps = []
    repeats = [subdir + f for f in os.listdir(subdir) if ".DS_Store" not in f]
    for repeat in repeats:
        # print repeat
        t_indep, t_dep = read_file(repeat, decisions, objectives)
        indeps += t_indep
        deps += t_dep
    return indeps, deps

def parallelize(subdir, name, rep_no, decisions, objectives):
    print subdir, name, rep_no
    indeps, deps = collect_all_points(subdir, decisions, objectives)
    keys = lessismore.keys()

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
    tree_name = "./tree/" + name + "_" + str(rep_no) + '.dot'
    export_graphviz(model, out_file=tree_name)
    print tree_name

def run():
    dirs = ["./Data/" + f + "/" for f in os.listdir("./Data") if ".DS_Store" not in f]

    pom_dirs = [f for f in dirs if "POM" in f]
    monrp_dirs = [f for f in dirs if "MONRP" in f]
    xomo_dirs = ['./Data/MOEAD_xomoo2_100/', './Data/MOEAD_xomo_all_100/', './Data/MOEAD_xomo_flight_100/', './Data/MOEAD_xomo_ground_100/', './Data/MOEAD_xomo_osp_100/', ]


    assert(len(pom_dirs) + len(monrp_dirs) + len(xomo_dirs) == len(dirs)), "Something is wrong"
    import multiprocessing as mp
    # Main control loop
    pool = mp.Pool()
    # for pom_dir in pom_dirs:
    #     name = pom_dir.split('/')[2].split('_')[1].lower()
    #     subdirs = [pom_dir + f + "/" for f in os.listdir(pom_dir) if ".DS_Store" not in f]
    #     for rep_no, subdir in enumerate(subdirs):
    #         pool.apply_async(parallelize, (subdir, name, rep_no))
    #         # parallelize(subdir, name, rep_no, 9, 3)

    # for monrp_dir in monrp_dirs:
    #     name = '_'.join(monrp_dir.split('/')[2].split('_')[1:7])
    #     subdirs = [monrp_dir + f + "/" for f in os.listdir(monrp_dir) if ".DS_Store" not in f]
    #     for rep_no, subdir in enumerate(subdirs):
    #         pool.apply_async(parallelize, (subdir, name, rep_no, 50, 3))
    #         # parallelize(subdir, name, rep_no, 50, 3)

    for xomo_dir in xomo_dirs:
        if "xomoo2" in xomo_dir:
            name = "xomoo2"
        else:
            name = '_'.join(xomo_dir.split('/')[2].split('_')[1:3])
        subdirs = [xomo_dir + f + "/" for f in os.listdir(xomo_dir) if ".DS_Store" not in f]
        for rep_no, subdir in enumerate(subdirs):
            pool.apply_async(parallelize, (subdir, name, rep_no, 27, 4))
            # parallelize(subdir, name, rep_no, 27, 4)

    pool.close()
    pool.join()


run()