import os
import sys
import subprocess

iswindows = os.name == "nt"

ffmpegExtensions = ["mov", "mp4", "webm", "avi", "mkv", "flv", "wmv", "m4v", "f4v", "mpeg",
                    "jpg", "jpeg", "png", "webp", "jxl", "avif", "gif", "bmp", "svg", "tiff", "ico",
                    "mp3", "ogg", "wav", "flac", "aac", "wma", "aiff", "m4a", "mka", "opus", "alac"]
heifConvertInExtensions = ["heic", "heif"]
heifConvertOutExtensions = ["jpg", "png", "webp", "gif", "tiff", "bmp", "ico"]
webifyInExtensions = ["ttf", "otf"]
webifyOutExtensions = ["woff", "eot", "svg"]

# Convert files using heif-convert
def heifConvertC(inputFile: str, outputFile: str, inputExt: str, outputExt: str):
    print("\033[38;5;117mCalling heif-convert...\033[0m")
    try:
        result = subprocess.run(
            ['heif-convert', inputFile, '-f', outputExt],
            check=True, 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE 
        )

        # Check if the output file name is different, then rename it
        generatedFile = inputFile.replace(inputExt, outputExt)
        if outputFile != generatedFile:
            os.rename(generatedFile, outputFile)
        print(f"\033[38;5;120mWrote {os.path.join(os.getcwd(), outputFile)}\033[0m")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during HEIF conversion: {e.stderr.decode('utf-8')}")
    except FileNotFoundError:
        print("heif-convert is not installed or not found in the system path.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def heifConvertandFFmpegC(inputFile: str, outputFile: str, inputExt: str, outputExt: str):
    print(f"\033[38;5;117mheif-convert does not support converting to that extension, however ffmpeg does.\nConverting {inputExt} to png with heif-convert and then to {outputExt} with ffmpeg.\033[0m")
    tempfile = inputFile.replace(inputExt, "png")
    # Workaround for when there is already a file with the same name as the tempfile in the directory
    if tempfile in os.listdir():
        temperfile = tempfile.replace("png", "TEMPORARILYRENAMED.png").replace("PNG", "TEMPORARILYRENAMED.PNG")
        os.rename(tempfile, temperfile)
    else:
        temperfile = None
    heifConvertC(inputFile, tempfile, inputExt, "png")
    ffmpegC(tempfile, outputFile, 7)
    os.remove(tempfile)
    # Workaround above, pt2
    if temperfile in os.listdir():
        os.rename(temperfile, tempfile)

# Convert files using ffmpeg
def ffmpegC(inputFile, outputFile, effortLevel):
    print("\033[38;5;117mCalling ffmpeg...\033[0m")
    try:
        # Use subprocess.run to call ffmpeg
        result = subprocess.run(
            ['ffmpeg', '-hide_banner', '-i', inputFile, '-effort', str(effortLevel), outputFile],
            check=True,
            stderr=subprocess.PIPE 
        )
        print(f"\033[38;5;120mWrote {os.path.join(os.getcwd(), outputFile)}\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during conversion: {e.stderr.decode('utf-8')}")
    except FileNotFoundError:
        print("ffmpeg is not installed or not found in the system path.")

def ffmpegAV1C(inputFile, outputFile):
    print("\033[38;5;117mCalling ffmpeg...\033[0m")
    outputFile = outputFile.replace(".av1", ".webm")
    print(f"ffmpeg -i {inputFile} -c:v libaom-av1 -c:a libopus {outputFile}")
    try:
        os.system(f"ffmpeg -i {inputFile} -c:v libaom-av1 -crf 26 -c:a libopus {outputFile}")
        print(f"\033[38;5;120mWrote {os.path.join(os.getcwd(), outputFile)}\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during conversion: {e.stderr.decode('utf-8')}")
    except FileNotFoundError:
        print("ffmpeg is not installed or not found in the system path.")

# Convert files using webify
def webifyC(inputFile, outputFile, outputExt):
    oslist = os.listdir()
    if iswindows:
        os.system(f'.\win\webify.exe {inputFile}')
    else:
        os.system(f'./webify {inputFile}')
    outputName = outputFile.split(".")[0]
    inputName = inputFile.split(".")[0]
    for i in ['eot', 'woff', 'svg']:
        if i != outputExt and outputName + "." + i not in oslist:
            print("Removing " + inputName + "." + i)
            try:
                os.remove(inputName + "." + i)
            except OSError:
                pass
    if inputName != outputName:
        newSourceName = inputName + "." + outputExt
        print(f"Renaming {newSourceName} to {outputFile}")
        os.rename(newSourceName, outputFile)

# Convert files using woff2_compress
def woff2CC(inputFile, outputFile, outputExt):
    if iswindows:
        os.system(f".\win\woff2_compress.exe {inputFile}")
    else:
        os.system(f"./woff2_compress {inputFile}")
    outputName = outputFile.split(".")[0]
    inputName = inputFile.split(".")[0]
    if inputName != outputName:
        newSourceName = inputName + "." + outputExt
        print(f"Renaming {newSourceName} to {outputFile}")
        os.rename(newSourceName, outputFile)

# Convert files using woff2_decompress
def woff2CD(inputFile, outputFile, outputExt):
    if iswindows:
        os.system(f".\win\woff2_decompress.exe {inputFile}")
    else:
        os.system(f"./woff2_decompress {inputFile}")
    outputName = outputFile.split(".")[0]
    inputName = inputFile.split(".")[0]
    if inputName != outputName:
        newSourceName = inputName + "." + outputExt
        print(f"Renaming {newSourceName} to {outputFile}")
        os.rename(newSourceName, outputFile)

def main():
    # Handle command-line arguments
    try:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
    except IndexError:
        print("Syntax: python3 converter.py [input file path] [output file path] [ffmpeg effort level if using ffmpeg (1-7, default 4)]")
        sys.exit(1)

    # Handle optional effort level
    try:
        effortLevel = int(sys.argv[3])
    except IndexError:
        effortLevel = 4
    except ValueError:
        print("Effort level must be an integer between 1 and 7")
        sys.exit(1)

    try:
        inputExt = os.path.splitext(inputFile)[1][1:]  # Get extension without the dot
        outputExt = os.path.splitext(outputFile)[1][1:]
    except IndexError:
        print("File extension must be included in file name")
        sys.exit(1)
    
    print(f"Input File: {inputFile} (type {inputExt})\nOutput File: {outputFile} (type {outputExt})")

    if not os.path.isfile(inputFile):
        print("Error: The input file does not exist.")
        sys.exit(1)

    if os.path.isfile(outputFile):
        print("Error: The output file already exists.")
        sys.exit(1)

    # Process file conversion based on extensions
    if inputExt.lower() in ffmpegExtensions and outputExt.lower() == "av1":
        print("Utilising special AV1 mode: converts to AV1 with libaom-av1 and libopus")
        ffmpegAV1C(inputFile, outputFile)
    elif inputExt.lower() in ffmpegExtensions and outputExt.lower() in ffmpegExtensions:
        ffmpegC(inputFile, outputFile, effortLevel)
    elif inputExt.lower() in heifConvertInExtensions and outputExt.lower() in heifConvertOutExtensions:
        heifConvertC(inputFile, outputFile, inputExt, outputExt)
    elif inputExt.lower() in heifConvertInExtensions and outputExt.lower() in ffmpegExtensions:
        heifConvertandFFmpegC(inputFile, outputFile, inputExt, outputExt)
    elif inputExt.lower() in webifyInExtensions and outputExt.lower() in webifyOutExtensions:
        webifyC(inputFile, outputFile, outputExt)
    elif inputExt.lower() == "woff2" and outputExt.lower() == "ttf":
        woff2CD(inputFile, outputFile, outputExt)
    elif inputExt.lower() == "ttf" and outputExt.lower() == "woff2":
        woff2CC(inputFile, outputFile, outputExt)
    elif inputExt.lower() == "woff2" and outputExt.lower() in webifyOutExtensions:
        woff2CD(inputFile, outputFile, outputExt)
        inputFile = os.path.splitext(inputFile)[0] + ".ttf"
        outputFile = os.path.splitext(outputFile)[0] + "." + outputExt.lower()
        webifyC(inputFile, outputFile, outputExt)
        os.remove(inputFile)
    else:
        print(f"Converting {inputExt} to {outputExt} is not supported.")
        sys.exit(1)

if __name__ == "__main__":
    main()
