from wxpy import *

bot = Bot(cache_path=True)

for index in range(len(bot.friends().search('一一'))):
    print(bot.friends().search('一一')[index])
    people = bot.friends().search('一一')[index]
    print(people.name)
    if people.name=='一一':
        print('yes');
        friend=people
    else:
    	print('no');
print(friend)
friend.send("hello")

@bot.register(friend)
def recv_send_msg(recv_msg):
    print('收到的消息：', recv_msg)
    return '自动回复：{}'.format(recv_msg)

# 进入Python命令行，让程序保持运行
embed()
