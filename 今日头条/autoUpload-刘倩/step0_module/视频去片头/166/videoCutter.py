# -*- coding: utf-8 -*-
import subprocess
import shlex
import os

new_path = r'./newVideos'
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

    timeFromBegin = 8  # 距离文件开始起始时间
    timeToEOF = 0  # 距离文件结束截止时间
    # if f.startswith('故事') and f.endswith('.mp4')
    files = [f for f in os.listdir('.') ]

    for f in files:
        print("----\n", f)
        cmd = 'ffprobe "{}"'.format(f)
        rst = runCommand(cmd)
        rst = [r.decode("UTF8").strip() for r in rst if "Duration" in r.decode("UTF8").strip()]
        # print(len(rst))
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

            cmd = 'ffmpeg -ss {} -i "{}" -t {} -vcodec copy -acodec copy "./newVideos/{}"'.format(secondsToString(timeFromBegin),
                                                                                         f, validDura, f)
            print(cmd)
            rst = runCommand(cmd)
            rst = [r.decode("UTF8").strip() for r in rst]
            os.remove(f)
            # print("\n".join(rst))
    print('共处理{}个文件'.format(len(files)))

if __name__ == "__main__":
    result = processVideoStripCmd()
