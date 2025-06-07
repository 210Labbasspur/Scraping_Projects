import json
import csv
import scrapy
from datetime import datetime
from scrapy.selector import Selector
import urllib.parse


class Coop(scrapy.Spider):
    name = 'coop'
    prefix = 'https://www.coop.ch'
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
        'FEED_URI': f'output/Coop - {datetime.now().strftime("%d-%m-%Y")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
        'DOWNLOADER_MIDDLEWARES': {'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400}
    }

    api_Key = 'Enter_your_Key_Here'
    proxy = f'http://scraperapi.render=true:{api_Key}@proxy-server.scraperapi.com:8001'

    def start_requests(self):
        urls = []
        with open("input/coop_urls.csv", 'r', newline='', encoding='utf-8', errors='ignore') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                url = row['url']
                if url:
                    urls.append(url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, # headers=self.headers,
                                 meta={'proxy': self.proxy,'render':True,'premium':True} )

    def parse(self, response):
        if True:
            count = 1
            for category in response.css('a.pageHeader__content-navigation-l1-item-link'):
                if category.css("::attr(href)").get('').strip():
                    cat = category.css("::text").get('').strip()
                    cat_url = self.prefix + category.css("::attr(href)").get('').strip()
                    print(count, cat, cat_url)
                    count += 1
                    if 'c/m_' in cat_url:
                        yield scrapy.Request(url=cat_url, callback=self.listing_parse, headers=self.headers,
                                             meta={'proxy': self.proxy,'render_js':True,'premium':True, 'cat': cat})

    def listing_parse(self, response):
        print('Welcome to Listing Page')
        if response.css('a.pagination__next'):
            url = response.css('a.pagination__next ::attr(data-backend-url)').get('').strip().replace('page=2', 'page=1')
            displayUrl = response.css('a.pagination__next ::attr(href)').get('').strip().replace('page=2', 'page=1')
            url = urllib.parse.quote(url, safe='')
            displayUrl = urllib.parse.quote(displayUrl, safe='')
            detail_url = f"https://www.coop.ch/de/dynamic-pageload/productListJson?componentName=productListJson&url={url}&displayUrl={displayUrl}&compiledTemplates%5B%5D=productTile&compiledTemplates%5B%5D=sellingBanner"
            cat = response.meta['cat']
            yield scrapy.Request(url=detail_url, callback=self.detail_parse, headers=self.headers,
                                 meta={'proxy': self.proxy,'render_js':True,'premium':True, 'cat': cat} )

    def detail_parse(self, response):
        print('Welcome to Detail Page')
        data = json.loads(response.text)
        cat = response.meta['cat']
        if data:
            for element in data['contentJsons']['anchors'][0]['json']['elements']:
                item = dict()
                item['Title'] = element.get('title')
                item['price'] = element.get('price') if element.get('price') else None
                item['saving'] = element.get('saving') if element.get('saving') else None
                item['discountData'] = element.get('savingText') if element.get('savingText') else None
                item['productLink'] = self.prefix + element.get('href') if element.get('href') else ''
                item['quantityPrice'] = element.get('priceContext') if element.get('priceContext') else None
                if element.get('image'):
                    item['imageUrl'] = 'https:' + element.get('image').get('src').replace('15_15','710_710')
                item['category'] = cat
                yield item

            page_html =  data['html']
            if page_html:
                sel = Selector(text=page_html, type="html")
                if sel.css('a.pagination__next'):
                    url = sel.css('a.pagination__next ::attr(data-backend-url)').get('').strip()
                    displayUrl = sel.css('a.pagination__next ::attr(href)').get('').strip()
                    url = urllib.parse.quote(url, safe='')
                    displayUrl = urllib.parse.quote(displayUrl, safe='')
                    detail_url = f"https://www.coop.ch/de/dynamic-pageload/productListJson?componentName=productListJson&url={url}&displayUrl={displayUrl}&compiledTemplates%5B%5D=productTile&compiledTemplates%5B%5D=sellingBanner"
                    yield scrapy.Request(url=detail_url, callback=self.detail_parse, headers=self.headers,
                                         meta={'proxy': self.proxy,'premium':True, 'cat': cat})
