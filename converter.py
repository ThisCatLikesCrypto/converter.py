import os
import sys
import platform

iswindows = platform.uname().system.startswith('Win')

ffmpegExtensions = ["mov", "mp4", "webm", "avi", 
                    "jpg", "jpeg", "png", "webp", "jxl", "avif", "gif", "bmp", "svg", "tiff",
                    "mp3", "ogg", "wav", "flac", "aac", "wma", "aiff", "m4a"]
webifyInExtensions = ["ttf", "otf"]
webifyOutExtensions = ["woff", "eot", "svg"]

def ffmpegC(inputFile, outputFile):
    os.system(f'ffmpeg -i {inputFile} {outputFile}')

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
        print("Syntax: python3 converter.py [input file name] [output file name]")
        sys.exit()
    try:
        inputExt = inputFile.split(".")[1]
        outputExt = outputFile.split(".")[1]
    except IndexError:
        print("File extension must be included in file name")
        sys.exit()
    
    print(f"Input File: {inputFile} (type {inputExt})\nOutput File: {outputFile} (type {outputExt})")

    if inputExt.lower() in ffmpegExtensions and outputExt.lower() in ffmpegExtensions:
        ffmpegC(inputFile, outputFile)
    elif inputExt.lower() == "woff":
        print("fuck")
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
    print("\033[38;5;120mConverted!\033[0m")


if __name__ == "__main__":
    main()