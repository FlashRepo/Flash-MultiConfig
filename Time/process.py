import pickle

d = pickle.load(open('FlashB_30_50.p'))
problems = sorted(d.keys())
for problem in problems:
    print problem, sum(d[problem]['time'])
import pdb
pdb.set_trace()