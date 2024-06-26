import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import os

def getAlgorithm(p):
    if p == "1":
        return "Multi Source Dijkstra"
    if p == "2":
        return "Single Source Bellman Ford"
    if p == "3":
        return "Degree Centrality"
    if p == "4":
        return "Eigenvector Centrality"
    if p == "5":
        return "Predecessor"
    if p == "6":
        return "Average Clustering"
    if p == "7":
        return "Randomized Partitioning"
    if p == "8":
        return "Center"
    if p == "9":
        return "Node Connectivity"
    if p == "10":
        return "Single Source Dijkstra"
    return "Unknown"

def match_name(name):
    new_name = ""

    if "ScriptBase" in name:
        new_name = "NX Graph"
    else:
        new_name = "OOCGraph"

    if "n_0" in name:
        new_name += " - 10 thousand nodes"
    elif "n_1" in name:
        new_name += " - 100 thousand nodes"
    elif "n_2" in name:
        new_name += " - 1 million nodes"
    elif "n_3" in name:
        new_name += " - 1.6 million nodes"
    elif "n_4" in name:
        new_name += " - 4.8 million nodes"
    
    return new_name

def main():
    # Step 1: Read the data from the files
    n = "*"
    p = "10"
    file_pattern = "newResults/*.py_n_"+n+"_p_"+p+"/*/memoryResults.txt"  # Adjust the path and pattern as needed
    files = glob.glob(file_pattern)

    # List to hold individual dataframes
    dfs = []
    count = 0
    for file in files:
        df = pd.read_csv(file, skiprows=4, header=None, names=['memory_used'])
        df['time_minutes'] = df.index * 0.01 / 60 # Create a time column assuming each measurement is 0.01 seconds apart
        base_name = os.path.abspath(file)
        name_part = base_name.split('/')[11]  + "_" + str(count)
        count+=1
        name_part = match_name(name_part) #+ "-" + str(count) 
        df['source'] = name_part  # Add a column to indicate the source file
        
        df['memory_used_MB'] = df['memory_used'] / (1024 * 1024)
        df = df.iloc[0:-20].copy()

        dfs.append(df)
        print(name_part)

    combined_df = pd.concat(dfs)

    print("start")
    # Step 3: Plot the data using Seaborn
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=combined_df, x='time_minutes', y='memory_used_MB', hue='source', palette='tab10')
    print("more")
    # plt.yscale('log')  # Set y-axis to log scale
    # plt.ylim(bottom=1)
    plt.xscale('log')  # Set y-axis to log scale
    plt.title('Memory Used by Process Over Time (Trimmed) - ' + getAlgorithm(p))
    plt.xlabel('Time (minutes)')
    plt.ylabel('Memory Used (MB)')
    plt.legend(title='Source File')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('memory_usage_plot_'+ getAlgorithm(p)+'_consolidated.png')  # Save the plot to a file
    plt.show()

if __name__ == '__main__':
    main()
