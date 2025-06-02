import scrapy
from datetime import date
from datetime import datetime

class AllStarHealth(scrapy.Spider):
    name = 'AllStarHealth'
    url = "https://www.allstarhealth.com/cl.aspx"
    custom_settings = {
        'FEED_URI': 'AllStarHealth.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }
    headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'Accept-Language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
      'Cache-Control': 'max-age=0',
      'Connection': 'keep-alive',
      'Cookie': 'SessionID=856e5eb344a14294a156bcd7312f5740; URLBeforeRedirect=/home.aspx; CartID=39a5638a8b154b3a9de39dd96bbfe8c8; TESTCOOKIESUPPORT=1; ASP.NET_SessionId=rgo23vh5tdx4fekt1jctvrdo; CartID=39a5638a8b154b3a9de39dd96bbfe8c8',
      'Referer': 'https://www.allstarhealth.com/',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-User': '?1',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"'
    }

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers)

    def parse(self, response):
        for category in response.css('.subtitle+ table a'):
            category_url = category.css('::attr(href)').get('')
            if category_url:
                yield response.follow(url=category_url, callback=self.listing_page, headers=self.headers)

    def listing_page(self, response):
        for list_item in response.css('.product_box'):
            product_url = list_item.css('.pro_txt a::attr(href)').get('')
            if product_url:
                item= dict()
                today = date.today()
                item['Date'] = today
                item['Time'] = datetime.now().time()
                store_name = response.css('#search_query ::attr(placeholder)').get('').strip()
                item['Store Name'] = store_name.replace('Search ','')
                item['Product Brand'] = list_item.css('.pro_txt h3::text').get('').strip()
                yield response.follow(url=product_url, callback=self.detail_page, headers=self.headers, meta={'item': item})

        next_page = response.css('li+ .previous a ::attr(href)').get('')
        if next_page:
            yield response.follow(url=next_page, headers=self.headers, callback=self.listing_page)

    def detail_page(self, response):
        item = response.meta['item']
        item['Product Name'] = response.css('.titl_txt::text').get('').strip()
        item['Product UPC'] = response.xpath("//*[contains(@itemprop, 'gtin12')]/@content").get('').strip()
        item['Product Price($)'] = response.xpath("//*[contains(@itemprop, 'price')]/@content").get('').strip()
        item['Product Image URL'] = response.css('#ctl00_ContentPlaceHolder1_imgFamilyPicFileName ::attr(src)').get('').strip()
        item['Product URL'] = response.xpath("//*[contains(@rel, 'canonical')]/@href").get('').strip()

        other_sizes = response.css('.othr_siz_sec').get('')
        if other_sizes:
            for sizes in response.css('.scrol_block li'):
                other_size_link = sizes.css('.enlarge::attr(href)').get('')
                yield response.follow(url=other_size_link, callback=self.other_sizes_detail_page,
                                      headers=self.headers, meta={'item': item})
        yield item

    def other_sizes_detail_page(self, response):
        item = response.meta['item']
        item['Product Name'] = response.css('.titl_txt::text').get('').strip()
        item['Product UPC'] = response.xpath("//*[contains(@itemprop, 'gtin12')]/@content").get('').strip()
        item['Product Price($)'] = response.xpath("//*[contains(@itemprop, 'price')]/@content").get('').strip()
        item['Product URL'] = response.xpath("//*[contains(@rel, 'canonical')]/@href").get('').strip()
        yield item