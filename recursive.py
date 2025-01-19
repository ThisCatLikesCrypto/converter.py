import os
import subprocess
import sys
from multiprocessing import Pool, cpu_count, Manager
import signal
import time

def convert_file(task):
    """
    Call the existing converter script to convert the file.
    """
    input_file, output_file = task
    try:
        subprocess.run(['python3', 'converter.py', input_file, output_file], check=True)
        os.remove(input_file)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_file}: {e}")

def collect_tasks(directory):
    """
    Collect all files to be converted and prepare tasks.
    """
    tasks = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            input_file = os.path.join(root, file)
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.heif', '.avif', '.bmp', '.tiff')):
                output_file = os.path.splitext(input_file)[0] + '.webp'
                print(f"Queueing conversion of {input_file} to {output_file}")
                tasks.append((input_file, output_file))
            elif file.lower().endswith(('.mp4', '.mov', '.avi', '.wmv')):
                output_file = os.path.splitext(input_file)[0] + '.av1'
                print(f"Queueing conversion of {input_file} to {output_file}")
                tasks.append((input_file, output_file))
            else:
                print(f"Skipping {input_file}")
    return tasks

def init_worker():
    """
    Initialize the worker processes with a signal handler to enable graceful shutdown.
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 recursive.py [directory]")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"The specified directory {directory} does not exist.")
        sys.exit(1)

    start_time = time.time()

    # Collect tasks for conversion
    tasks = collect_tasks(directory)

    # Determine the number of processes to use
    num_processes = min(cpu_count(), len(tasks))

    # Use a multiprocessing Pool to process files in parallel
    with Manager() as manager:
        stop_event = manager.Event()

        def graceful_exit(signum, frame):
            print("\nGraceful shutdown initiated. Waiting for processes to finish...")
            stop_event.set()
            pool.terminate()
            pool.join()
            print("All processes terminated.")
            sys.exit(0)

        signal.signal(signal.SIGINT, graceful_exit)

        with Pool(processes=num_processes, initializer=init_worker) as pool:
            try:
                pool.map(convert_file, tasks)
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt detected. Terminating pool...")
                pool.terminate()
                pool.join()

        print("All tasks completed.")
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Elapsed time: {elapsed_time} seconds")