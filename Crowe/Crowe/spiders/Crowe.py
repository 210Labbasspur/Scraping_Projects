####################        Crowe

import csv
import scrapy
import datetime

class Crowe(scrapy.Spider):
    name = 'Crowe'
    url = 'https://www.crowe.com/api/sitecore/ListWithFilter/GetTable?sc_mode=normal&id=%7BE7625BFA-976F-441D-A69C-1AB8293A874E%7D&languageName=en-GB&page={}&isDateDesc=true&enforceNormal=True'
    # dutch_url = 'https://www.crowe.com/api/sitecore/ListWithFilter/GetTable?sc_mode=normal&id=%7BE7625BFA-976F-441D-A69C-1AB8293A874E%7D&languageName=nl-NL&page={}&isDateDesc=true&enforceNormal=True'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    custom_settings = {
        'FEED_URI': f'output/Crowe - 1.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',

    }

    # api_Key = '66488b6993c2f255fd148ea56cbb00e4'
    # proxy = f'http://scraperapi.render=true:{api_Key}@proxy-server.scraperapi.com:8001'

    def start_requests(self):
        # url1 = 'https://www.crowe.com/be/spark/insights/brexit-is-your-company-ready'
        # url2 = 'https://www.crowe.com/be/spark/insights/buitenlandse-werknemers-bedrijfsleiders-onderzoekers'
        # url3 = 'https://www.crowe.com/be/spark/insights/brexit-is-your-company-ready'
        # url4 = 'https://www.crowe.com/be/spark/insights/oecd-proposals-on-the-taxation-of-digital-businesses'
        # url5 = 'https://www.crowe.com/be/spark/insights/overview-of-support-measures-in-belgium-20200407'
        # urls = [url1, url2, url3, url4, url5]
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.detail_parse, headers=self.headers,
        #                           meta={'proxy': self.proxy, 'render': True, 'premium': True}
        #                           # meta={'blog_title':blog_title}
        #                           )
        page_no = 0
        yield scrapy.Request(url= self.url.format(page_no), callback=self.parse,  headers=self.headers,
                             # meta={'page_no':page_no, 'proxy': self.proxy,'render':True,'premium':True})
                             meta={'page_no':page_no})


    def parse(self, response):
        loop = response.xpath("//*[contains(@class,'news-list-table__table__item__link')]")
        for index, blog in enumerate(loop):
            blog_url = blog.css('a ::attr(href)').get('').strip()
            blog_title = blog.css('a ::text').get('').strip()
            print(index+1, blog_title, blog_url)
            yield response.follow(url=blog_url, callback=self.detail_parse, headers=self.headers,
                                 # meta={'proxy': self.proxy, 'blog_title':blog_title,'render':True,'premium':True}
                                 meta={'blog_title':blog_title}
                                 )

        page_no = response.meta['page_no']
        if page_no < 18:
            page_no += 1
            yield scrapy.Request(url= self.url.format(page_no), callback=self.parse,  headers=self.headers,
                                 # meta={'page_no': page_no, 'proxy': self.proxy,'render':True,'premium':True})
                                meta={'page_no':page_no})


    def detail_parse(self, response):
        item = dict()
        # blog_title = response.meta['blog_title']
        # item['Title'] = blog_title
        item['Title'] = ''.join(e.strip() for e in response.css('.article-header__title ::text').getall())
        item['Date'] = response.css('.article-header__date ::text').get('').strip()
        item['Content'] = response.xpath("//*[contains(@class,'article-header__content rich-text')]").get('').strip()
        item['Img_url'] = response.css('img.lazyloaded ::attr(src)').get('').strip()

        item['Detail_URL'] = response.url
        yield item


        with open('Output/Crowe - with code.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Date', 'Content', 'Img_url', 'Detail_URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(item)
            print('Data Saved using Code')

