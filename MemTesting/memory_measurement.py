import subprocess
import psutil
import time
import sys
import os

# agregar cantidad de disco usado y de allocs

def run_and_monitor_script(script_path, output_dir):
    start_time = time.time()
    memory_usage = []

    process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process_pid = process.pid

    while process.poll() is None:
        memory_usage.append(psutil.Process(process_pid).memory_info().rss)
        time.sleep(0.01)  # Adjust the sampling interval as needed

    end_time = time.time()

    # Generate a unique output file name
    script_name = os.path.basename(script_path)
    output_file_name = f"{script_name}_output_{int(time.time())}.txt"
    output_path = os.path.join(output_dir, output_file_name)

    with open(output_path, 'x') as output_file:
        output_file.write(f'Script Name: {script_path}\n')
        output_file.write(f'Total Time: {end_time - start_time} seconds\n')
        output_file.write(f'Max Memory: {max(memory_usage)} bytes\n')
        output_file.write('Memory Usage (in bytes):\n')
        for mem in memory_usage:
            output_file.write(f'{mem}\n')

    print("Processing finished. Results saved to", output_path)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python monitoring_script.py <script_to_run.py>")
        sys.exit(1)

    script_to_run = sys.argv[1]
    output_dir = 'results/'

    run_and_monitor_script(script_to_run, output_dir)
