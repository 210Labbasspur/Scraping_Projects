import csv
import json
import scrapy
from openpyxl import load_workbook

class AxisGIS(scrapy.Spider):
    name = 'AxisGIS'
    prefix = 'https://api.axisgis.com'
    # url = "https://api.axisgis.com/node/axisapi/search/BristolRI?f=json&q=First%20School"
    url = "https://api.axisgis.com/node/axisapi/search/BristolRI?f=json&q={}"

    # product_url = "https://api.axisgis.com/node/axisapi/parcelbycama/BristolRI?f=json&q=24-65"
    product_url = "https://api.axisgis.com/node/axisapi/parcelbycama/BristolRI?f=json&q={}"

    # url = "https://api.axisgis.com/node/axisapi/documents/BristolRI?f=json&q=24-65"
    NEReval_url = "https://api.axisgis.com/node/axisapi/documents/BristolRI?f=json&q={}"
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'origin': 'https://next.axisgis.com',
        'referer': 'https://next.axisgis.com/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    # custom_settings = {'FEED_URI': 'output/AxisGIS Record.csv',
    #                    'FEED_FORMAT': 'csv',
    #                    'FEED_EXPORT_ENCODING': 'utf-8-sig', }

    custom_settings = { 'FEED_URI': 'output/AxisGIS Complete Record.xlsx',
                        'FEED_FORMAT': 'xlsx',
                        'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
                        'FEED_EXPORT_ENCODING': 'utf-8', }


    def start_requests(self):
        file_path = "input/Bristol Property Addresses.xlsx"
        sheet_name = 'Sheet1'  # Update with your sheet name
        workbook = load_workbook(filename=file_path)
        sheet = workbook[sheet_name]
        addresses = []
        for cell in sheet['A']:
            addresses.append(cell.value)

        count = 1
        for address in addresses:#[:35]:
            print(count, 'Search Address is :', address)
            count += 1
            search_address = address.replace(' ','%20')
            yield scrapy.Request(url=self.url.format(search_address), callback=self.parse, headers=self.headers)


    def parse(self, response):
        data = json.loads(response.text)
        for address in data['results']:
            q = address.get('ParcelNumber')
            yield scrapy.Request(url=self.product_url.format(q), callback=self.detail_parse, headers=self.headers)


    def detail_parse(self, response):
        data = json.loads(response.text)
        if data['Properties']:
            item = dict()
            item['PropertyAddress'] = data['Properties'][0]['PropertyAddress']
            item['MapSheet'] = data['Properties'][0]['MapSheet']
            item['OwnerName'] = data['Properties'][0]['OwnerName']
            item['OwnerAddress'] = data['Properties'][0]['OwnerAddress']
            item['OwnerAddress2'] = data['Properties'][0]['OwnerAddress2']
            item['OwnerCity'] = data['Properties'][0]['OwnerCity']
            item['OwnerState'] = data['Properties'][0]['OwnerState']
            item['OwnerZip'] = data['Properties'][0]['OwnerZip']
            item['Zone1'] = data['Properties'][0]['Zone1']
            item['TotalAcres'] = data['Properties'][0]['TotalAcres']
            item['YearBuilt'] = data['Properties'][0]['YearBuilt']
            item['BuildType'] = data['Properties'][0]['BuildType']
            item['FinArea'] = data['Properties'][0]['FinArea']
            item['TotalLandValue'] = data['Properties'][0]['TotalLandValue']
            item['TotalBuildingValue'] = data['Properties'][0]['TotalBuildingValue']

            q = data['Properties'][0]['ParcelNumber']
            yield scrapy.Request(url=self.NEReval_url.format(q), callback=self.detail_parse2, headers=self.headers,
                                 meta={'item':item})

    def detail_parse2(self, response):
        data = json.loads(response.text)
        item = response.meta['item']

        for results in data['results']:
            if results.get('Category') ==  "NEReval Property Card":
                item['NEReval Property Card'] = results.get('FileName')

                yield item
