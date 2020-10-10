# -*- coding: utf-8 -*-
import shutil
import  os
import scrapy
from scrapy.selector import Selector
import json

video_categoryId = "256"

filenamejson = "./exportedData.json"
videofilepath = "/Volumes/lilei/资源/学唐诗微信小程序/Documents/videofile/"+video_categoryId
changedfilepath = "/Users/leili/Desktop/"+video_categoryId
if not os.path.exists(changedfilepath):
    os.mkdir(changedfilepath)
else:
    print(changedfilepath + '   is ok!')
if __name__ == "__main__":
    print(filenamejson + '   is ok!')
    f = open(filenamejson, encoding='utf-8')
    filenamejson = json.load(f)
    filenames = filenamejson[0]["data"]
    print(videofilepath + '   is ok!')
    if not os.path.exists(changedfilepath):
        os.mkdir(changedfilepath)
    else:
        print(changedfilepath + '   is ok!')
    print(filenamejson)
    for i in range(len(filenames)):
        categoryId = filenames[i]["categoryId"]
        if categoryId == video_categoryId :
            print(categoryId)
            videoId = filenames[i]["videoId"]
            videoName = filenames[i]["videoName"]
            local_file_path = videofilepath + "/" + str(videoId) + ".mp4"
            if os.path.exists(local_file_path):
                dst_file_path = changedfilepath + "/《" + str(videoName) + "》古诗.mp4"
                shutil.copy(local_file_path, dst_file_path)  # copy file
    # filenames = os.listdir(videofilepath)

    # for i in range(len(filenames)):
    #     filename =filenames[i]
    #     print(filename)
    #     print(i)
    #     # os.rename(filepath + '\\' + data,filepath + '\\' + newname)


