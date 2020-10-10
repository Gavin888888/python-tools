import numpy as np
import cv2
import subprocess
import imageio
import os
from PIL import Image

'''
这是一个将彩色视频装换成灰度视频的代码块
'''

def video2mp3(file_name):
    """
    将视频转为音频
    :param file_name: 传入视频文件的路径
    :return:
    """
    outfile_name = file_name.split('.')[0] + '.mp3'
    subprocess.call('ffmpeg -i ' + file_name
                    + ' -f mp3 ' + outfile_name, shell=True)


def video_add_mp3(file_name, mp3_file):
    """
     视频添加音频
    :param file_name: 传入视频文件的路径
    :param mp3_file: 传入音频文件的路径
    :return:
    """
    outfile_name = file_name.split('.')[0] + '-txt.mp4'
    subprocess.call('ffmpeg -i ' + file_name
                    + ' -i ' + mp3_file + ' -strict -2 -f mp4 '
                    + outfile_name, shell=True)

# 捕获视频
old_video_name = '1.mp4'
cap = cv2.VideoCapture('/Users/leili/Desktop/wxAutoJoin/'+old_video_name)
video2mp3(file_name=old_video_name)
video_add_mp3(file_name="output1.mp4",mp3_file="1.mp4")
# 定义编解码器，创建VideoWriter 对象
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc('U', '2', '6', '3')
out = cv2.VideoWriter('/Users/leili/Desktop/wxAutoJoin/output3.mp4',fourcc, 30.0, (576,1024),False)
#（写出的文件，？？，帧率，（分辨率），是否彩色）  非彩色要把每一帧图像装换成灰度图
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        # frame = cv2.flip(frame,0)  #可以进行视频反转
        # write the flipped frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #换换成灰度图
        out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()