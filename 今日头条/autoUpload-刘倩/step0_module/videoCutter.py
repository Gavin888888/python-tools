# -*- coding: utf-8 -*-
import subprocess
import shutil
import shlex
import os

video_path = r'/Users/leili/Desktop/'+"256"
new_path = r'{}/newVideos'.format(video_path)

timeFromBegin = 8 # 距离文件开始起始时间
timeToEOF = 8  # 距离文件结束截止时间

if not os.path.exists(new_path):
    os.mkdir(new_path)
else:
    print(new_path + '   is ok!')

def runCommand(cmd):
    output = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # rst = output.stdout.read().decode("UTF8").strip()
    rst = output.stdout.readlines()  # .decode("UTF8").strip()
    return rst

def processVideoStripCmd():
    def secondsToString(seconds):
        strSeconds = []
        strSeconds.append(seconds // 3600)
        strSeconds.append((seconds - strSeconds[0] * 3600) // 60)
        strSeconds.append(seconds % 60)
        strSeconds = list(map(lambda x: str.format('{:02d}', x), strSeconds))
        strSeconds = ":".join(strSeconds)
        return strSeconds


    # if f.startswith('故事') and f.endswith('.mp4')
    files = [f for f in os.listdir(video_path) ]

    for f in files:
        print("----", f)
        cmd = 'ffprobe "{}"'.format(video_path+"/"+f)
        rst = runCommand(cmd)
        rst = [r.decode("UTF8").strip() for r in rst if "Duration" in r.decode("UTF8").strip()]
        print(len(rst))
        duration = ""
        validDura = 0
        if len(rst) > 0:
            start = len('Duration: ')
            duration = rst[0][start:start + 8]
            t = list(map(int, duration.split(':')))
            v = t[0] * 3600 + t[1] * 60 + t[2]
            v = v - timeFromBegin  # 开头
            v = v - timeToEOF  # 结尾
            validDura = secondsToString(v)
            print("\t 总时长:{}, 有效时长:{}".format(duration, validDura))
            print("{}/{}".format(new_path, f))
            cmd = 'ffmpeg -ss {} -i "{}" -t {} -vcodec copy -acodec copy "{}"'.format(secondsToString(timeFromBegin),
                                                                                         video_path+"/"+f, validDura,new_path+"/"+f)
            print(cmd)
            rst = runCommand(cmd)
            rst = [r.decode("UTF8").strip() for r in rst]
            os.remove(video_path+"/"+f)
            # print("\n".join(rst))
    print('共处理{}个文件'.format(len(files)))

if __name__ == "__main__":
    result = processVideoStripCmd()
    files = [f for f in os.listdir(new_path)]
    for f in files:
        shutil.copy('{}'.format(new_path + "/" + f), "/Users/leili/Desktop/13718665070/" + f)  # copy file
        os.remove(new_path + "/" + f)

