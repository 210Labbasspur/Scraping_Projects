import scrapy
import datetime
from urllib.parse import urlparse, parse_qs

class onnifultonmarket(scrapy.Spider):
    name = 'onnifultonmarket'
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
        'FEED_URI': f'output/Onni Fulton Market Floorplans - {datetime.datetime.now().strftime("%d-%m-%Y")}.csv',
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
        url = 'https://www.onnifultonmarket.com/floorplans?gad_source=1&gclid=CjwKCAjwnqK1BhBvEiwAi7o0X2DCt7uBFErRnMb4pxQmz55jgiYd1G2yqVZGEg3-sEDhNkyzlq9GzhoC-T8QAvD_BwE'
        yield scrapy.Request(url=url, callback=self.parse, headers=self.headers, )

    def parse(self, response):
        loop = response.xpath("//*[contains(@class,'btn btn-primary btn-block btn-block track-apply floorplan-action-button')]")
        for index, floor in enumerate(loop):
            floor_url = floor.css('::attr(href)').get('').strip()
            print(index+1, floor_url)
            floor_url = response.urljoin(floor_url)
            yield response.follow(url=floor_url, callback=self.detail_parse, headers=self.headers,)

    def detail_parse(self, response):
        unit_size = response.xpath("//*[contains(@data-selenium-id,'SID_h1Tag')]/text()").get('').strip().replace('-','').replace('THE SHOREHAM','')
        bed_bath = response.xpath("//*[contains(@class,'row mb-4 pt-5 justify-content-between align-items-center')]/div[1]/div[1]")
        bed = bed_bath.xpath(".//span[contains(text(),'Bedroom')]/text()").get('').strip().replace('Bedroom','').replace(' ','').replace('s','')
        bath = bed_bath.xpath(".//span[contains(text(),'Bathroom')]/text()").get('').strip().replace('Bathroom','').replace(' ','').replace('s','')
        for appartment in response.css('.unit-container'):
            item = dict()
            item['Building Name'] = 'Onni Fulton Market'
            item['Unit size'] = unit_size.replace('  ','')
            for unit in appartment.css('.td-card-name ::text').getall():
                if '#' in unit:
                    item['Unit #'] = unit.strip().replace('#','')
            item['Beds'] = bed
            item['Bath'] = bath
            item['Sq. Ft.'] = appartment.xpath(".//*[contains(@class,'td-card-sqft')]/text()").get('').strip()

            input_pricing_url = appartment.css(".td-card-footer a ::attr(href)").get('').strip()
            parsed_url = urlparse(input_pricing_url)
            query_params = parse_qs(parsed_url.query)
            myolepropertyid = query_params.get('myOlePropertyId', [None])[0]
            unitid = query_params.get('UnitID', [None])[0]
            floorplanid = query_params.get('FloorPlanID', [None])[0]
            moveindate = query_params.get('MoveInDate', [None])[0]
            pricingcallback = unitid
            required_pricing_url = (f'https://onnifultonmarket.securecafe.com/onlineleasing/rcLoadContent.ashx?contentclass='
                                    f'oleapplication&stepname=RentalOptions&myOlePropertyId={myolepropertyid}&UnitID={unitid}&FloorPlanID'
                                    f'={floorplanid}&MoveInDate={moveindate}&sLeaseTerm=12&sGuestRISelectionItems=&PricingCallBack={pricingcallback}')

            yield response.follow(url=required_pricing_url, callback=self.pricing_parse, headers=self.headers,
                                  meta={'item': item})

    def pricing_parse(self, response):
        item = response.meta['item']
        item['Available Date'] = response.css("input#sMoveInDate ::attr(value)").get('').strip()
        item['12 month Price'] = response.xpath("//*[contains(text(),'Rent:')]/parent::div[1]/following-sibling::div[1]/label[1]/text()").get('').strip()

        best_value =  response.xpath("//*[contains(text(),'Best Value')]/parent::div[1]/following-sibling::div[1]/label[1]/i[1]/text()").getall()
        best_value_price, best_value_month, best_value_text = None, None, None
        for bv in best_value:
            if 'month' in bv:
                best_value_month, best_value_text = bv.split()[:2]
            if '$' in bv:
                best_value_price = bv.strip()
        item['Best Value Price and term'] =  f'{best_value_price} @ {best_value_month} {best_value_text}'

        if best_value_price:
            yield item
