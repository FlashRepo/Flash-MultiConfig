import pickle
import os

pickle_folders = [f for f in os.listdir('.') if "PickleLocker_FlashB_"  in f]

for pickle_folder in pickle_folders:

    files = ['SS-A', 'SS-B', 'SS-C', 'SS-D', 'SS-E', 'SS-F', 'SS-G', 'SS-H', 'SS-I', 'SS-J', 'SS-K', 'SS-L', 'SS-M','SS-N', 'SS-O']

    pickle_files = [pickle_folder + '/' + f  for f in os.listdir(pickle_folder)]

    dict = {}
    for file in files:
        pfiles = [ pfile for pfile in pickle_files if file in pfile]
        print file, len(pfiles)
        for i,pfile in enumerate(pfiles):
            t = pickle.load(open(pfile))
            if i == 0:
                key = t.keys()[-1]
                dict[key] = {}
                dict[key]['evals'] = [t[key]['evals']]
                dict[key]['igd'] = [t[key]['igd']]
                dict[key]['gen_dist'] = [t[key]['gen_dist']]
                dict[key]['time'] = [t[key]['time']]

            dict[key]['evals'].append(t[key]['evals'])
            dict[key]['igd'].append(t[key]['igd'])
            dict[key]['gen_dist'].append(t[key]['gen_dist'])
            dict[key]['time'].append(t[key]['time'])

    a = pickle_folder.replace('PickleLocker_FlashB_', '').split('_')[0]
    b = pickle_folder.replace('PickleLocker_FlashB_', '').split('_')[1]
    pickle.dump(dict, open('Pickles/' + 'FlashB_' + str(a) + '_' + str(50) + '.p', 'w'))
