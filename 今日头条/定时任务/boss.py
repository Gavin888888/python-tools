# 2018-07-17
# Author limingxuan
# limx2011@hotmail.com
# blog：https://www.jianshu.com/p/a5907362ba72

import scrapy
import time

class ZhipinSpider(scrapy.Spider):
    name = 'zhipin'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['http://www.zhipin.com/']
    positionUrl = 'https://www.zhipin.com/job_detail/?query=python&scity=101010100'
    curPage = 1
    # 我的浏览器找不到源码中的一些字段，比如
    # x-devtools-emulate-network-conditions-client-id
    # upgrade-insecure-requests
    # dnt
    # cache-control
    # postman-token
    # 所以就没有加，按我的浏览器查到的信息填写的，现在看起来貌似也能跑起来
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'cookie': "JSESSIONID=""; __c=1530137184; sid=sem_pz_bdpc_dasou_title; __g=sem_pz_bdpc_dasou_title; __l=r=https%3A%2F%2Fwww.zhipin.com%2Fgongsi%2F5189f3fadb73e42f1HN40t8~.html&l=%2Fwww.zhipin.com%2Fgongsir%2F5189f3fadb73e42f1HN40t8~.html%3Fka%3Dcompany-jobs&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1531150234,1531231870,1531573701,1531741316; lastCity=101010100; toUrl=https%3A%2F%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3Dpython%26scity%3D101010100; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1531743361; __a=26651524.1530136298.1530136298.1530137184.286.2.285.199",
        'origin': "https://www.zhipin.com",
        'referer': "https://www.zhipin.com/job_detail/?query=python&scity=101010100",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }

    def start_requests(self):
        return [self.next_request()]

    def parse(self, response):
        print("request -> " + response.url)
        job_list = response.css('div.job-list > ul > li')
        for job in job_list:
            item = WwwZhipinComItem()
            job_primary = job.css('div.job-primary')
            item['pid'] = job.css(
                'div.info-primary > h3 > a::attr(data-jobid)').extract_first().strip()

            # job-title这里和源码不同，页面改版所导致
            item['positionName'] = job_primary.css(
                'div.info-primary > h3 > a > div.job-title::text').extract_first().strip()
            item['salary'] = job_primary.css(
                'div.info-primary > h3 > a > span::text').extract_first().strip()
            # 提取全部内容: .extract()，获得是一个列表
            # 提取第一个:.extract_first()，获得是一个字符串
            info_primary = job_primary.css(
                'div.info-primary > p::text').extract()
            item['city'] = info_primary[0].strip()
            item['experience'] = info_primary[1].strip()
            item['educational'] = info_primary[2].strip()
            item['company'] = job_primary.css(
                'div.info-company > div.company-text > h3 > a::text').extract_first().strip()
            company_infos = job_primary.css(
                'div.info-company > div.company-text > p::text').extract()
            if len(company_infos) == 3:
                item['industryField'] = company_infos[0].strip()
                item['financeStage'] = company_infos[1].strip()
                item['companySize'] = company_infos[2].strip()

            # 页面改版，已没有标签，所以这一段代码
            item['positionLables'] = job.css(
                'li > div.job-tags > span::text').extract()

            # Python strip() 方法用于移除字符串头尾指定的字符（默认为空格）或字符序列。
            # 注意：该方法只能删除开头或是结尾的字符，不能删除中间部分的字符。
            # 此处页面已改版，和源代码不同
            item['time'] = job_primary.css(
                'div.info-publis > p::text').extract_first().strip()

            item['updated_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            yield item

        self.curPage += 1
        time.sleep(5)  # 爬的慢一点，免得被封ip
        yield self.next_request()

    def next_request(self):
        return scrapy.http.FormRequest(
            self.positionUrl + ("&page=%d&ka=page-%d" %
                                (self.curPage, self.curPage)),
            headers=self.headers,
            callback=self.parse)