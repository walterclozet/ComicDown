# ComicDown
A simple python script to down load comic images to e:\Comic, this means is tool is currently windows only.

This tool requires Pillow, PyV8, json to download comics from web including:
733dm
manhuagui
dmzj
tencent comic
163 comic

The default download location is e:\comic, create it first. If you want your own location, open comicdown.py, change value of comic_dest_dir.
It's tested on windows python 2.7 but it sould support python3 and linux/mac os if you change the download dest path to linux path.

Usage:
Start the comic.py, it will ask for comic id. usually this is the last part of the url for the comic. it will search all sites for matching results, and display them.
Select one by entering the number of the comic, it will download all chapters to the dest path, the folder will be book_<id>, id the the comic id you entered.
Files will be renamed to P_(xxx), xxx is number of images from 000 to 999. To upload them to vol site, please use comicrepack tool.
