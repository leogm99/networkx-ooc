import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import os
from collections import defaultdict
# Step 1: Read the data from the files
n = "*"
p = "*"
file_pattern = "/home/grey/networkx/MemTesting/newResults/*.py_n_"+n+"_p_"+p+"/*/output.txt"  # Adjust the path and pattern as needed
files = glob.glob(file_pattern)

def compute_average(lst):
    return sum(lst) / len(lst) if lst else 0

count = 0
time = 0
times_dict = defaultdict(lambda: defaultdict(list))
for file in files:
    base_name = os.path.abspath(file)
    with open(file, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines) - 1):
            if "graph load done:" in lines[i]:
                time = float(lines[i + 1])
    name_part = base_name.split('/')[6].split('_p')[0]
    script_name = name_part.split('_')[0]
    n_number = name_part.split('_')[2]
    times_dict[script_name][n_number].append(time)

# for script_name, n_times in times_dict.items():
#     for n_number, times in n_times.items():
#         print(f"{script_name} - {n_number}: {times}")

averages_dict = {script_name: {n_number: compute_average(times) 
                               for n_number, times in n_times.items()} 
                 for script_name, n_times in times_dict.items()}

# Print the result
for script_name in sorted(averages_dict.keys()):
    for n_number in sorted(averages_dict[script_name].keys(), key=lambda x: int(x)):
        print(f"{script_name} - {n_number}: {averages_dict[script_name][n_number]}")