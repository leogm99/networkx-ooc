import os
import psutil
import cProfile
import pstats
import sys
import time
import pickle

def profiled_func(frame, event, arg):
    """Function to be used as a profiler callback."""
    if event == 'call':
        func_name = frame.f_code.co_name
        mem_before = psutil.Process(os.getpid()).memory_info().rss
        func_stats[func_name]['calls'] += 1
        func_stats[func_name]['memory_allocated'] += mem_before
    elif event == 'return':
        mem_after = psutil.Process(os.getpid()).memory_info().rss
        func_name = frame.f_code.co_name
        func_stats[func_name]['memory_allocated'] = (
            mem_after - func_stats[func_name]['memory_allocated']
        )

def run_and_profile(program_name):
    # Initialize profiling
    profiler = cProfile.Profile()
    profiler.enable()

    # Run the program
    try:
        exec(open(program_name).read())
    except Exception as e:
        print(f"Error executing {program_name}: {e}")

    # Disable profiling
    profiler.disable()

    # Save profiling data
    profiler_stats = pstats.Stats(profiler)
    profiler_stats.sort_stats('cumulative')

    # Generate stats for each function
    profiler_stats.print_stats()
    profiler_stats.dump_stats('profile_data')

    # Save function stats to a file
    with open('func_stats.pkl', 'wb') as f:
        pickle.dump(func_stats, f)

    # Save function stats to a plain text file
    with open('func_stats.txt', 'w') as f:
        for func_name, stats in func_stats.items():
            f.write(f"{func_name}:\n")
            f.write(f"  Calls: {stats['calls']}\n")
            f.write(f"  Memory Allocated: {stats['memory_allocated']} bytes\n\n")

def main():
    start_time = time.time()
    
    if len(sys.argv) != 2:
        print("Usage: python script.py <program_name>")
        sys.exit(1)

    program_name = sys.argv[1]
    global func_stats
    func_stats = {}

    # Run and profile the program
    run_and_profile(program_name)

    # Load function stats from the file
    with open('func_stats.pkl', 'rb') as f:
        func_stats = pickle.load(f)

    # Print function stats
    print("\nFunction Stats:")
    for func_name, stats in func_stats.items():
        print(f"{func_name}:")
        print(f"  Calls: {stats['calls']}")
        print(f"  Memory Allocated: {stats['memory_allocated']} bytes")
        print()

    # Save function stats to a plain text file
    with open('func_stats.txt', 'w') as f:
        f.write("\nFunction Stats:\n")
        for func_name, stats in func_stats.items():
            f.write(f"{func_name}:\n")
            f.write(f"  Calls: {stats['calls']}\n")
            f.write(f"  Memory Allocated: {stats['memory_allocated']} bytes\n\n")

    # Print total execution time
    end_time = time.time()
    print(f"\nTotal Execution Time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
