import os
import csv
import json
import scrapy
from copy import deepcopy
from datetime import datetime

class ACVAuctions(scrapy.Spider):
    name = 'acvauctions'
    url = "https://easy-pass.acvauctions.com/bff/filters/auctions/buying/active"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
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
    data = {
          "filters": [],
          "savedSearchIds": [10052744],
          "size": 100,
          "includeCounts": False,
        }

    login_data = {
        'email': 'marathonmotorsco@gmail.com',
        'password': 'Acv2023!',
        'web': True,
    }

    def start_requests(self):
        file_path = f'output/acvauctions - {datetime.now().strftime("%d-%m-%Y")}.csv'
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f'{file_path} has been deleted.')

        payload = deepcopy(self.login_data)
        login_url = 'https://mobile-gateway.acvauctions.com/api/legacylogin/v2'
        yield scrapy.Request(url=login_url, body=json.dumps(payload), method='POST', callback=self.login_parse, headers=self.headers)

    def login_parse(self, response):
        data = json.loads(response.text)
        jwtToken = data.get('jwtToken')

        payload = deepcopy(self.data)
        headers = deepcopy(self.headers)
        headers['authorization'] = f'Bearer {jwtToken}'
        yield scrapy.Request(url=self.url, body=json.dumps(payload), method='POST', callback=self.parse, headers=headers,
                             meta={'headers':headers})

    def parse(self, response):
        data = json.loads(response.text)
        for vehicle in data.get('data').get('results'):
            item = dict()
            id = vehicle.get('id')
            item['ID'] = id

            item['VIN'] = vehicle.get('vin')
            item['Mileage'] = vehicle.get('odometer')

            req_api_url = 'https://easy-pass.acvauctions.com/bff/auctions/buying/search/auction/' + str(id)
            headers = response.meta['headers']
            yield scrapy.Request(url=req_api_url, callback=self.detail_parse, headers=headers,
                                 meta={'headers': headers, 'item':item})

    def detail_parse(self, response):
        data = json.loads(response.text)
        item = response.meta['item']

        data = data.get('data')
        if data:
            item['Zip'] = data.get('sellerInfo').get('zipCode')
            for color in data['displayInfo']:
                if color.get('name') == "Color":
                    item['Color'] = color.get('value')
                    break

            item['Leather'], item['Sunroof'], item['Navigation'] = None, None, None
            for feature in data.get('conditionReport').get('sections'):
                if feature.get('title') == "Interior":
                    for f in feature.get('subsections')[0].get('questions'):
                        if f.get('title') == "Leather or Leather Type Seats":
                            item['Leather'] = f.get('yesNo')
                        if f.get('title') == "Sunroof":
                            item['Sunroof'] = f.get('yesNo')
                        if f.get('title') == "Navigation":
                            item['Navigation'] = f.get('yesNo')

            with open(f'output/acvauctions - {datetime.now().strftime("%d-%m-%Y")}.csv', 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['ID', 'VIN', 'Mileage', 'Zip', 'Color', 'Leather', 'Sunroof', 'Navigation']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if csvfile.tell() == 0:
                    writer.writeheader()
                writer.writerow(item)
                print('Data entered : ', item)
