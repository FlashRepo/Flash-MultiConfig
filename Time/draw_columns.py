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


x1 = [t.ncolumns for t in sorted(times, key=lambda x: x.ncolumns)]

t_epal001 = [t.epal001 for t in sorted(times, key=lambda x: x.nrows)]
t_epal03 = [t.epal03 for t in sorted(times, key=lambda x: x.nrows)]
t_flash = [t.flash for t in sorted(times, key=lambda x: x.nrows)]

import matplotlib.pyplot as plt

plt.plot(x1[:-2], t_epal001[:-2], marker='o', color='b', label='epal-0.01')
plt.plot(x1[:-2], t_epal03[:-2], marker='^', color='g', label='epal-0.3')
plt.plot(x1[-3:], t_epal001[-3:], marker='o', color='b', linestyle='dashed')
plt.plot(x1[-3:], t_epal03[-3:], marker='^', color='g', linestyle='dashed', )
plt.plot(x1, t_flash, marker='+', color='r', label='Flash')
plt.yscale('log')
plt.xscale('log')
plt.xlabel('# of configuration options in log scale', fontsize=16)
plt.ylabel('Time taken in log scale (in seconds)', fontsize=16)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3, fancybox=True, frameon=False, fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.savefig('columns.eps', bbox_inches='tight')