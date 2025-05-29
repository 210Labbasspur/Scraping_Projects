#############           Zillow_Canada

import os
import csv
import json
from copy import deepcopy
import scrapy
import datetime

class Zillow_Canada(scrapy.Spider):
    name = 'Zillow_Canada'
    prefix = 'https://www.zillow.com'
    url = 'https://www.zillow.com/async-create-search-page-state'
    headers = {'Content-Type': 'application/json'}
    data = {
        'searchQueryState': {
            'pagination': {
                'currentPage': 2,
            },
            'isMapVisible': True,
            'mapBounds': {
                'west': -79.83786584228515,
                'east': -79.56801415771484,
                'south': 44.31614001210359,
                'north': 44.384144514774164,
            },
            'usersSearchTerm': 'Mississauga Canada',
            'filterState': {
                'sortSelection': {
                    'value': 'globalrelevanceex',
                },
            },
            'isListVisible': True,
            'mapZoom': 12,
        },
        'wants': {
            'cat1': [
                'listResults',
                'mapResults',
            ],
            'cat2': [
                'total',
            ],
        },
        'requestId': 4,
        'isDebugRequest': False,
    }

    custom_settings = {
        #########################################################################################################
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        "DOWNLOADER_MIDDLEWARES": {
            'scrapy_poet.InjectionMiddleware': 543,  # You can adjust the priority number as needed
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
        },
        "REQUEST_FINGERPRINTER_CLASS": "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        # "ZYTE_API_KEY": f"Enter_Your_Zyte_API_Key_Here",  # Please enter your API Key here
        "ZYTE_API_KEY": f"b1ec0bb8aecc4d90b128e6615e9d3930",  # Please enter your API Key here
        "ZYTE_API_TRANSPARENT_MODE": True,
        "ZYTE_API_EXPERIMENTAL_COOKIES_ENABLED": True,
    }

    def __init__(self, *args, **kwargs):
        super(Zillow_Canada, self).__init__(*args, **kwargs)
        self.output_file = 'Output/Zillow_Canada.csv'  # Output CSV file
        self.output_dir = os.path.dirname(self.output_file)
        self.existing_property_ids = set()  # Set to store existing Property IDs

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.existing_property_ids.add(row['Zpid'])
        print(len(self.existing_property_ids),' = Existing_property_ids are : ', self.existing_property_ids)


    count = 1
    def start_requests(self):
        locations = []
        with open(f"input/Zillow_CA_Input.csv", mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                locations.append(dict(row))

        count = 0
        for location in locations:         ##     Toronto Canada       Brampton Canada       Mississauga Canada
            count += 1
            search_location = location.get('Location', '').strip()
            location_slug = search_location.lower().replace(' ', '-').replace(',', '')
            location_url = f'https://www.zillow.com/{location_slug}/'
            print(count, f" # Search Location is : {search_location} || Location URL is : {location_url}")
            yield scrapy.Request(location_url, callback=self.mapbounds_parse, headers=self.headers)


    def mapbounds_parse(self, response):
        json_data = response.css('#__NEXT_DATA__ ::text').get('').strip()
        data = json.loads(json_data)
        if data.get('props').get('pageProps').get('searchPageState').get('queryState'):
            mapBounds = dict()
            mapBounds['north'] = data.get('props').get('pageProps').get('searchPageState').get('queryState').get('mapBounds').get('north')
            mapBounds['south'] = data.get('props').get('pageProps').get('searchPageState').get('queryState').get('mapBounds').get('south')
            mapBounds['east'] = data.get('props').get('pageProps').get('searchPageState').get('queryState').get('mapBounds').get('east')
            mapBounds['west'] = data.get('props').get('pageProps').get('searchPageState').get('queryState').get('mapBounds').get('west')

            prod_no = 0
            page_no = 1
            payload = deepcopy(self.data)
            payload['searchQueryState']['pagination']['currentPage'] = page_no
            payload['searchQueryState']['mapBounds']['north'] = mapBounds['north']
            payload['searchQueryState']['mapBounds']['south'] = mapBounds['south']
            payload['searchQueryState']['mapBounds']['east'] = mapBounds['east']
            payload['searchQueryState']['mapBounds']['west'] = mapBounds['west']
            yield scrapy.Request(url=self.url, body=json.dumps(payload), method='PUT', callback=self.parse, headers=self.headers,
                     meta={'payload':payload,'page_no':page_no,'prod_no':prod_no,'mapBounds':mapBounds})



    def parse(self, response):
        prod_no = response.meta['prod_no']
        data = json.loads(response.text)
        if data:
            for house in data.get('cat1').get('searchResults').get('listResults'):
                property_id = house.get('zpid')
                prod_no += 1

                if property_id in self.existing_property_ids:
                    print(f'{property_id} : This property already exists in the output file')
                else:
                    self.existing_property_ids.add(property_id)

                    item = dict()
                    item['Zpid'] = house.get('zpid')

                    item['Street_address'] = house.get('addressStreet')
                    item['City'] = house.get('addressCity')
                    item['State'] = house.get('addressState')
                    item['ZipCode'] = house.get('addressZipcode')
                    item['Full Address'] = f"{item['Street_address']} {item['City']} {item['State']} {item['ZipCode']}"
                    item['Price'] = house.get('price')
                    item['Beds'] = house.get('beds')
                    item['Baths'] = house.get('baths')
                    item['Sqr_feet'] = house.get('area')
                    item['Home_Status'] = house.get('statusText')
                    if house.get('hdpData'):
                        item['Home_Type'] = house.get('hdpData').get('homeInfo').get('homeType')

                    item['Agent_name'] = ''
                    item['Agent_phone'] = ''

                    item['Listing Photos'] = []
                    if house.get('carouselPhotos'):
                        for images in house.get('carouselPhotos'):
                            item['Listing Photos'].append(images.get('url'))
                    item['Property_URL'] = house.get('detailUrl')
                    print(prod_no, " # Property is : ", item)

                    if 'C$' in item['Price']:  ### Identification that Canadanian Properties will have price in Canadian $
                        yield response.follow(url=house.get('detailUrl'), callback=self.parse_detail, headers=self.headers,
                                              meta={'item': item})
                    else:
                        print("This property is not from Canada because its price is not in C$ :: ", item)



            ##  Pagination
            # total_properties = data.get('cat1').get('searchList').get('totalResultCount')
            # print(f"Current-Offset = {prod_no} || Total Properties are : ", total_properties)
            # if prod_no < total_properties:
            #     page_no = response.meta['page_no'] + 1
            #     mapBounds = response.meta['mapBounds']
            #     payload = response.meta['payload']
            #     payload['searchQueryState']['pagination']['currentPage'] = page_no
            #     payload['searchQueryState']['mapBounds']['north'] = mapBounds['north']
            #     payload['searchQueryState']['mapBounds']['south'] = mapBounds['south']
            #     payload['searchQueryState']['mapBounds']['east'] = mapBounds['east']
            #     payload['searchQueryState']['mapBounds']['west'] = mapBounds['west']
            #     yield scrapy.Request(url=self.url, body=json.dumps(payload), method='PUT', callback=self.parse, headers=self.headers,
            #          meta={'payload':payload,'page_no':page_no,'prod_no':prod_no,'mapBounds':mapBounds})


    def parse_detail(self, response):
        item = response.meta['item']
        json_data = response.css('#__NEXT_DATA__ ::text').get('').strip()
        data = json.loads(json_data)
        if data.get('props').get('pageProps').get('componentProps').get('gdpClientCache'):
            r_data = json.loads(data.get('props').get('pageProps').get('componentProps').get('gdpClientCache'))
            zpid = int(item['Zpid'])
            zpid2 = {"zpid":zpid,"platform":"desktop","isDoubleScroll":True}
            req_field = {"zpid":zpid,"platform":"DESKTOP_WEB","formType":"OPAQUE","contactFormRenderParameter":zpid2,"skipCFRD":False,"ompPlatform":"web"}
            a_req_field = 'ForSaleShopperPlatformFullRenderQuery' + str(req_field).replace(' ','').replace('False','false').replace('True','true').replace('\'','\"')

            if r_data.get(a_req_field).get('property'):
                item['Agent_name'] = (r_data.get(a_req_field).get('property').get('attributionInfo').get('agentName'))
                item['Agent_phone'] = (r_data.get(a_req_field).get('property').get('attributionInfo').get('agentPhoneNumber'))

        self.save_to_csv(item)


    def save_to_csv(self, data):
        file_exists = os.path.exists(self.output_file)
        fieldnames = list(data.keys())
        with open(self.output_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
        print(f"Data saved successfully in '{self.output_file}' :: {data}")

