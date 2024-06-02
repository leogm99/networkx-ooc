import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import os
# Step 1: Read the data from the files
n = "*"
p = "1"
file_pattern = "/home/grey/networkx/MemTesting/newResults/ScriptBase.py_n_"+n+"_p_"+p+"/*/memoryResults.txt"  # Adjust the path and pattern as needed
files = glob.glob(file_pattern)

# List to hold individual dataframes
dfs = []
count = 0
for file in files:
    df = pd.read_csv(file, skiprows=4, header=None, names=['memory_used'])
    df['time_minutes'] = df.index * 0.01 / 60 # Create a time column assuming each measurement is 0.01 seconds apart
    base_name = os.path.abspath(file)
    name_part = base_name.split('/')[6]  #+ "_" + str(count)
    count+=1
    df['source'] = name_part  # Add a column to indicate the source file
       # Remove the first N and last M rows
 # Adjust this part based on your filename pattern
    
# /home/grey/networkx/MemTesting/newResults/ScriptBase.py_n_1_p_4/1717058051.7639937/diskResults.txt

    # Convert memory usage to megabytes and time to minutes
    df['memory_used_MB'] = df['memory_used'] / (1024 * 1024)
    # df['time_minutes'] = df['time'] / 60
    # Append the dataframe to the list
    df = df.iloc[0:-10].copy()

    dfs.append(df)
    print(name_part)

# Step 2: Combine the data into a single DataFrame
combined_df = pd.concat(dfs)

# Define the time range to keep
# start_time = 0  # Adjust as needed
# end_time = combined_df['time'].max() - 1  # Adjust as needed

# # Filter the data to keep only the relevant part
# filtered_df = combined_df.loc[(combined_df['time'] >= start_time) & (combined_df['time'] <= end_time)].copy()

# # Convert memory usage to megabytes and time to minutes
# filtered_df.loc[:, 'memory_used_MB'] = filtered_df['memory_used'] / (1024 * 1024)
# filtered_df.loc[:, 'time_minutes'] = filtered_df['time'] / 60
print("start")
# Step 3: Plot the data using Seaborn
plt.figure(figsize=(14, 7))
sns.lineplot(data=combined_df, x='time_minutes', y='memory_used_MB', hue='source', palette='tab10')
print("more")
# plt.yscale('log')  # Set y-axis to log scale
# plt.ylim(bottom=1)
plt.xscale('log')  # Set y-axis to log scale
plt.title('Memory Used by Process Over Time (Trimmed)')
plt.xlabel('Time (minutes)')
plt.ylabel('Memory Used (MB)')
plt.legend(title='Source File')
plt.grid(True)
plt.tight_layout()
plt.savefig('memory_usage_plot_trimmed_mb_1_all_cons.png')  # Save the plot to a file
plt.show()
print("Plot saved as memory_usage_plot_trimmed_log_mb.png")