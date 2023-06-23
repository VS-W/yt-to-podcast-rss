import re, datetime
from socket import socket
from os import listdir, chdir, stat
from os.path import isfile, join
from pathlib import Path
from urllib import parse as urlparse
from xml.etree import ElementTree as xmltree
from math import floor
from mutagen.mp3 import MP3
from json import load
from traceback import print_stack, print_exc
import yt_dlp as youtube_dl

with open("options.json") as options_file:
    ydl_opts = load(options_file)

BASEPATH = ydl_opts["BASEPATH"]
PUBLICURL = ydl_opts["PUBLICURL"]
REMOVE_WORDS = ydl_opts["REMOVE_WORDS"]
CHANNELID = ydl_opts["CHANNELID"]

def download_audio(ydl_opts):
    ydl_opts["outtmpl"] = BASEPATH + "/download/" + ydl_opts["outtmpl"]

    ydl = youtube_dl.YoutubeDL(ydl_opts)
    ydl.download([CHANNELID])

def clean_files():
    for file in listdir(BASEPATH + "/download/"):
        if ('.mp3' in file):
            try:
                filename = file.strip()
                for word in REMOVE_WORDS:
                    filename = filename.replace(word, "").strip()
                filename = filename.replace("  ", " ")

                match = re.match(r"^\[\d{8}\]", filename)

                if match:
                    print(f'{filename}')
                    p = Path(BASEPATH + "/download/" + file).absolute()
                    parent_dir = p.parents[1]
                    p.rename(parent_dir / filename)
            except Exception as e:
                print("An exception occurred: ") 
                print_exc()
                print_stack()

def generate_rss():
    tree = xmltree.parse(BASEPATH + "/podcasttemplate.rss")
    root = tree.getroot()[0]

    files = [f for f in listdir(BASEPATH) if isfile(join("", f))]
    files.sort()

    for file in files:
        if (".mp3" in file):
            filename = file.split(".mp3")[0]
            fileurl = PUBLICURL + urlparse.quote(file)
            filelength = str(floor(MP3(file).info.length))
            filesize = str(stat(file).st_size)

            newitem = xmltree.Element('item')

            eltitle = xmltree.SubElement(newitem, "title")
            title = filename.split(filename.split("] ")[0])[1].strip()[2:]
            eltitle.text = title

            elenclosure = xmltree.SubElement(newitem, "enclosure")
            elenclosure.set("url", fileurl)
            elenclosure.set("type", "audio/mpeg")
            elenclosure.set("length", filesize)

            elguid = xmltree.SubElement(newitem, "guid")
            elguid.text = fileurl

            elpubDate = xmltree.SubElement(newitem, "pubDate")
            pubDateText = filename.split("] ")[0].replace("[", "").strip()
            pubDate = datetime.datetime.strptime(pubDateText, "%Y%m%d")
            elpubDate.text = f'{pubDate.strftime("%d")} {pubDate.strftime("%B")} {pubDate.strftime("%Y")} 08:00:00 -0000'

            elduration = xmltree.SubElement(newitem, "duration")
            elduration.text = filelength

            root.append(newitem)

    tree.write(BASEPATH + "/podcast.rss")

# download_audio(ydl_opts)
clean_files()
