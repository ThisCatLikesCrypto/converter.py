# converter.py
A simple python script to act as a 'universal converter' for file types  
Usage: ```python3 converter.py [input file] [output file]```

# dependencies
A recent python3, and ffmpeg (and Windows or Linux, I can't build for MacOS)

## installing ffmpeg
On Windows, type ```winget install ffmpeg``` into the command prompt. K-Lite Codec Pack is recommended.
Most Linux distros have ffmpeg installed by default.

# supported file types
Video: mov, mp4, avi, and webm
Audio: mp3, ogg, wav, flac, aac, wma, aiff, and m4a  
Image: jpg, jpeg, png, webp, avif, jxl, gif, bmp, svg, and tiff  
Font: ttf, woff (convert to only), woff2, eot (convert to only), svg (convert to only), otf (convert from (to eot and woff) only)