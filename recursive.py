#!/bin/python3
import os
import subprocess
import sys

def convert_file(input_file, output_file, quality):
    """
    Call the existing converter script to convert the file.
    """
    try:
        subprocess.run(['python3', 'converter.py', input_file, output_file, quality], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_file}: {e}")

def process_directory(directory, quality):
    """
    Recursively traverse the directory and convert image/video files.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            input_file = os.path.join(root, file)
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.heic')):
                output_file = os.path.splitext(input_file)[0] + '.webp'
                print(f"Converting {input_file} to {output_file} with quality {quality}")
                convert_file(input_file, output_file, quality)
            elif file.lower().endswith(('.mp4', '.mov')):
                output_file = os.path.splitext(input_file)[0] + '.av1'
                print(f"Converting {input_file} to {output_file} with quality {quality}")
                convert_file(input_file, output_file, quality)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 recursive.py <directory> <quality>")
        sys.exit(1)

    directory = sys.argv[1]
    quality = sys.argv[2]
    
    if not os.path.isdir(directory):
        print(f"The specified directory {directory} does not exist.")
        sys.exit(1)

    process_directory(directory, quality)
