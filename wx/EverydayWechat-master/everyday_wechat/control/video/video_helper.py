# encoding:utf-8
import requests
from bs4 import BeautifulSoup
import re
import json
import os

__all__ = [
    'resolutionVideo'
]
import re
import time
from datetime import datetime
import random
import itchat
from everyday_wechat.utils.common import (
    FILEHELPER,
)
def resolutionVideo(msg):  # 视频地址
    """ 视频解析 """
    # msg['Text']: 分享的标题
    # msg['Url']: 分享的链接
    share_video_name = msg['Text']
    share_video_url = msg['Url']
    print('分享的标题：={}\n'.format(share_video_name))
    print('分享的链接：={}\n'.format(share_video_url))
    # print('分享的Content：={}\n'.format(msg['Content']))
    # print('分享的Content：={}\n'.format(msg['Image']))
    try:
        # 获取发送者的用户id
        uuid = FILEHELPER if msg['ToUserName'] == FILEHELPER else msg.fromUserName
        retext = "http://vip.yunzhiku.club/?v={}".format(share_video_url)
        itchat.send(retext, uuid)
    except Exception as exception:
        print(str(exception))
# http: // vip.yunzhiku.club /?v = https: // www.iqiyi.com / v_19rr7pmpos.html  # vfrm=19-9-0-1
    #     conf = config.get('auto_reply_info')
    #     if not conf.get('is_auto_reply'):
    #         return
    #     # 获取发送者的用户id
    #     uuid = FILEHELPER if msg['ToUserName'] == FILEHELPER else msg.fromUserName
    #     is_all = conf.get('is_auto_reply_all')
    #     auto_uuids = conf.get('auto_reply_black_uuids') if is_all else conf.get('auto_reply_white_uuids')
    #     # 开启回复所有人，当用户是黑名单，不回复消息
    #     if is_all and uuid in auto_uuids:
    #         return
    #
    #     # 关闭回复所有人，当用户不是白名单，不回复消息
    #     if not is_all and uuid not in auto_uuids:
    #         return
    #
    #     receive_text = msg.text  # 好友发送来的消息内容
    #     # 好友叫啥，用于打印
    #     nick_name = FILEHELPER if uuid == FILEHELPER else msg.user.nickName
    #     print('\n{}发来信息：{}'.format(nick_name, receive_text))
    #
    #     uuid = msg.fromUserName  # 群 uid
    #     ated_uuid = uuid  # 艾特你的用户的uuid
    #     ated_name = nick_name  # 艾特你的人的群里的名称
    #
    #     # 如果是帮助
    #     helps = re.findall(help_complie, receive_text, re.I)
    #     if helps:
    #         retext = help_group_content
    #         itchat.send(retext, uuid)
    #         return

