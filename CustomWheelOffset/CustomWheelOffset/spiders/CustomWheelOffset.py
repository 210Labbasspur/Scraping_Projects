import json
import scrapy
import datetime


class CustomWheelOffset(scrapy.Spider):
    name = 'CustomWheelOffset'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'PHPSESSID=dmga91rs5unn9helgsmj9g9s0p; _gcl_au=1.1.1897037265.1728039633; _ga=GA1.1.1253451634.1728039645; __attentive_id=dd92c08f1e8945deb52c75b987b47bd6; __attentive_cco=1728039653467; _clck=q1hpvy%7C2%7Cfpq%7C0%7C1738; __attentive_ss_referrer=ORGANIC; __attentive_dv=1; __hstc=192160757.247ecb0c3672bf99a26393bdaca76bc5.1728039658759.1728039658759.1728039658759.1; hubspotutk=247ecb0c3672bf99a26393bdaca76bc5; __hssrc=1; cookieconsent_status=dismiss; aws-waf-token=f2f4cc95-a417-4d5b-8a6c-4157e0d5c13b:EQoAidtNBiFTAAAA:8g2WtZ1bOleYcn82zYuIbIWclrtG6ja9RnFqBMzw2cyh7tjCABHLQ1I+y8ikUFN9bwEvCEp9Gnna0yvgrQWVUEBnGAXt3byEBVoksPbu8C9LMAO/0Xe1wPoCpgeLnTiftflAhUaSEmmyangZ9hib9SRJV0K9ytVSJeQkZjDE7AOsz7QkgllmorlSO5fm5+uCbUdZ4Iw4SmCTXiODqPplhSD4ClvE3GeuvNzAmp9gvf3jgy56hwHN6iEpP6FirMz7jz7lG9qzNZWUgrQ=; tracker_device_is_opt_in=true; tracker_device=7f4f3d6a-9dd0-467b-8b33-c39c2194688e; _ga_NQ7N6B82Q5=GS1.1.1728039645.1.1.1728040103.55.0.1849257081; __kla_id=eyJjaWQiOiJORFUyWVdJeU9EWXRNV0kzWXkwMFpqUTFMVGhqTXpRdE9EVTJOREkyWVdKa1l6YzAiLCIkcmVmZXJyZXIiOnsidHMiOjE3MjgwMzk2NDgsInZhbHVlIjoiIiwiZmlyc3RfcGFnZSI6Imh0dHBzOi8vd3d3LmN1c3RvbXdoZWVsb2Zmc2V0LmNvbS8ifSwiJGxhc3RfcmVmZXJyZXIiOnsidHMiOjE3MjgwNDAxMDQsInZhbHVlIjoiIiwiZmlyc3RfcGFnZSI6Imh0dHBzOi8vd3d3LmN1c3RvbXdoZWVsb2Zmc2V0LmNvbS8ifX0=; _uetsid=eb759b20823f11ef83b6afaf8ef030a9; _uetvid=eb75bf20823f11efbfa2c9f7f97568a9; __attentive_pv=9; __hssc=192160757.9.1728039658759; PHPSESSID=k3f8recjirvc78dpndoi84n1hf',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    custom_settings = {
        'FEED_URI': f'output/Fitment List - {datetime.datetime.now().strftime("%d-%m-%Y")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',

        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
            "scrapy_poet.InjectionMiddleware": 543,
        },
        "REQUEST_FINGERPRINTER_CLASS": "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ZYTE_API_KEY": "",  # Please enter your API Key here
        "ZYTE_API_TRANSPARENT_MODE": True,
        "ZYTE_API_EXPERIMENTAL_COOKIES_ENABLED": True,
    }


    def start_requests(self):
        url = 'https://www.customwheeloffset.com/'
        yield scrapy.Request(url, callback=self.year, headers=self.headers)


    def year(self, response):
        for years in response.css("#yearDrop .ymm-li"):
            year = years.css("::text").get('').strip()
            year_slug = years.css("::text").get('').strip()
            year_url = f'https://www.enthusiastenterprises.us/fitment/vehicle/co/{year_slug}'
            yield scrapy.Request(year_url, callback=self.make, headers=self.headers, meta={'year':year})


    def make(self, response):
        data = json.loads(response.text)
        if data:
            for make in data:
                year = response.meta['year']
                make_slug = make.replace(' ','+')
                make_url = response.url + f'/{make_slug}'
                yield scrapy.Request(make_url, callback=self.model, headers=self.headers, meta={'year':year, 'make':make})


    def model(self, response):
        data = json.loads(response.text)
        if data:
            for model in data:
                year = response.meta['year']
                make = response.meta['make']
                model_slug = model.replace(' ','+')
                model_url = response.url + f'/{model_slug}'
                yield scrapy.Request(model_url, callback=self.trim, headers=self.headers, meta={'year': year, 'make': make, 'model':model})


    def trim(self, response):
        data = json.loads(response.text)
        if data:
            for trim in data.get('trim',[]):
                year = response.meta['year']
                make = response.meta['make']
                model = response.meta['model']

                year_slug = year.replace(' ','+')
                make_slug = make.replace(' ','+')
                model_slug = model.replace(' ','+')
                trim_slug = trim.replace(' ','+')

                trim_url = f'https://www.enthusiastenterprises.us/fitment/vehicle/co/offsetguide/{year_slug}/{make_slug}/{model_slug}/trim/{trim_slug}/drives'
                yield scrapy.Request(trim_url, callback=self.drive, headers=self.headers, meta={'year': year, 'make': make, 'model':model, 'trim':trim})


    def drive(self, response):
        data = json.loads(response.text)
        if data:
            for drive in data:
                item = dict()
                item['Year'] = response.meta['year']
                item['Make'] = response.meta['make']
                item['Model'] = response.meta['model']
                item['Trim'] = response.meta['trim']
                item['Drive'] = drive
                yield item
