# -*- coding:utf-8 -*-
import os
import json
import urllib.request

def loadFont(jsonName):
    f = open(jsonName, encoding='utf-8')
    poemjson = json.load(f)
    return poemjson["RECORDS"]


def saveImgToLocal(file_path, file_name, image_url):
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)  # 如果没有这个path则直接创建
        filename = '{}/{}'.format(file_path, file_name) +image_url[len(image_url)-4:len(image_url)]
        urllib.request.urlretrieve(image_url, filename=filename)
    except IOError as e:
        print(1, e)
    except Exception as e:
        print(2, e)

def saveAudioToLocal(file_path, file_name, image_url):
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)  # 如果没有这个path则直接创建
        filename = '{}/{}.mp3'.format(file_path, file_name)
        urllib.request.urlretrieve(image_url, filename=filename)
    except IOError as e:
        print(1, e)
    except Exception as e:
        print(2, e)

if __name__ == '__main__':
    path = "/Users/leili/Desktop/file"  #文件夹目录
    files = os.listdir(path)  #得到文件夹下的所有文件名称
    print( files)
    newdata=[]
    for filename in files:  # 遍历文件夹
        if ".html" in filename:
            print(filename)
        else:
            continue

        print("文件名="+filename)
        fopen = open(path+"/"+filename, 'r')  # r 代表read
        json_txt = json.load(fopen)
        datalist=json_txt["result"]["specialList"]["data"]
        for temp in datalist:
            saveImgToLocal(os.path.abspath('homeimg'), str(temp["id"]), temp["pic"])
            pic=temp["pic"]
            temp["pic"]="https://7072-prd-1tu5i-1300613606.tcb.qcloud.la/homeimages/"+str(temp["id"])+pic[len(pic)-4:len(pic)]
            list = temp["list"]
            newlist=[]
            for list_item in list:
                list_item_id = list_item["id"]
                list_item_pic = list_item["pic"]
                list_item_url = list_item["url"]
                saveAudioToLocal(os.path.abspath('homeaudio'), list_item_id, list_item_url)
                # saveImgToLocal(os.path.abspath('homeimg'), list_item_id, list_item_pic)
                list_item["pic"] = "https://7072-prd-1tu5i-1300613606.tcb.qcloud.la/homeimages/" + str(list_item["id"]) + list_item_pic[len(list_item_pic) - 4:len(list_item_pic)]
                list_item["url"] = "https://7072-prd-1tu5i-1300613606.tcb.qcloud.la/homeaudio/" + str(list_item["id"]) + list_item_url[len(list_item_url) - 4:len(list_item_url)]
                newlist.append(list_item)
            temp["list"]=newlist
            newdata.append(temp)
    print(newdata)
    with open(os.path.abspath('homelist.json'), "w") as f:
        json.dump(newdata, f)
    print("加载入文件完成...")