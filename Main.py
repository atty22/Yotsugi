#!/bin/python
from glob import glob
from os import chdir, path, rename, remove
from subprocess import run
from requests import post
from telegraph import Telegraph
from platform import system

print('''
Unlimited Rulebook.

This program need imagick, you can download it from :
Arch:  sudo pacman -S imagemagick
Debian: sudo apt install imagemagick
Windows:
https://download.imagemagick.org/ImageMagick/download/binaries/ImageMagick-7.0.11-12-Q16-HDRI-x64-dll.exe

This program will convert all your png or jpeg image to jpg before upload it on telegraph

- Yotsugi Ononoki by
      .o.           .       .                 .oooo.   
     .888.        .o8     .o8               .dP""Y88b  
    .8"888.     .o888oo .o888oo oooo    ooo       ]8P' 
   .8' `888.      888     888    `88.  .8'      .d8P'  
  .88ooo8888.     888     888     `88..8'     .dP'     
 .8'     `888.    888 .   888 .    `888'    .oP     .o 
o88o     o8888o   "888"   "888"     .8'     8888888888 
                                .o..P'                 
                                `Y8P'                  
''')
# input
title = ""
while len(title) == 0:
    title = input("Title: ")

chdir(input('Folder: ').replace("\\", "\\").replace('"', '').replace("'", "\'"))

# define variable
nlist = []
listo = []
nfilework = 0
html = '''<p>{}</p>
'''.format(input("Initial Text:"))
edtext = '''<p>{}</p>
'''.format(input("Ending Text:"))
ordfile = []
telegraph = Telegraph()
telegraph.create_account(short_name="Yotsugi")

# convert png to jpg, and rename jpeg to jpg
print("Converting file")
if system() == 'Windows':
    for i in glob("*.png"):
        print("Converting: ", i)
        run(str("magick.exe mogrify -format jpg  -quality 89 " + i), shell=True)
        remove(i)
elif system() == 'Linux':
    for i in glob("*.png"):
        print("Converting: ", i)
        run(str("mogrify -format jpg  -quality 89 " + i), shell=True)
        remove(i)
else:
    print("I'm not compatible with your system")

for i in glob("*.jpeg"):
    rename(i, str(path.splitext(i)[0] + ".jpg"))

# learn file structure
listfile = glob("*.jpg")
prefix = path.commonprefix(listfile)
print("common prefix: ", prefix)
number0 = len(str(path.splitext(listfile[0])[0][len(prefix):]))
for item in listfile:
    nlist.append(str(path.splitext(item)[0][len(prefix):]))  # convert str file name in int to sort
nlist.sort(key=int)
for itemd in nlist:
    while len(itemd) != number0:
        itemd = "0" + itemd
    file = str(prefix + itemd + ".jpg")  # recreate original file name
    with open(file, 'rb') as f:
        html += "<img src='{}'/>".format(post('https://telegra.ph/upload',
                                              files={'file': ('file', f, 'image/jpeg')}).json()[0]['src'])
    nfilework += 1  # for cli GUI
    print(file, "    Uploaded    ", nfilework, "/", len(nlist), "    ", int(nfilework / len(nlist) * 100), "%")
    # for cli GUI
html += edtext
html += "<p>Upload with Yotsugi by @atty2</p>"
response = telegraph.create_page(title, html_content=html)
print('''
http://telegra.ph/{}'''.format(response['path']))
