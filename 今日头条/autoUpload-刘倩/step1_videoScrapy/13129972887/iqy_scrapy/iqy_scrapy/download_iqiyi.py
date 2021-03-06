import requests, re, execjs, json, re
from pyquery import PyQuery as pq

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
}
baseUrl = "https://cache.video.iqiyi.com/jp/dash?"
params = {
    "tvid": "",
    "bid": "500",
    "authKey": "",
    "vid": "",
    "src": "01010031010000000000",
    "vt": "0",
    "rs": "1",
    "uid": "",
    "ori": "pcw",
    "ps": "0",
    "tm": "",
    "qd_v": "1",
    "k_uid": "",
    "pt": "0",
    "d": "0",
    "s": "",
    "lid": "",
    "cf": "",
    "ct": "",
    "authKey": "",
    "k_tag": "1",
    "ost": "0",
    "ppt": "0",
    "dfp": "a0a57400d6988441389ca045bfb5b431dcfb3cb78ce419977045fe56959720662b",
    "locale": "zh_cn",
    "prio": "",
    "pck": "",
    "k_err_retries": "0",
    "k_ft1": "",
    "k_ft4": "",
    "bop": ""
}


# 获取js加密程序1,2代表提到的两种加密方式r()和cmd5x()
def getJs(i):
    if (i == 1):
        with open("E:/py/entryptR.js", 'r', encoding='utf-8') as f:
            html = ""
            line = f.readline()
            while (line):
                html += line
                line = f.readline()
            return html
    if (i == 2):
        with open("E:/py/encryptCmd5x.js", 'r', encoding='utf-8') as f:
            html = ""
            line = f.readline()
            while (line):
                html += line
                line = f.readline()
            return html


# 获取参数
def getParams(url):
    r = requests.get(url, headers=headers)
    html = r.text
    title = re.findall(r"<meta property=\"og:title\"[^>]*?content=\"(.*?)\"/>", html)[0]
    initParams = re.findall(r"param\[\'(.*?)\'] = \"(.*?)\"", html)
    params["albumid"] = initParams[0][1]
    params["tvid"] = initParams[1][1]
    params["vid"] = initParams[2][1]
    params["k_uid"] = "9653bb59c557abf0d0298813a66521ef"
    ctx = execjs.compile(getJs(1))
    params["tm"] = ctx.call("getTime")  # 利用js获取当前时间戳
    params['prio'] = json.dumps({'ff': "f4v", 'code': 2})
    params['bop'] = json.dumps(
        {'version': "7.0", 'dfp': "a0a57400d6988441389ca045bfb5b431dcfb3cb78ce419977045fe56959720662b"})
    params["authKey"] = ctx.call("getKey", params["tm"], params['tvid'])
    params["k_ft1"], params["k_ft4"] = ctx.call("getK_ft", params["prio"])
    p = baseUrl + ctx.call("getUrl", params)
    params["callback"] = 'Q' + ctx.call("R", p)
    params["ut"] = "0"
    s = p.replace("https://cache.video.iqiyi.com", "") + "&ut=0"
    ctx = execjs.compile(getJs(2))
    params["vf"] = ctx.call("cmd5x", s)
    return title, p + "&ut=0" + "&vf=" + params["vf"]


# 下载f4v
def downloadF4v(title, url):
    try:
        pattern = re.compile("\"([^\"]*?\.f4v.*?)\"")
        r = requests.get(url1, headers=headers)
        f4v_urls = pattern.findall(r.text)
        url2s = []
        for f4v_url in f4v_urls:
            url2s.append("http://data.video.iqiyi.com/videos" + f4v_url.replace("\\", ""))
    except:
        print("访问返回为空")
        return 0
    if (len(url2s) == 0):
        print("不存在f4v链接")
        return 0
    count = 1
    with open("E:/" + title + ".f4v", 'wb') as f:
        for url2 in url2s:
            try:
                r = requests.get(url2, headers=headers)
                url3 = r.json()['l']
                f.write(requests.get(url3, headers=headers).content)
                print("已下载:", round(count / len(url2s) * 100, 2), "%")
            except:
                print("part" + str(count) + " 下载失败!")
            count += 1
    return 1


# 下载m3u8
def downloadM3U8(title, url1):
    try:
        pattern = re.compile(r"\"m3u8\":\"(.*?)\"")
        urls = re.findall(r"(http.*?)\\n", pattern.findall(requests.get(url1, headers=headers).text)[0])
        url2s = []
        for url in urls:
            url2s.append(url.replace("\\", ''))
        count = 1
    except:
        print("访问返回为空")
        return 0
    if (len(url2s) == 0):
        print("不存在M3U8链接")
        return 0
    with open("E:/" + title + ".mp4", 'wb') as f:
        for url2 in url2s:
            try:
                r = requests.get(url2, headers=headers)
                f.write(r.content)
                print("已下载:", round(count / len(url2s) * 100, 2), "%")
            except:
                print("part" + str(count) + " 下载失败!")
            count += 1
    return 1


if __name__ == "__main__":
    # url = "https://www.iqiyi.com/v_19rr9ofttc.html"
    ret = 0
    url = "https://www.iqiyi.com/v_19rrnbwak8.html"
    title, url1 = getParams(url)
    print("开始下载 ", title)
    ret = downloadF4v(title, url1)
    if (ret == 0):
        ret = downloadM3U8(title, url1)
    if (ret == 0):
        print(title, " 下载失败!")
    else:
        print(title, " 下载成功!")
