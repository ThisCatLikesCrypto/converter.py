import os
import subprocess
import sys

def convert_file(input_file, output_file):
    """
    Call the existing converter script to convert the file.
    """
    try:
        subprocess.run(['python3', 'converter.py', input_file, output_file], check=True)
        os.remove(input_file)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_file}: {e}")

def process_directory(directory):
    """
    Recursively traverse the directory and convert image/video files.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            input_file = os.path.join(root, file)
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.heic')):
                output_file = os.path.splitext(input_file)[0] + '.webp'
                print(f"Converting {input_file} to {output_file}")
                convert_file(input_file, output_file)
            elif file.lower().endswith(('.mp4', '.mov', '.webm', '.avi', '.wmv')):
                output_file = os.path.splitext(input_file)[0] + '.av1'
                print(f"Converting {input_file} to {output_file}")
                convert_file(input_file, output_file)
            else:
                print(f"Skipping {input_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 recursive.py [directory]")
        sys.exit(1)

    directory = sys.argv[1]
    
    if not os.path.isdir(directory):
        print(f"The specified directory {directory} does not exist.")
        sys.exit(1)

    process_directory(directory)
