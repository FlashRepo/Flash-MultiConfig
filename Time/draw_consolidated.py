import matplotlib.pyplot as plt

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




left, width = .53, .5
bottom, height = .25, .5
right = left + width
top = bottom + height

f, ((ax1, ax2, ax3)) = plt.subplots(1, 3)

x1 = [t.nrows for t in sorted(times, key=lambda x: x.nrows)]

t_epal001 = [t.epal001 for t in sorted(times, key=lambda x: x.nrows)]
t_epal03 = [t.epal03 for t in sorted(times, key=lambda x: x.nrows)]
t_flash = [t.flash for t in sorted(times, key=lambda x: x.nrows)]

ax1.plot(x1[:-2], t_epal001[:-2], marker='o', color='b', label='epal-0.01')
ax1.plot(x1[:-2], t_epal03[:-2], marker='^', color='g', label='epal-0.3')
ax1.plot(x1[-3:], t_epal001[-3:], marker='o', color='b', linestyle='dashed')
ax1.plot(x1[-3:], t_epal03[-3:], marker='^', color='g', linestyle='dashed', )
ax1.plot(x1, t_flash, marker='+', color='r', label='Flash')
ax1.set_yscale('log')
ax1.set_xscale('log')
ax1.set_xlabel('# of configurations in log scale', fontsize=16)
ax1.set_ylabel('Time taken in log scale (in seconds)', fontsize=16)
ax1.tick_params(axis='both', which='major', labelsize=16)

x1 = [t.ncolumns for t in sorted(times, key=lambda x: x.ncolumns)]

ax2.plot(x1[:-2], t_epal001[:-2], marker='o', color='b', label='epal-0.01')
ax2.plot(x1[:-2], t_epal03[:-2], marker='^', color='g', label='epal-0.3')
ax2.plot(x1[-3:], t_epal001[-3:], marker='o', color='b', linestyle='dashed')
ax2.plot(x1[-3:], t_epal03[-3:], marker='^', color='g', linestyle='dashed', )
ax2.plot(x1, t_flash, marker='+', color='r', label='Flash')
ax2.set_yscale('log')
ax2.set_xscale('log')
ax2.set_xlabel('# of configuration options in log scale', fontsize=16)
ax2.set_ylabel('Time taken in log scale (in seconds)', fontsize=16)



t_epal001 = [t.epal001/t.flash for t in sorted(times, key=lambda x: x.nrows)]
t_epal03 = [t.epal03/t.flash for t in sorted(times, key=lambda x: x.nrows)]
# t_flash = [t.flash for t in sorted(times, key=lambda x: x.nrows)]

import numpy as np
space = 7
ind = np.arange(space, space*(len(times)+1), space)  # the x locations for the groups
width = 1.5

rects1 = ax3.bar(ind, t_epal001, width, color='blue', label='epal_0.01')
rects2 = ax3.bar(ind + 1 * width, t_epal03, width, color='green', label='epal_0.3')

ax3.plot([i for i in xrange(5, int(max(ind) *1.06))], [1 for _ in xrange(5, int(max(ind) *1.06))], linestyle='--', color='black', label='Flash')
ax3.set_xticks(ind + 3*width / 2)
ax3.set_xticklabels([x.name for x in times], rotation='vertical')

ax3.set_xlim(3, 113)
ax3.set_xlabel('Software Systems', fontsize=16)
ax3.set_ylabel('Gain Ratio', fontsize=16)
ax3.legend(loc='upper center', bbox_to_anchor=(0.5, 1.12), ncol=3, fancybox=True, frameon=False, fontsize=14)
ax3.tick_params(axis='both', which='major', labelsize=16)


from matplotlib.lines import Line2D

circ1 = Line2D([0], [0], linestyle="none", marker="o", markersize=10, color="b")
circ2 = Line2D([0], [0], linestyle="none", marker="^", markersize=10, color="g")
circ3 = Line2D([0], [0], linestyle="none", marker="+", markersize=10, color="r")

plt.figlegend((circ1, circ2, circ3), ('ePal-0.01', 'ePal-0.3', 'Flash'), frameon=False, loc='upper center',
              bbox_to_anchor=(0.3, 1.09),fancybox=True, ncol=3)
f.set_size_inches(18, 5)
plt.savefig('time_consolidated.eps', bbox_inches='tight')
