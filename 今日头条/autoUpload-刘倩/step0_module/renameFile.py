# -*- coding: utf-8 -*-
import os

def rename(path):
    files = [f for f in os.listdir(path) if not f.startswith('.')]
    print(files)
    for file in files:
        print(file)
        dir = os.path.join(path, file)
        if os.path.isdir(dir):
            rename(dir)
            continue
        file_split = file.split('集 ')
        newname = file_split[1]
        newname1 = newname.split('-少儿-')[0]
        new_dir = os.path.join(path, "儿歌：《{}》".format(newname1) + '.mp4')
        os.rename(dir, new_dir)

video_path = "{}/videos".format(os.path.dirname(__file__))
rename(video_path)