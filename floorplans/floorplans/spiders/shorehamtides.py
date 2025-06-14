import scrapy
import datetime


class shorehamtides(scrapy.Spider):
    name = 'shorehamtides'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    custom_settings = {
        'FEED_URI': f'output/Shoreham & Tides Floorplans - {datetime.datetime.now().strftime("%d-%m-%Y")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',

        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000
        },
        "REQUEST_FINGERPRINTER_CLASS": "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ZYTE_API_KEY": "ENTER_YOUR_ZYTE_API_KEY",  # Please enter your API Key here
        "ZYTE_API_TRANSPARENT_MODE": True,
        "ZYTE_API_EXPERIMENTAL_COOKIES_ENABLED": True,
    }

    def start_requests(self):
        url = 'https://www.shorehamtides.com/floorplans?gadid=660718530417&device=c&network=g&keyword=shoreham%20and%20tides&adgroup=151232635393&campaign=20236336283&gclid=CjwKCAjwnqK1BhBvEiwAi7o0X-hrLQoi95fiGTx4nlfn58YZUKWA3Z7V2NmlpR4ENQFEV_5Gx9gNzhoCd6cQAvD_BwE'
        yield scrapy.Request(url=url, callback=self.parse, headers=self.headers,)

    def parse(self, response):
        for floor in response.xpath("//*[contains(@class,'pb-4 mb-2 col-12  col-sm-6 col-lg-4 fp-container')]"):
            floor_url = floor.xpath(".//*[contains(@class,'btn btn-primary btn-block btn-block track-apply floorplan-action-button')]/@href").get('').strip()
            yield response.follow(url=floor_url, callback=self.detail_parse, headers=self.headers,)

    def detail_parse(self, response):
        unit_size = response.xpath("//*[contains(@data-selenium-id,'SID_h1Tag')]/text()").get('').strip().replace('-','').replace('THE SHOREHAM','')
        bed_bath = response.xpath("//*[contains(@class,'row mb-4 pt-5 justify-content-between align-items-center')]/div[1]/div[1]")
        bed = bed_bath.xpath(".//span[contains(text(),'Bedroom')]/text()").get('').strip().replace('Bedroom','').replace(' ','').replace('s','')
        bath = bed_bath.xpath(".//span[contains(text(),'Bathroom')]/text()").get('').strip().replace('Bathroom','').replace(' ','').replace('s','')
        for appartment in response.css('.unit-container'):
            item = dict()
            item['Building Name'] = 'Shoreham & Tides'
            item['Unit size'] = unit_size.replace('  ','')
            for unit in appartment.css('.td-card-name ::text').getall():
                if '#' in unit:
                    item['Unit #'] = unit.strip().replace('#','')
            item['Beds'] = bed
            item['Bath'] = bath
            item['Sq. Ft.'] = appartment.xpath(".//*[contains(@class,'td-card-sqft')]/text()").get('').strip()
            pricing_url = appartment.css(".td-card-footer a ::attr(href)").get('').strip()
            if pricing_url:
                yield response.follow(url=pricing_url, callback=self.pricing_parse, headers=self.headers,
                                      meta={'item':item})

    def pricing_parse(self, response):
        item = response.meta['item']
        item['Available Date'] = response.xpath("//*[contains(@class,'required isdate maskdate moveindatevalidation excludeDays')]/@value").get('').strip()
        item['12 month Price'] = response.css(".card-selected .lease-price .ysp span ::text").get('').strip()
        best_value_price =  response.xpath("//*[contains(text(),'Best Value')]/parent::div[1]/following-sibling::div[1]/div[1]/span[1]/text()").get('').strip()
        best_value_month =  response.xpath("//*[contains(@data-selenium-id,'BVLeaseTerm')]/text()").get('').strip()
        best_value_text = response.xpath("//*[contains(@data-selenium-id,'BVLeaseTerm')]/parent::div[1]/following-sibling::div[1]/text()").get('').strip()
        item['Best Value Price and term'] =  f'{best_value_price} @ {best_value_month} {best_value_text}'
        yield item
