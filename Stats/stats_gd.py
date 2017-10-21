from sk import rdivDemo
import pickle
import os

locker = './PickleLocker/'
files = [locker + f for f in os.listdir(locker) if '.p' in f]
epal = pickle.load(open(locker + 'epal.p'))
f30 = pickle.load(open(locker + 'FlashB_30.p'))
f75 = pickle.load(open(locker + 'FlashB_75.p'))
f100 = pickle.load(open(locker + 'FlashB_100.p'))

f_10_50 = pickle.load(open(locker + 'FlashB_50.p'))
f_15_50 = pickle.load(open(locker + 'FlashB_15_50.p'))
f_20_50 = pickle.load(open(locker + 'FlashB_20_50.p'))
f_25_50 = pickle.load(open(locker + 'FlashB_25_50.p'))
f_30_50 = pickle.load(open(locker + 'FlashB_30_50.p'))

names = ['SS-A', 'SS-B', 'SS-C', 'SS-D', 'SS-E', 'SS-F', 'SS-G', 'SS-H', 'SS-I', 'SS-J', 'SS-K', 'SS-L']#, 'SS-M', 'SS-N', 'SS-O']

quality = 'gen_dist'
for name in names:
    e1 = ['epal-0.01'] + epal[name][0.01][quality]
    e2 = ['epal-0.3'] + epal[name][0.3][quality]
    # f1 = ['Flash30'] + [f[0] for f in f30[name][quality]]
    f20 = ['Flash50'] + [f[0] for f in f_10_50[name][quality]]
    # f3 = ['Flash75'] + [f[0] for f in f75[name][quality]]
    # f4 = ['Flash100'] + [f[0] for f in f100[name][quality]]

    f21 = ['Flash50'] + [f[0] for f in f_15_50[name][quality]]
    f22 = ['Flash50'] + [f[0] for f in f_20_50[name][quality]]
    f23 = ['Flash50'] + [f[0] for f in f_25_50[name][quality]]
    f24 = ['Flash50'] + [f[0] for f in f_30_50[name][quality]]

    print name
    # data.append([name, mean(res['rank_diff']), mean(rnk['rank_diff']), mean(flsh['rank_diff'])])
    # data.append([name, mean(res['evals']), mean(rnk['evals']), mean(flsh['evals']), sizes[name]*0.2])
    rdivDemo(name, [e1, e2, f24], globalMinMax=False, isLatex=False)