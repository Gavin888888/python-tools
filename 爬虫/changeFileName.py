# -*- coding:utf-8 -*-
import os
import shutil
import json

jsonpath = "/Users/leili/Desktop/exportedData.json"

if __name__ == "__main__":
    f = open(jsonpath, encoding='utf-8')
    poemjson = json.load(f)
    # print(poemjson)
    data=poemjson[0]["data"]
    # print(data)
    for i in range(0, len(data)):
        categoryId=data[i]["categoryId"]
        videoId = data[i]["videoId"]
        videoName = data[i]["videoName"]
        print(videoId+"====="+categoryId)
        if categoryId=="257":
            will_file_path = "/Volumes/lilei/资源/学唐诗微信小程序/Documents/videofile/" + categoryId + "/" + videoId + ".mp4"
            dest_file_path = "/Users/leili/Desktop/upload/257/" + str(videoName) + ".mp4"
            shutil.copy(will_file_path, dest_file_path)  # copy file


    # if not os.path.exists(filepath):
    #     print("目录不存在!!")
    #     os._exit(1)
    # filenames = os.listdir(filepath)
    # for i in range(len(filenames)):
    #     filename =filenames[i]
    #     print(filename)
    #     print(i)
    #     # os.rename(filepath + '\\' + data,filepath + '\\' + newname)
    #     local_file_path = filepath+"/"+filename
    #     dst_file_path = "/Users/leili/Desktop/changeFileName/newvideos/" + str(i)+".mp4"
    #     shutil.copy(local_file_path, dst_file_path)  # copy file

