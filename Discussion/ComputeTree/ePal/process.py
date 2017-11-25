import os

c_folder = "./Data/Data/"

result_folders = [folder[0] + "/" for folder in os.walk(c_folder) if c_folder not in folder]
for folder in result_folders:
    files = [folder + f for f in os.listdir(folder) if "_0.01.csv" not in f]
    files = [f for f in files if "_0.3.csv" not in f]
    print folder, len(files), len([f for f in os.listdir(folder)])
    for f in files:
        os.remove(f)