import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import os
import re

# Step 1: Read the data from the files
n = "*"
p = "5"
file_pattern = "/home/grey/networkx/MemTesting/newResults/*.py_n_"+n+"_p_"+p+"/*/diskResults.txt"  # Adjust the path and pattern as needed
files = glob.glob(file_pattern)

# List to hold individual dataframes
dfs = []
count = 0

def parse_used_memory(line):
    match = re.search(r'used=(\d+)', line)
    return int(match.group(1)) if match else None

for file in files:

    with open(file, 'r') as f:
        lines = f.readlines()[4:]  # Skip the first 4 lines
        
    # Parse the used memory values
    used_memory = [parse_used_memory(line) for line in lines if parse_used_memory(line) is not None]
    
    # Create a dataframe
    df = pd.DataFrame(used_memory, columns=['memory_used'])
    df['time_minutes'] = df.index * 0.01 / 60 # Create a time column assuming each measurement is 0.01 seconds apart
    base_name = os.path.abspath(file)
    name_part = base_name.split('/')[6]  + "_" + str(count)
    count+=1
    df['source'] = name_part  # Add a column to indicate the source file
    initial_memory_used = df['memory_used'].iloc[0]
    df['memory_used'] = df['memory_used'] - initial_memory_used
    df['memory_used_MB'] = df['memory_used'] / (1024 * 1024)
    df = df.iloc[0:-20].copy()

    dfs.append(df)
    print(name_part)

combined_df = pd.concat(dfs)

print("start")
# Step 3: Plot the data using Seaborn
plt.figure(figsize=(14, 7))
sns.lineplot(data=combined_df, x='time_minutes', y='memory_used_MB', hue='source', palette='tab10', legend=False)
print("more")
# plt.yscale('log')  # Set y-axis to log scale
# plt.ylim(bottom=1)
plt.xscale('log')  # Set y-axis to log scale
plt.title('Memory Used by Process Over Time (Trimmed)')
plt.xlabel('Time (minutes)')
plt.ylabel('Memory Used (MB)')
# plt.legend(title='Source File')
plt.grid(True)
plt.tight_layout()
plt.savefig('disk_usage_plot_tpredecesor.png')  # Save the plot to a file
plt.show()