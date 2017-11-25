import os
import numpy as np

folders = ['MOEAD_MONRP_50_4_5_0_110_100', 'MOEAD_MONRP_50_4_5_0_90_100', 'MOEAD_MONRP_50_4_5_4_110_100', 'MOEAD_MONRP_50_4_5_4_90_100', 'MOEAD_POM3A_100', 'MOEAD_POM3B_100', 'MOEAD_POM3C_100', 'MOEAD_POM3D_100', 'MOEAD_xomo_all_100', 'MOEAD_xomo_flight_100', 'MOEAD_xomo_ground_100', 'MOEAD_xomo_osp_100', 'MOEAD_xomoo2_100']

for folder in folders:
    repeat_folders = [folder + "/" + f + "/" for f in os.listdir(folder) if ".DS_Store" not in f]
    evals = []
    for repeat_folder in repeat_folders:
        files = [repeat_folder + f for f in os.listdir(repeat_folder)]
        t_evals = 0
        for file in files:
            lines_seen = set()  # holds lines already seen
            for line in open(file, "r"):
                if line not in lines_seen:  # not a duplicate
                    t_evals += 1
                    lines_seen.add(line)
        evals.append(t_evals)
    print folder, np.median(evals)
