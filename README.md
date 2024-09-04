# converter.py
A simple python script to act as a 'universal converter' for file types  
Usage: ```python3 converter.py [input file] [output file]```

# dependencies
A recent python3  
Ffmpeg (and Windows or Linux, I can't build for MacOS)  
and ```pip install heif-convert```

## installing ffmpeg
On Windows, type ```winget install ffmpeg``` into the command prompt.  
Most Linux distros have ffmpeg installed by default.

# supported file types
Video: mov, mp4, avi, webm, mk4, flv, wmv, m4v, f4v, and mpeg  
Audio: mp3, ogg, wav, flac, aac, wma, aiff, m4a, mka, opus, and alac  
Image: jpg, jpeg, png, webp, avif, jxl, heic (convert from only), heif (convert from only), gif, bmp, svg, ico and tiff  
Font: ttf, woff (convert to only), woff2, eot (convert to only), svg (convert to only), otf (convert from (to eot and woff) only)