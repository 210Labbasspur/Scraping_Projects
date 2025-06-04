import scrapy
import csv
from urllib.parse import urljoin
from collections import defaultdict

class apa(scrapy.Spider):
    name = "apa"
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'no-cache',
        'json-naming-strategy': 'camel',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }
    custom_settings = {
        # # 'FEED_URI': f'output/APA - uniquelist.csv',
        'FEED_URI': f'output/APA - Record.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
        'DOWNLOADER_MIDDLEWARES': {'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400}
    }

    # api_Key = '66488b6993c2f255fd148ea56cbb00e4'
    api_Key = 'ENTER_YOUR_SCRAPPERAPI_KEY_HERE'
    proxy = f'http://scraperapi.render=true:{api_Key}@proxy-server.scraperapi.com:8001'

    dict_list = []
    count = 0
    def start_requests(self):
        # url = 'https://www.a-p-a.net/members/'
        # yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

        all_members = []
        with open("output/APA - uniquelist.csv", 'r', newline='', encoding='utf-8', errors='ignore') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                member = dict()
                member['cst_url'] = row['cst_url']
                member['cst_name'] = row['cst_name']
                if member:
                    all_members.append(member)

        combined_dict = defaultdict(list)
        for item in all_members:
            combined_dict[item['cst_url']].append(item['cst_name'])
        unique_list = [{'cst_url': url, 'cst_name': ', '.join(names)} for url, names in combined_dict.items()]

        for index, member in enumerate(unique_list, start= 1):
            detail_page_URL = member.get('cst_url')
            cst_name = member.get('cst_name')
            print(member)
            yield scrapy.Request(url=detail_page_URL, callback=self.parse_details_page,
                                 meta={'proxy': self.proxy,'render':True,'premium':True, 'cst_name':cst_name} )
                                # )

    # def parse(self, response):
    #     count = 1
    #     for cst in response.xpath("//*[contains(@value,'https://www.a-p-a.net/?speciality=')]"):
    #         cst_url = cst.css('::attr(value)').get('').strip().replace('/#content','')
    #         cst_name = cst.css('::text').get('').strip()
    #         print(count, cst_name, cst_url)
    #         count +=1
    #         yield scrapy.Request(url=cst_url, callback=self.listing_parse, headers=self.headers, meta={'cst_name':cst_name})
    #
    #
    # def listing_parse(self, response):
    #     cst_name = response.meta['cst_name']
    #     for members in response.css('article.c-tile--member'):
    #         detail_page_URL = members.css('a.c-tile__link::attr(href)').get('')
    #         self.count += 1
    #         # print(self.count, cst_name, detail_page_URL)
    #         item = dict()
    #         item['Ser'] = self.count
    #         item['cst_name'] = cst_name
    #         item['cst_url'] = detail_page_URL
    #         self.dict_list.append(item)
    #         yield item
    #         # yield scrapy.Request(url=detail_page_URL, callback=self.parse_details_page,
    #         #                      # meta={'proxy': self.proxy,'render':True,'premium':True, 'cst_name':cst_name} )
    #         #                     )
    #
    #     next_page = response.css('a.next::attr(href)').get('').strip()
    #     if next_page:
    #         yield response.follow(url=next_page, callback=self.listing_parse, headers=self.headers, meta={'cst_name':cst_name})

    def parse_details_page(self, response):
        item = dict()
        item['Company_Name'] = response.css('h1.u-margin-top-large::text').get('').strip()
        emails = response.xpath('//*[contains(@href,"mailto")]/text()').getall()
        item['E-mail'] = ', '.join(e.strip() for e in emails)
        item['Website'] = response.xpath('//*[contains(@href,"http")]/text()').get('').strip()
        address = response.xpath("//*[contains(@class,'c-tile--hero__title u-h4')]/text()").getall()
        address = ', '.join(e.strip().replace('\n','').replace('\t','') for e in address)
        item['Address'] = address.replace(',,',',')
        item['Contact'] = response.xpath('//*[contains(@href,"tel:")]/text()').get('').strip()
        item['Company_Service_Type'] = response.meta['cst_name']
        item['Detail URL'] = response.url
        yield item

