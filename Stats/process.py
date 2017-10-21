import pickle
import numpy as np


pickle_locker = "./PickleLocker/"
pickle_files = ['epal.p', 'FlashB_100.p', 'FlashB_15_50.p', 'FlashB_20_50.p', 'FlashB_25_50.p', 'FlashB_30.p', 'FlashB_30_50.p', 'FlashB_50.p', 'FlashB_75.p']


files = ['SS-A', 'SS-B', 'SS-C', 'SS-D', 'SS-E', 'SS-F', 'SS-G', 'SS-H', 'SS-I', 'SS-J', 'SS-K', 'SS-L', 'SS-M', 'SS-N', 'SS-O']

quality = 'gen_dist'

for file in files:
    print file,
    for pfile in pickle_files:
        dict = pickle.load(open(pickle_locker + pfile))
        if pfile == 'epal.p':
            try:
                print np.median(dict[file][0.01][quality]), np.median(dict[file][0.3][quality]),
            except: print 'X X ',
        else:
            print np.median([d[0] for d in dict[file][quality]]),
    print

