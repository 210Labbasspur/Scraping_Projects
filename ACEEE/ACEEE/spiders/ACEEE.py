##############          ACEEE

import re
import json
import scrapy
from datetime import datetime
from scrapy.selector import Selector

class ACEEE(scrapy.Spider):
    name = "ACEEE"
    url = 'https://www.aceee.org/views/ajax?_wrapper_format=drupal_ajax&view_name=resources&view_display_id=page_1&view_args=&view_path=%2Fpublications&view_base_path=publications&view_dom_id=fc7590ae743ea2a5148c08c1c0c43f1b65a15963538ffe0e377f86e14ad0b76d&pager_element=0&page={}&_drupal_ajax=1&ajax_page_state%5Btheme%5D=aceee_foundation&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=eJxtkGtuwzAMgy8kxEcypJhJvSqW4MfW9PRLWxQt1v2RyE8gCIhnAHGxURL3bCWsasJK_Jc7945alOXz1jTPZ-KUunHZw1NMS7XSSXBLRlzcGlJcsh62hRUF9WiSvEbPjvAUJMrX_bA28RdfCCPOZueMY22umcuM8B-MwhV0D98GOVdeK_uphVSHs04vMo3iQzS3ExK1vXVsQbiBvjN-WrjPR_072CwNBV1Hlc-f_QIwLIHQ'
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=1, i',
        'referer': 'https://www.aceee.org/publications',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'SSESS14e287370fdbb469a2d85ebb407667fb=rLZqqW%2CT%2Cc5yqw3Nn2tddau7pP5XEouxb8H85sK9Or0fd2VB; cookie-agreed=0; _gcl_au=1.1.157105631.1741115973; _ga=GA1.1.360747828.1741115973; _ga_WD12JJP0RV=GS1.1.1741126751.7.1.1741126785.26.0.1884299367',
    }

    custom_settings = {
        'FEED_URI': f'output/ACEEE - {datetime.now().strftime("%d-%m-%Y")}.xlsx',
        'FEED_FORMAT': 'xlsx',
        'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    count = 0
    def start_requests(self):
        page_no = 0
        yield scrapy.Request(self.url.format(page_no), callback=self.parse, headers=self.headers, meta={'page_no':page_no})

        yield scrapy.Request('https://www.aceee.org/summer-study-2023-proceedings', callback=self.pdf_parse, headers=self.headers, meta={'year':'2023'})
        yield scrapy.Request('https://www.aceee.org/summer-study-2024-proceedings', callback=self.pdf_parse, headers=self.headers, meta={'year':'2024'})


    def pdf_parse(self, response):
        count = 1
        for record in response.css('#proceeding'):
            item = dict()
            item['Resource Name'] = record.css('::text').get('').strip()
            item['Resource Type'] = 'Summer Study'
            item['Authoring Organization'] = 'ACEEE'
            item['Authoring Organization Type'] = 'Association'
            item['Authors'] = record.css('div ::text').get('').strip()
            item['Description / Abstract'] = record.css('::attr(href)').get('').strip()
            item['Year Published'] = response.meta['year']
            item['Applicable Region'] = 'Global'
            item['URL'] = record.css('::attr(href)').get('').strip()
            yield item

            print(count,' # Summer Study for year |',response.meta['year'],'| is : ', item)
            count += 1


    def parse(self, response):
        page_no = response.meta['page_no']
        data = json.loads(response.text)
        if data:
            for row in data:
                if row.get('method') == 'replaceWith':
                    selector = Selector(text=row.get('data',''))
                    for record in selector.xpath("//*[contains(@class,'list-media media')]"):
                        record_url = record.css("::attr(href)").get('').strip()
                        self.count += 1
                        print(self.count, " # Record URL is : ", record_url)
                        yield response.follow(record_url, callback=self.detail_parse, headers=self.headers)

                    if selector.xpath("//*[contains(@class,'list-media media')]"):
                        page_no += 1
                        print('Next Page is : ', page_no)
                        yield scrapy.Request(self.url.format(page_no), callback=self.parse, headers=self.headers, meta={'page_no':page_no})



    def detail_parse(self, response):
        item = dict()

        item['Resource Name'] = response.css('.hero-text h1 ::text').get('').strip()
        item['Resource Type'] = response.css('.hero-text .tag ::text').get('').strip()

        item['Authoring Organization'] = 'ACEEE'
        item['Authoring Organization Type'] = 'Association'

        item['Authors'] = ', '.join(e.strip() for e in response.css('.staff .list-title ::text').getall())

        pre_description = ' '.join(e.strip() for e in response.xpath("//*[contains(@class,'small-6 small-offset-2 medium-5 medium-offset-1 cell')]//text()").getall())
        # post_description = ' '.join(e.strip() for e in response.css('.entry p ::text,.entry ol ::text, .entry h3 ::text').getall()).replace('Authors:','')
        item['Description / Abstract'] = f'{pre_description}'

        item['Year'] =  response.css(".hero-text .summary ::text").get('').strip()
        item['Year Published'] =  response.css(".hero-text .summary ::text").get('').strip().split(', ')[-1]

        item['Applicable Region'] = 'Global'
        item['URL'] = response.url
        yield item
