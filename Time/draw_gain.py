class container:
    def __init__(self, name, nrows, ncolumns, epal001, epal03, flash):
        self.name = name
        self.nrows = nrows
        self.ncolumns = ncolumns
        self.epal001 = epal001
        self.epal03 = epal03
        self.flash = flash


times = []
times.append(container('SS-A', 1343, 3, 65.516, 33.521, 48.735))
times.append(container('SS-B', 206, 3, 53.517, 30.048, 8.297))
times.append(container('SS-C', 1512, 3, 97.684, 48.681, 51.67))
times.append(container('SS-D', 196, 3, 75.032, 49.721, 7.425))
times.append(container('SS-E', 755, 3, 168.857, 45.183, 18.737))
times.append(container('SS-F', 195, 3, 77.1, 56.688, 6.56))
times.append(container('SS-G', 195, 3, 68, 55.379, 4.199))
times.append(container('SS-H', 258, 4, 63.159, 35.293, 7.54))
# times.append(container('SS-I', 1080, 5, 5590.371, 3845.652, 32.928))
times.append(container('SS-I', 1080, 5, 559.371, 384.652, 32.928))
times.append(container('SS-J', 3839, 6, 881.8, 271.727, 130.063))
times.append(container('SS-K', 2879, 6, 862.8, 270.086, 89.796))
times.append(container('SS-L', 1022, 11, 156.931, 68.173, 37.796))
times.append(container('SS-M', 239359, 13, 36000, 36000, 4321.571))
times.append(container('SS-N', 53661, 17, 36000, 36000, 1193.94))
times.append(container('SS-O', 65424, 59, 36000, 36000, 2174.255))


x1 = [t.nrows for t in sorted(times, key=lambda x: x.nrows)]
x2 = [t.ncolumns for t in sorted(times, key=lambda x: x.ncolumns)]

t_epal001 = [t.epal001/t.flash for t in sorted(times, key=lambda x: x.nrows)]
t_epal03 = [t.epal03/t.flash for t in sorted(times, key=lambda x: x.nrows)]
# t_flash = [t.flash for t in sorted(times, key=lambda x: x.nrows)]

import numpy as np
space = 7
ind = np.arange(space, space*(len(times)+1), space)  # the x locations for the groups
width = 1.5

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
rects1 = ax.bar(ind, t_epal001, width, color='blue', label='epal_0.01/Flash')
rects2 = ax.bar(ind + 1 * width, t_epal03, width, color='green', label='epal_0.3/Flash')

ax.plot([i for i in xrange(5, int(max(ind) *1.06))], [1 for _ in xrange(5, int(max(ind) *1.06))], linestyle='--', color='black', label='Flash')
ax.set_xticks(ind + 3*width / 2)
ax.set_xticklabels([x.name for x in times], rotation='vertical')

plt.xlim(3, 113)
plt.xlabel('Software Systems', fontsize=16)
plt.ylabel('Gain Ratio', fontsize=16)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3, fancybox=True, frameon=False, fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.savefig('gain.eps', bbox_inches='tight')