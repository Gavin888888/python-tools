import moviepy.editor as mp
from moviepy.editor import *
from moviepy.editor import TextClip
from moviepy.audio.fx import all


# vid1=VideoFileClip("1.mp4")
# s=vid1.reader.size  #返回视频的尺寸
# #[960, 540]
# print(s)
# s=vid1.reader.fps  #返回的帧率
# v=vid1.resize(0.5)  #尺寸等比缩放0.5
# #注意：只有写入文件后才有效果
# v.write_videofile("my.mp4")

FONT_URL = './FZCuJinLJW.TTF'
video_path="1.mp4"
video_name="《一生爱你千百回》"
singer='演唱：梅艳芳'
video = mp.VideoFileClip(video_path,audio=True)
print(video.size)

logo = (mp.ImageClip("headerimage.jpg")
        .set_duration(video.duration)  # 水印持续时间
        .resize(width=576)  # 水印的高度，会等比缩放
        .margin(left=0,right=0, top=0, opacity=1)  # 水印边距和透明度
        .set_pos(("left","top")))  # 水印的位置
logo1 = (mp.ImageClip("footerimage.jpeg")
         .set_duration(video.duration)  # 水印持续时间
         .resize(width=576)  # 水印的高度，会等比缩放
         .margin(left=0,right=0, bottom=0, opacity=1)  # 水印边距和透明度
         .set_pos(("left","bottom")))  # 水印的位置
txt = (mp.TextClip(video_name,color='#FFFFFF', font=FONT_URL, fontsize=40)
.set_duration(video.duration)
       .set_position([200,210]))
subtxt = (mp.TextClip(singer,color='#FFFFFF', font=FONT_URL, fontsize=25)
       .set_duration(video.duration)
       .set_position([210,260]))

video1 = mp.VideoFileClip(video_path,audio=True)
audioclip=video1.audio
audioclip.write_audiofile('test.mp3')
print(audioclip)

final = mp.CompositeVideoClip([video, logo,logo1,txt,subtxt])
final=final.set_audio(audioclip)

# mp4文件默认用libx264编码， 比特率单位bps
final.write_videofile("test.mp4",audio_codec="aac")

