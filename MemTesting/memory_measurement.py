import subprocess
import psutil
import shutil
import time
import sys
import os

# agregar cantidad de disco usado y de allocs

def run_and_monitor_script(script_path, output_dir, n, p):
    start_time = time.time()
    memory_usage = []
    disk_usage = []
    swap_memory = []
    io_usage = []

    script_name = os.path.basename(script_path)
    
    memory_file_name = f"{script_name}_memoryResults_{int(time.time())}.txt"
    memoryOutput_path = os.path.join(output_dir, memory_file_name)

    disk_file_name = f"{script_name}_diskResults_{int(time.time())}.txt"
    diskOutput_path = os.path.join(output_dir, disk_file_name)

    io_file_name = f"{script_name}_ioResults_{int(time.time())}.txt"
    ioOutput_path = os.path.join(output_dir, io_file_name)

    swap_file_name = f"{script_name}_swapResults_{int(time.time())}.txt"
    swapOutput_path = os.path.join(output_dir, swap_file_name)
    
    stdoutFile = open(f"newResults/{script_name}_output_{int(time.time())}.txt", 'x')

    process = subprocess.Popen(['python', script_path, f"{n}", f"{p}"], stdout=stdoutFile, stderr=stdoutFile)
    process_pid = process.pid
    print(process_pid)
    cont = 0
    try:
        while process.poll() is None:
            memory_usage.append(psutil.Process(process_pid).memory_info().rss)
            swap_memory.append(psutil.swap_memory())
            disk_usage.append(shutil.disk_usage("/home/grey/networkx/MemTesting/DB"))
            cont += 1
            if not (cont%100):
                io_usage.append(psutil.Process(process_pid).io_counters())
            
            time.sleep(0.01)  # Adjust the sampling interval as needed
    except BaseException as e:
        print(e)

    end_time = time.time()

    # Generate a unique output file name


    with open(memoryOutput_path, 'x') as output_file:
        output_file.write(f'Script Name: {script_path}\n')
        output_file.write(f'Total Time: {end_time - start_time} seconds\n')
        output_file.write(f'Max Memory: {max(memory_usage)} bytes\n')
        output_file.write('Memory Usage (in bytes):\n')
        for mem in memory_usage:
            output_file.write(f'{mem}\n')

    with open(diskOutput_path, 'x') as output_file:
        output_file.write(f'Script Name: {script_path}\n')
        output_file.write(f'Total Time: {end_time - start_time} seconds\n')
        output_file.write(f'Max Memory: {max(disk_usage, key=lambda x: x[1])} bytes\n')
        output_file.write('Disk Usage:\n')
        for mem in disk_usage:
            output_file.write(f'{mem}\n')

    with open(ioOutput_path, 'x') as output_file:
        output_file.write(f'Script Name: {script_path}\n')
        output_file.write(f'Total Time: {end_time - start_time} seconds\n')
        output_file.write('IO Usage:\n')
        for mem in io_usage:
            output_file.write(f'{mem}\n')

    with open(swapOutput_path, 'x') as output_file:
        output_file.write(f'Script Name: {script_path}\n')
        output_file.write(f'Total Time: {end_time - start_time} seconds\n')
        output_file.write('Swap Usage:\n')
        for mem in swap_memory:
            output_file.write(f'{mem}\n')

    print("Processing finished. Results saved")
    time.sleep(1)

if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print("Usage: python monitoring_script.py <script_to_run.py>")
    #     sys.exit(1)

    # erdosGenerators= {(10000, 0.0005),(10000, 0.001),(100000, 0.00001),(100000, 0.000005), (1000000, 0.0000001)}

    # values = {(0, 0), (1, 1), (2, 2)}
    script_to_run = sys.argv[1]
    output_dir = 'newResults/'
    # for n,p in values:
    # run_and_monitor_script(script_to_run, output_dir, n, p)
    # n=10000
    # p=0.00005
    run_and_monitor_script(script_to_run, output_dir, 1, 1)
