from wxpy import *
import re
import jieba
import pandas as pd
import numpy

bot=Bot(cache_path=True)
friends=bot.friends()


# 统计签名
with open('signatures.txt','w',encoding='utf-8') as f:
    for friend in friends:
        # 对数据进行清洗，将标点符号等对词频统计造成影响的因素剔除
        pattern=re.compile(r'[一-龥]+')
        filterdata=re.findall(pattern,friend.signature)
        f.write(''.join(filterdata))



#过滤停止词
with open('signatures.txt','r',encoding='utf-8') as f:
    data=f.read()
    segment=jieba.lcut(data)

    words_df=pd.DataFrame({'segment':segment})
    stopwords = pd.read_csv("stopwords.txt", index_col=False, quoting=3, sep=" ", names=['stopword'], encoding='utf-8')
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]


#使用numpy进行词频统计
words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数":numpy.size})
words_stat = words_stat.reset_index().sort_values(by=["计数"],ascending=False)
# print(words_stat)

#词频可视化：词云，基于wordcloud库，当然pyecharts也可以实现
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt

# 设置词云属性
# color_mask = imread('background.jfif')
# color_mask = imread('bg.jpg')
color_mask = imread('bg1.jpeg')

wordcloud = WordCloud(
                # font_path="simhei.ttf",   # mac上没有该字体
                font_path="/System/Library/Assets/com_apple_MobileAsset_Font3/6d903871680879cf5606a3d2bcbef058e56b20d4.asset/AssetData/华文仿宋.ttf",   # 设置字体可以显示中文
                background_color="white",       # 背景颜色
                max_words=100,                  # 词云显示的最大词数
                mask=color_mask,                # 设置背景图片
                max_font_size=100,              # 字体最大值
                random_state=42,
                width=1000, height=860, margin=2,# 设置图片默认的大小,但是如果使用背景图片的话,                                                   # 那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
                )

# 生成词云, 可以用generate输入全部文本,也可以我们计算好词频后使用generate_from_frequencies函数
word_frequence = {x[0]:x[1]for x in words_stat.head(100).values}
print(word_frequence)
word_frequence_dict = {}
for key in word_frequence:
    word_frequence_dict[key] = word_frequence[key]

print(word_frequence_dict)
wordcloud.generate_from_frequencies(word_frequence_dict)
# 从背景图片生成颜色值
image_colors = ImageColorGenerator(color_mask)
# 重新上色
wordcloud.recolor(color_func=image_colors)
# 保存图片
wordcloud.to_file('output.png')
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
