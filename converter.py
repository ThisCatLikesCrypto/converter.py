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
    FORCE_OSSYSTEM_FFMPEG_AV1 = False
    try:
        if FORCE_OSSYSTEM_FFMPEG_AV1 == True:
            os.system(f"ffmpeg -i {inputFile} -c:v libaom-av1 -crf 26 -c:a libopus {outputFile}")
        else:
            result = subprocess.run(
            ['ffmpeg', '-hide_banner', '-i', inputFile, '-c:v', 'libaom-av1', '-crf', '26', '-c:a', 'libopus', outputFile],
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
        os.system(f'.\\win\\webify.exe {inputFile}')
    else:
        os.system(f'./bin/webify {inputFile}')
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
        os.system(f".\\win\\woff2_compress.exe {inputFile}")
    else:
        os.system(f"./bin/woff2_compress {inputFile}")
    outputName = outputFile.split(".")[0]
    inputName = inputFile.split(".")[0]
    if inputName != outputName:
        newSourceName = inputName + "." + outputExt
        print(f"Renaming {newSourceName} to {outputFile}")
        os.rename(newSourceName, outputFile)

# Convert files using woff2_decompress
def woff2CD(inputFile, outputFile, outputExt):
    if iswindows:
        os.system(f".\\win\\woff2_decompress.exe {inputFile}")
    else:
        os.system(f"./binwoff2_decompress {inputFile}")
    outputName = outputFile.split(".")[0]
    inputName = inputFile.split(".")[0]
    if inputName != outputName:
        newSourceName = inputName + "." + outputExt
        print(f"Renaming {newSourceName} to {outputFile}")
        os.rename(newSourceName, outputFile)

def _is_problematic_path(path: str) -> bool:
    # Consider spaces and shell-significant characters problematic for os.system calls.
    specialChars = ' !@#$%^&*+{}|:<>?,;[]\'"`'
    return any(ch in path for ch in specialChars)

def _make_safe_name(path: str) -> str:
    # Create a safe filename in the same directory, avoiding spaces and special chars.
    dirn, basen = os.path.split(path)
    name, ext = os.path.splitext(basen)
    safe_base = ''.join(ch if ch.isalnum() or ch in ('-', '_', '.') else '_' for ch in name)
    # Prefix to avoid collisions and indicate temporary nature.
    safe_basen = f"{safe_base}__safe{ext}"
    safe_path = os.path.join(dirn or ".", safe_basen)
    # Ensure uniqueness
    counter = 1
    while os.path.exists(safe_path):
        safe_basen = f"{safe_base}__safe_{counter}{ext}"
        safe_path = os.path.join(dirn or ".", safe_basen)
        counter += 1
    return safe_path

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

    # Prepare safe temporary names if necessary
    originalInput = inputFile
    originalOutput = outputFile

    tempInput = inputFile
    tempOutput = outputFile

    needTempInput = _is_problematic_path(inputFile)
    needTempOutput = _is_problematic_path(outputFile)

    if needTempInput:
        tempInput = _make_safe_name(inputFile)
        print(f"Renaming input to safe temporary name: {tempInput}")
        os.rename(inputFile, tempInput)

    if needTempOutput:
        # Generate a safe output path in the same directory
        tempOutput = _make_safe_name(outputFile)

    print(tempInput)
    print(tempOutput)

    # Process file conversion based on extensions, using safe temp paths
    if inputExt.lower() in ffmpegExtensions and outputExt.lower() == "av1":
        print("Utilising special AV1 mode: converts to AV1 with libaom-av1 and libopus")
        ffmpegAV1C(tempInput, tempOutput)
    elif inputExt.lower() in ffmpegExtensions and outputExt.lower() in ffmpegExtensions:
        ffmpegC(tempInput, tempOutput, effortLevel)
    elif inputExt.lower() in heifConvertInExtensions and outputExt.lower() in heifConvertOutExtensions:
        heifConvertC(tempInput, tempOutput, inputExt, outputExt)
    elif inputExt.lower() in heifConvertInExtensions and outputExt.lower() in ffmpegExtensions:
        heifConvertandFFmpegC(tempInput, tempOutput, inputExt, outputExt)
    elif inputExt.lower() in webifyInExtensions and outputExt.lower() in webifyOutExtensions:
        webifyC(tempInput, tempOutput, outputExt)
    elif inputExt.lower() == "woff2" and outputExt.lower() == "ttf":
        woff2CD(tempInput, tempOutput, outputExt)
    elif inputExt.lower() == "ttf" and outputExt.lower() == "woff2":
        woff2CC(tempInput, tempOutput, outputExt)
    elif inputExt.lower() == "woff2" and outputExt.lower() in webifyOutExtensions:
        woff2CD(tempInput, tempOutput, outputExt)
        tempInput = os.path.splitext(tempInput)[0] + ".ttf"
        tempOutput = os.path.splitext(tempOutput)[0] + "." + outputExt.lower()
        webifyC(tempInput, tempOutput, outputExt)
    else:
        print(f"Converting {inputExt} to {outputExt} is not supported.")
        # Restore original input name if we changed it
        if needTempInput and os.path.exists(tempInput) and not os.path.exists(originalInput):
            os.rename(tempInput, originalInput)
        sys.exit(1)

    # After conversion: move safe temp output to the requested output path
    try:
        # ffmpegAV1C may change extension to .webm; handle that when tempOutput differs by extension
        if not os.path.exists(tempOutput):
            # Try to find generated file with possibly altered extension
            tempBase = os.path.splitext(tempOutput)[0]
            candidates = [p for p in os.listdir(os.path.dirname(tempOutput) or ".")
                          if os.path.splitext(p)[0] == os.path.basename(tempBase)]
            for cand in candidates:
                candPath = os.path.join(os.path.dirname(tempOutput) or ".", cand)
                if os.path.isfile(candPath):
                    tempOutput = candPath
                    break

        if os.path.abspath(tempOutput) != os.path.abspath(originalOutput):
            print(f"Renaming output to requested name: {originalOutput}")
            os.rename(tempOutput, originalOutput)
    except Exception as e:
        print(f"Failed to finalize output file name: {e}")

    # Restore original input filename if it was temporarily changed
    try:
        if needTempInput and os.path.exists(tempInput) and not os.path.exists(originalInput):
            print(f"Restoring original input filename: {originalInput}")
            os.rename(tempInput, originalInput)
    except Exception as e:
        print(f"Failed to restore original input filename: {e}")

if __name__ == "__main__":
    main()
