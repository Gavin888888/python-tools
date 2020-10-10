# -*- coding: utf-8 -*-
"""
Project: EverydayWechat-Github
Creator: DoubleThunder
Create time: 2019-07-12 23:07
Introduction: 处理好友消息内容
"""
baiduwenku_complie = r'^(?:0|wenku.baidu|wk.baidu)\s*$'
at_compile = r'(@.*?\s{1,}).*?'
tomorrow_compile = r'明[日天]'

punct_complie = r'[^a-zA-z0-9\u4e00-\u9fa5]+$'  # 去除句子最后面的标点
help_complie = r'^(?:0|帮忙|帮助|help)\s*$'

weather_compile = r'^(?:\s*(?:1|天气|weather)(?!\d).*?|.*?(?:天气|weather)\s*)$'
weather_clean_compile = r'1|天气|weather|\s'
calendar_complie = r'^\s*(?:2|日历|万年历|calendar)(?=19|2[01]\d{2}|\s|$)'
calendar_date_compile = r'^\s*(19|2[01]\d{2})[\-\/—\s年]*(0?[1-9]|1[012])[\-\/—\s月]*(0?[1-9]|[12][0-9]|3[01])[\s日号]*$'
rubbish_complie = r'^\s*(?:3|垃圾|rubbish)(?!\d)'

common_msg = '@{ated_name}\u2005\n{text}'
weather_error_msg = '@{ated_name}\u2005\n未找到『{city}』城市的天气信息'
weather_null_msg = '@{ated_name}\u2005\n 请输入城市名'

calendar_error_msg = '@{ated_name}\u2005日期格式不对'
calendar_no_result_msg = '@{ated_name}\u2005未找到{_date}的数据'

rubbish_normal_msg = '@{ated_name}\u2005\n【查询结果】：『{name}』属于{_type}'
rubbish_other_msg = '@{ated_name}\u2005\n【查询结果】：『{name}』无记录\n【推荐查询】：{other}'
rubbish_nothing_msg = '@{ated_name}\u2005\n【查询结果】：『{name}』无记录'
rubbish_null_msg = '@{ated_name}\u2005 请输入垃圾名称'

help_group_content = """小助手功能：
1.输入：天气+城市名 
例如：天气北京
2.输入：日历+日期(格式:yyyy-MM-dd 可空)
例如：日历2019-07-03
3.输入：vip视频解析
例如：（爱奇艺/优酷/腾讯）url
更多功能：请输入 help/帮助。
"""

import re
import time
from datetime import datetime
import random
import itchat
from everyday_wechat.utils import config
from everyday_wechat.utils.data_collection import (
    get_weather_info,
    get_bot_info,
    # get_calendar_info,
)
from everyday_wechat.control.wenku.wenku import (
    parserJS,
)
from everyday_wechat.utils.common import (
    FILEHELPER,
)
from everyday_wechat.utils.db_helper import (
    find_weather,
    udpate_user_city,
    udpate_weather
)
__all__ = ['handle_friend']


def handle_friend(msg):
    """ 处理好友信息 """
    try:
        conf = config.get('auto_reply_info')
        if not conf.get('is_auto_reply'):
            return
        # 获取发送者的用户id
        uuid = FILEHELPER if msg['ToUserName'] == FILEHELPER else msg.fromUserName
        is_all = conf.get('is_auto_reply_all')
        auto_uuids = conf.get('auto_reply_black_uuids') if is_all else conf.get('auto_reply_white_uuids')
        # 开启回复所有人，当用户是黑名单，不回复消息
        if is_all and uuid in auto_uuids:
            return

        # 关闭回复所有人，当用户不是白名单，不回复消息
        if not is_all and uuid not in auto_uuids:
            return

        receive_text = msg.text  # 好友发送来的消息内容
        # 好友叫啥，用于打印
        nick_name = FILEHELPER if uuid == FILEHELPER else msg.user.nickName
        print('\n{}发来信息：{}'.format(nick_name, receive_text))

        uuid = msg.fromUserName  # 群 uid
        ated_uuid = uuid  # 艾特你的用户的uuid
        ated_name = nick_name  # 艾特你的人的群里的名称

        # 如果是帮助
        helps = re.findall(help_complie, receive_text, re.I)
        if helps:
            retext = help_group_content
            itchat.send(retext, uuid)
            return

        # 百度文库解析
        if "wenku.baidu" in receive_text:
            retext = parserJS(receive_text)  # 解析文库文档
            retext = '臣妾做不到'
            itchat.send(retext, toUserName=uuid)
            return
        # 已开启天气查询，并包括天气关键词

        if re.findall(weather_compile, receive_text, re.I):
                city = re.sub(weather_clean_compile, '', receive_text, flags=re.IGNORECASE).strip()
                print('--------------------------{}--------------------------'.format(city))
                _date = datetime.now().strftime('%Y-%m-%d')
                weather_info = find_weather(_date, city)
                if weather_info:
                    retext = common_msg.format(ated_name=ated_name, text=weather_info)
                    itchat.send(retext, uuid)
                    return

                weather_info = get_weather_info(city)
                if weather_info:
                    # print(ated_name, city, retext)
                    retext = common_msg.format(ated_name=ated_name, text=weather_info)
                    itchat.send(retext, uuid)

                    data = {
                        '_date': _date,
                        'city_name': city,
                        'weather_info': weather_info,
                        'userid': ated_uuid,
                        'last_time': datetime.now()
                    }
                    udpate_weather(data)
                    # userid,city_name,last_time,group_name udpate_weather_city
                    data2 = {
                        'userid': ated_uuid,
                        'city_name': city,
                        'last_time': datetime.now()
                    }
                    udpate_user_city(data2)
                    return
                else:
                    retext = weather_error_msg.format(ated_name=ated_name, city=city)
                    itchat.send(retext, uuid)
                    return
                return

        reply_text = get_bot_info(receive_text, uuid)  # 获取自动回复
        if reply_text:  # 如内容不为空，回复消息
            time.sleep(random.randint(1, 2))  # 休眠一秒，保安全。想更快的，可以直接注释。
            reply_text = reply_text if not uuid == FILEHELPER else '机器人回复：' + reply_text
            itchat.send(reply_text, toUserName=uuid)
            print('回复{}：{}'.format(nick_name, reply_text))
        else:
            print('自动回复失败\n')
    except Exception as exception:
        print(str(exception))
