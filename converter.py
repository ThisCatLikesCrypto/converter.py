import os
import sys
import subprocess

iswindows = os.name == "nt"

ffmpegExtensions = ["mov", "mp4", "webm", "avi", "mkv", "flv", "wmv", "m4v", "f4v", "mpeg"
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
            ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', inputFile, outputFile, '-effort', str(effortLevel)],
            check=True,
            stderr=subprocess.PIPE 
        )
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
    try:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
    except IndexError:
        print("Syntax: python3 converter.py [input file name] [output file name] [ffmpeg effort level if using ffmpeg (1-7, default 4)]")
        sys.exit()
    try: effortLevel = int(sys.argv[3])
    except IndexError: effortLevel = 4
    try:
        inputExt = inputFile.split(".")[1]
        outputExt = outputFile.split(".")[1]
    except IndexError:
        print("File extension must be included in file name")
        sys.exit()
    
    print(f"Input File: {inputFile} (type {inputExt})\nOutput File: {outputFile} (type {outputExt})")

    if inputFile not in os.listdir():
        print("bruh the input file doesn't exist")
        sys.exit()
    elif outputFile in os.listdir():
        print("bruh the output file already exists")
        sys.exit()

    if inputExt.lower() in ffmpegExtensions and outputExt.lower() in ffmpegExtensions:
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
        inputFile = inputFile.split(".")[0] + ".ttf"
        outputFile = outputFile.split(".")[0] + "." + outputExt.lower()
        webifyC(inputFile, outputFile, outputExt)
        os.remove(inputFile)
    else:
        print(f"Converting {inputExt} to {outputExt} not supported.")
        sys.exit()


if __name__ == "__main__":
    main()