import json
import scrapy
import pandas as pd
from copy import deepcopy
from datetime import datetime
from urllib.parse import urljoin
# import pyexcel


class ZilloeSpider(scrapy.Spider):
    name = 'zillow_spider'
    time_stamp = datetime.now().strftime("%d_%b_%Y_%H_%M_%S")
    current_date = datetime.now().strftime("%Y/%m/%d")

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'ROBOTSTXT_OBEY': False,
        'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
        'FEEDS': {f'outputs/Zillow_{time_stamp}.xlsx': {'format': 'xlsx', 'overwrite': True}},
        "ZYTE_API_EXPERIMENTAL_COOKIES_ENABLED": True,
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        'DOWNLOADER_MIDDLEWARES': {
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
            'scrapy_poet.InjectionMiddleware': 543,
        },
        'REQUEST_FINGERPRINTER_CLASS': "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        'ZYTE_API_KEY': "7dcf43600b8d4e1eb7b6b8f375aba276",  # TODO: Please enter you api-key
        "ZYTE_API_TRANSPARENT_MODE": True,
    }
    url = 'https://www.zillow.com/homes/{}_rb/'
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    def start_requests(self):
        # input_addresses = pyexcel.get_records(file_name='inputs/input.xlsx')
        # for i in input_addresses[:]:
        #     url = deepcopy(self.url).format(i['Address'].replace(' ', '-'))
        #     yield scrapy.Request(url, headers=self.headers, meta={'address': i['Address']})

        input_addresses = pd.read_excel('inputs/input.xlsx').to_dict(orient='records')  # Load the Excel file using pandas
        for i in input_addresses:
            url = deepcopy(self.url).format(i['Address'].replace(' ', '-'))
            yield scrapy.Request(url, headers=self.headers, meta={'address': i['Address']})


    def parse(self, response, **kwargs):
        item = dict()
        item['Address'] = response.meta.get('address', '')
        try:
            data = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').get('')).get('props', {}).get('pageProps', {}).get('componentProps', {})
            data = json.loads(data.get('gdpClientCache', "{}"))
            key = list(data.keys())[0]
            data = data[key].get('property', {})
            item['Street'] = data.get('address', {}).get('streetAddress', '')
            item['City'] = data.get('address', {}).get('city', '')
            item['State'] = data.get('address', {}).get('state', '')
            item['Zip'] = data.get('address', {}).get('zipcode', '')
            item['URL'] = urljoin('https://www.zillow.com/', data.get('hdpUrl'))
            item['Zillow ID'] = data.get('zpid', '')
            item['Bedrooms'] = data.get('bedrooms', '')
            item['Bathrooms'] = data.get('bathrooms', '')
            item['Full bathrooms'] = data.get('resoFacts', {}).get('bathroomsFull', '')
            item['1/2 bathrooms'] = data.get('resoFacts', {}).get('bathroomsHalf', '')
            item['Total interior livable area'] = data.get('livingArea', '')
            item['Common walls with other units/homes'] = data.get('resoFacts', {}).get('commonWalls', '')
            item['Total structure area'] = data.get('livingAreaValue', '')
            item['Finished area above grade'] = data.get('aboveGradeFinishedArea', '')
            item['Finished area below grade'] = data.get('belowGradeFinishedArea', '')
            item['Garage spaces'] = data.get('garageParkingCapacity', '')
            item['Stories'] = data.get('resoFacts', {}).get('stories', '')
            item['Levels'] = data.get('resoFacts', {}).get('levels', '')
            item['Home type'] = data.get('resoFacts', {}).get('homeType', '')
            item['Architectural style'] = data.get('resoFacts', {}).get('architecturalStyle', '')
            item['Property subType'] = data.get('resoFacts', {}).get('propertySubType', '')
            item['New construction'] = data.get('resoFacts', {}).get('isNewConstruction', '')
            item['Year built'] = data.get('resoFacts', {}).get('yearBuilt', '')
            item['Construction materials'] = data.get('resoFacts', {}).get('constructionMaterials', [])
            item['Subdivision'] = data.get('resoFacts', {}).get('subdivisionName', '')
            item['First Sale Date'] = ''
            item['First Sale Price'] = ''
            item['First $ / Sq. Ft.'] = ''
            item['First Source'] = ''
            item['First MLS#'] = ''
            item['Overview'] = data.get('description')
            item['Source'] = ''
            item['MLS#'] = ''
            item['Sold on'] = ''
            item['Sold'] = ''
            if data.get('priceHistory'):
                item['First Sale Date'] = data.get('priceHistory', [])[-1].get('date')
                item['First Sale Price'] = data.get('priceHistory', [])[-1].get('price')
                item['First $ / Sq. Ft.'] = data.get('priceHistory', [])[-1].get('pricePerSquareFoot')
                item['First Source'] = data.get('priceHistory', [])[-1].get('source')
                item['First MLS#'] = data.get('priceHistory', [])[-1].get('attributeSource', {}).get('infoString1', '')
                item['Source'] = data.get('priceHistory', [])[0].get('source')
                item['MLS#'] = data.get('priceHistory', [])[0].get('attributeSource', {}).get('infoString1', '')
                item['Sold on'] = data.get('priceHistory', [])[0].get('date')
                item['Sold'] = data.get('priceHistory', [])[-1].get('price')
            item['Google Map Available'] = 'No'
            item['Google Map Link'] = ''
            if data.get('staticMap', {}).get('sources', []):
                item['Google Map Available'] = 'Yes'
                item['Google Map Link'] = data.get('staticMap', {}).get('sources', [])[-1].get('url', '')
            item['No. of Pictures'] = len(data.get('originalPhotos', []))
            item['Pictures'] = [i.get('mixedSources', {}).get('jpeg', [])[-1].get('url') for i in data.get('originalPhotos', [])]
            yield item
        except:
            yield item
