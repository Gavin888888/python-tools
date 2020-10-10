import os
import shutil

filepath = "/Users/leili/Desktop/changeFileName/videos"
if __name__ == "__main__":

    if not os.path.exists(filepath):
        print("目录不存在!!")
        os._exit(1)
    filenames = os.listdir(filepath)
    for i in range(len(filenames)):
        filename =filenames[i]
        print(filename)
        print(i)
        # os.rename(filepath + '\\' + data,filepath + '\\' + newname)
        local_file_path = filepath+"/"+filename
        dst_file_path = "/Users/leili/Desktop/changeFileName/newvideos/" + str(i)+".mp4"
        shutil.copy(local_file_path, dst_file_path)  # copy file

