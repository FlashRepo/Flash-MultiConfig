import matplotlib.pyplot as plt
import os
import pickle
import numpy as np

pickle_folder = './Pickles/'
pickle_files = ['./Pickles/FlashB_10_50.p', './Pickles/FlashB_20_50.p', './Pickles/FlashB_30_50.p', './Pickles/FlashB_40_50.p', './Pickles/FlashB_50_50.p']

systems = ['SS-A', 'SS-B', 'SS-C', 'SS-D', 'SS-E', 'SS-F', 'SS-G', 'SS-H', 'SS-I', 'SS-J', 'SS-K', 'SS-L']

consolidated = {}
for pickle_file in pickle_files:
    consolidated[pickle_file.replace('./Pickles/FlashB_', '')] = {}
    dict = pickle.load(open(pickle_file, 'r'))
    t_igd = [np.mean([f[0] for f in dict[system]['igd']]) for system in systems]
    t_gd = [np.mean([f[0] for f in dict[system]['gen_dist']]) for system in systems]

    consolidated[pickle_file.replace('./Pickles/FlashB_', '')]['igd'] = np.mean(t_igd)
    consolidated[pickle_file.replace('./Pickles/FlashB_', '')]['gd'] = np.mean(t_gd)


x = [x.replace('.p', '').split('_')[0] for x in sorted(consolidated.keys())]
y1 = [consolidated[key]['gd'] for key in sorted(consolidated.keys())]
y2 = [consolidated[key]['igd'] for key in sorted(consolidated.keys())]



# plt.xlim(0, 60)
# plt.plot(x, y1, 'o')
# plt.savefig('gd.png')
# plt.cla()
#
# plt.xlim(0, 60)
# plt.plot(x, y2, 'o')
# plt.savefig('igd.png')
# plt.cla()

labels = ['10', '20', '30', '40', '50']
ylabel = ['', '0.008', '0.01', '0.012', '0.014', '0.016', '0.018', '0.02']
xlabel = ['', '0.0055', '0.006', '0.0065', '0.007', '0.0075']

plt.plot(y1, y2, 'o--', color='r')
for label, x, y in zip(labels, y1, y2):
    plt.annotate(
        label,
        xy=(x, y), xytext=(20, 3),
        textcoords='offset points', ha='right', va='bottom')
plt.xlabel('Generational Distance')
plt.ylabel('Inverse Generational Distance')

ax = plt.gca() # grab the current axis
ax.set_xticklabels(xlabel) # set the labels to display at those ticks
ax.set_yticklabels(ylabel) # set the labels to display at those ticks


# plt.xticks(xlabel)
# plt.yticks(ylabel)
plt.savefig('tradeoff.eps', bbox_inches='tight')
plt.cla()
# plt.show()