import requests
from pyquery import PyQuery as pq

r = requests.get('http://www.toutiao.com/a6296462662335201793/')
d = pq(r.content)
d('video')  # video元素不存在
d('#video')  # id是video的元素是存在的

import base64
main_url = "aHR0cDovL3Y3LnBzdGF0cC5jb20vZmJiZmE2Yjc4ZjM4MThhM2M0OTVhMmRkYjAyOWY5NTAvNTc5\nMWMzODAvdmlkZW8vYy8zNDMwNzcxZjMyNmY0ZDUxOTRiNTYyMzdhNmEyMzFmYy8=\n"
print(base64.standard_b64decode(main_url))
# output: http://v7.pstatp.com/fbbfa6b78f3818a3c495a2ddb029f950/5791c380/video/c/3430771f326f4d5194b56237a6a231fc/