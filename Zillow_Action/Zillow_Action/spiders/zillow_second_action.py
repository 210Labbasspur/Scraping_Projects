import os
import csv
import json
import scrapy
import datetime
from copy import deepcopy
import requests

class zillow_second_action(scrapy.Spider):
    name = 'zillow_second_action'
    prefix = 'https://www.zillow.com'
    url = 'https://www.zillow.com/async-create-search-page-state'
    data = {
            'searchQueryState': {
                'isMapVisible': True,
                'mapBounds': {
                    # 'west': -92.43985490625002,
                    # 'east': -75.16934709375002,
                    # 'south': 25.142289758144372,
                    # 'north': 30.29416135224398,
                },
                # 'usersSearchTerm': 'FL',
                # 'regionSelection': [
                #     {
                #         'regionId': 14,
                #         'regionType': 2,
                #     },
                # ],
                'filterState': {
                    'sortSelection': {
                        'value': 'globalrelevanceex',
                    },
                    'isForSaleByAgent': {
                        'value': False,
                    },
                    'isForSaleByOwner': {
                        'value': False,
                    },
                    'isNewConstruction': {
                        'value': False,
                    },
                    'isComingSoon': {
                        'value': False,
                    },
                    'isAuction': {
                        'value': False,
                    },
                    'isForSaleForeclosure': {
                        'value': False,
                    },
                    'isPreMarketPreForeclosure': {
                        'value': True,
                    },
                    'price': {
                        # 'max': 200000,
                        # 'min': 150000,
                    },
                },
                'isListVisible': True,
                # 'mapZoom': 4,
                # 'mapZoom': 6,
                # 'category': 'cat2',
                'pagination': {
                    'currentPage': 1,
                },
            },
            'wants': {
                'cat2': [
                    'listResults',
                    'mapResults',
                ],
                'cat1': [
                    'total',
                ],
            },
            # 'requestId': 5,
            # 'requestId': 8,
            'isDebugRequest': False,
        }
    headers = {'Content-Type': 'application/json'}
    custom_settings = { 'FEEDS': { f'Output/Second_Action/Zillow_Second_Action_New.json': { 'format': 'json', 'overwrite': True, 'encoding': 'utf-8', }, } }

    count = 1
    old_properties_zpids = []
    old_properties = []
    new_properties = []

    old_json_file_path = "Output/Second_Action/Zillow_Second_Action_Old.json"
    database_csv_file_path = "Output/Second_Action/Zillow_Second_Action_Database.csv"

    def start_requests(self):
        yield scrapy.Request('https://quotes.toscrape.com/', callback=self.pre_parse)

    def pre_parse(self, response):
        ##  Reading old Database JSON file to save it in Zillow_Second_Action_New.json at the end.
        if os.path.exists(self.old_json_file_path):
            with open(self.old_json_file_path, 'r') as f:
                self.old_properties = json.load(f)
            if self.old_properties:  #####  Saving old_properties.json in new_properties.json
                for property in self.old_properties:
                    yield property
        else:
            self.old_properties = []

        ##  Reading Database csv file
        if os.path.exists(self.database_csv_file_path):
            with open(self.database_csv_file_path, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                self.old_properties_zpids = [row[0] for row in reader if row]  # Extract ZPIDs from the Database csv file
        else:
            self.old_properties_zpids = []
        print('self.old_properties_zpids extracted from Database CSV are : ', self.old_properties_zpids)

        locations = []
        with open('input/locations_list.txt', 'r') as file:
            for line in file:
                location = line.strip().replace('\x00', '')
                locations.append(location) if location else None

        count = 0
        for location in locations:
            count += 1
            print(count, '# Location is : ', location)
            location_slug = location.lower().replace(' ', '-').replace(',', '')
            location_url = f'https://www.zillow.com/{location_slug}/'
            yield scrapy.Request(location_url, callback=self.parse1, headers={'Content-Type': 'application/json'},)


    def parse1(self, response):
        data = json.loads(response.css('#__NEXT_DATA__ ::text').get('').strip())
        if data.get('props').get('pageProps').get('searchPageState').get('queryState'):
            mapBounds = dict()
            mapBounds['north'] = data.get('props').get('pageProps').get('searchPageState').get('queryState').get('mapBounds').get('north')
            mapBounds['south'] = data.get('props').get('pageProps').get('searchPageState').get('queryState').get('mapBounds').get('south')
            mapBounds['east'] = data.get('props').get('pageProps').get('searchPageState').get('queryState').get('mapBounds').get('east')
            mapBounds['west'] = data.get('props').get('pageProps').get('searchPageState').get('queryState').get('mapBounds').get('west')

            payload = deepcopy(self.data)
            payload['searchQueryState']['mapBounds']['north'] = mapBounds['north']
            payload['searchQueryState']['mapBounds']['south'] = mapBounds['south']
            payload['searchQueryState']['mapBounds']['east'] = mapBounds['east']
            payload['searchQueryState']['mapBounds']['west'] = mapBounds['west']

            initial = 0
            inc = 25000
            final = 700000
            for i in range(initial, final+1, inc):
                if i + inc <= final:
                    start = i
                    end = i + inc
                    page_no = 1
                    offset = 0
                    payload['searchQueryState']['pagination']['currentPage'] = page_no
                    payload['searchQueryState']['filterState']['price']['min'] = start
                    payload['searchQueryState']['filterState']['price']['max'] = end
                    yield scrapy.Request(url=self.url, body=json.dumps(payload), method='PUT', callback=self.parse, headers=self.headers,
                                         meta={'page_no':page_no,'offset':offset, 'payload':payload,'mapBounds':mapBounds})

            #### This one is called at the end from price range || from = 700k --> To= Unlimited (Any Price)
            page_no = 1
            offset = 0
            payload['searchQueryState']['pagination']['currentPage'] = page_no
            payload['searchQueryState']['filterState']['price']['min'] = 700000
            yield scrapy.Request(url=self.url, body=json.dumps(payload), method='PUT', callback=self.parse, headers=self.headers,
                                 meta={'page_no':page_no,'offset':offset, 'payload':payload,'mapBounds':mapBounds})


    def parse(self, response):
        offset = response.meta['offset']
        data = json.loads(response.text)
        if data:
            for house in data.get('cat2').get('searchResults').get('listResults'):
                offset += 1

                if house.get('zpid') in self.old_properties_zpids:
                        print('This property already exists in the database', house.get('zpid'), '||', house.get('addressStreet'))

                ## This is to ensure that script only extracts IL, CA and FL states.
                elif house.get('addressState') == 'IL' or house.get('addressState') == 'CA' or house.get('addressState') == 'FL':
                    print(offset, '# This is the new property, lets process this :',house.get('zpid'), '||', house.get('addressStreet'))

                    item = dict()
                    item['Zpid'] = house.get('zpid')
                    item['Street_address'] = house.get('addressStreet')
                    item['City'] = house.get('addressCity')
                    item['State'] = house.get('addressState')
                    item['ZipCode'] = house.get('addressZipcode')
                    item['Price'] = house.get('price')
                    item['Beds'] = house.get('beds')
                    item['Baths'] = house.get('baths')
                    item['Sqr_feet'] = house.get('area')
                    item['Home_Status'] = house.get('statusText')
                    if house.get('hdpData'):
                        item['Zestimate'] = house.get('hdpData').get('homeInfo').get('zestimate')
                        item['RentZestimate'] = house.get('hdpData').get('homeInfo').get('rentZestimate')
                        item['Days_on_zillow'] = house.get('hdpData').get('homeInfo').get('daysOnZillow')
                        item['Home_Type'] = house.get('hdpData').get('homeInfo').get('homeType')

                    item['Lat_Long'] = house.get('latLong')
                    item['Broker_Name'] = house.get('brokerName')
                    item['Event Description'] = ''

                    item['Listing Photos'] = []
                    if house.get('carouselPhotos'):
                        for images in house.get('carouselPhotos'):
                            item['Listing Photos'].append(images.get('url'))
                    item['Complete_url'] = house.get('detailUrl')
                    item['URL'] = house.get('detailUrl')
                    yield response.follow(url=house.get('detailUrl'), callback=self.parse_detail, headers=self.headers, meta={'item':item})


            total_offset = data.get('cat2').get('searchList').get('totalResultCount')
            print(f"Current offset : {offset} || Total offset is : ", total_offset)
            if offset < total_offset:
                page_no = response.meta['page_no'] + 1
                payload = response.meta['payload']
                mapBounds = response.meta['mapBounds']
                payload['searchQueryState']['pagination']['currentPage'] = page_no
                payload['searchQueryState']['mapBounds']['north'] = mapBounds['north']
                payload['searchQueryState']['mapBounds']['south'] = mapBounds['south']
                payload['searchQueryState']['mapBounds']['east'] = mapBounds['east']
                payload['searchQueryState']['mapBounds']['west'] = mapBounds['west']
                yield scrapy.Request(url=self.url, body=json.dumps(payload), method='PUT', callback=self.parse, headers=self.headers,
                                     meta={'page_no':page_no,'offset':offset, 'payload':payload,'mapBounds':mapBounds})


    def parse_detail(self, response):
        item = response.meta['item']
        data = json.loads(response.css('#__NEXT_DATA__ ::text').get('').strip())
        if data.get('props').get('pageProps').get('componentProps').get('gdpClientCache'):
            r_data = json.loads(data.get('props').get('pageProps').get('componentProps').get('gdpClientCache'))
            property_dict = {}
            for value in r_data.values():
                nested_dict = value if isinstance(value, dict) else None
                property_dict = nested_dict.get('property') if nested_dict.get('property') else None
                break   ##  This break is important - (Keep it)

            if property_dict:
                item['Structure Area'] = property_dict.get('resoFacts', {}).get('buildingArea', '')
                item['Type'] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts', []) if feature.get('factLabel') == 'Type'), '')
                item["Year Built"] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts', []) if feature.get('factLabel') == 'Year Built'), '')
                item['Heating'] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts', []) if feature.get('factLabel') == 'Heating'), '')
                item['Cooling'] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts', []) if feature.get('factLabel') == 'Cooling'), '')
                item['Parking'] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts', []) if feature.get('factLabel') == 'Parking'), '')
                item['HOA'] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts', []) if feature.get('factLabel') == 'HOA'), '')
                item['Lot'] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts', []) if feature.get('factLabel') == 'Lot'), '')
                item['Price/sqft'] = next((feature.get('factValue') for feature in property_dict.get('resoFacts', {}).get('atAGlanceFacts', []) if feature.get('factLabel') == 'Price/sqft'), '')
                item["Offer Review Date"] = next((feature.get('factValue') for feature in property_dict.get('resoFacts',{}).get('atAGlanceFacts', []) if feature.get('factLabel') == 'Offer Review Date'), '')

                property_ = property_dict
                foreclosure_more_details = property_.get('foreclosureMoreInfo')
                
                foreclosure_details = {
                    **foreclosure_more_details,
                    "foreclosureDefaultFilingDate": property_.get("foreclosureDefaultFilingDate"),
                    "foreclosureAuctionFilingDate": property_.get("foreclosureAuctionFilingDate"),
                    "foreclosureLoanDate": property_.get("foreclosureLoanDate"),
                    "foreclosureLoanOriginator": property_.get("foreclosureLoanOriginator"),
                    "foreclosureLoanAmount": property_.get("foreclosureLoanAmount"),
                    "foreclosurePriorSaleDate": property_.get("foreclosurePriorSaleDate"),
                    "foreclosurePriorSaleAmount": property_.get("foreclosurePriorSaleAmount"),
                    "foreclosureBalanceReportingDate": property_.get("foreclosureBalanceReportingDate"),
                    "foreclosureDefaultDescription": property_.get("foreclosureDefaultDescription"),
                    "foreclosurePastDueBalance": property_.get("foreclosurePastDueBalance"),
                    "foreclosureUnpaidBalance": property_.get("foreclosureUnpaidBalance"),
                    "foreclosureAuctionTime": property_.get("foreclosureAuctionTime"),
                    "foreclosureAuctionDescription": property_.get("foreclosureAuctionDescription"),
                    "foreclosureAuctionCity": property_.get("foreclosureAuctionCity"),
                    "foreclosureAuctionLocation": property_.get("foreclosureAuctionLocation"),
                    "foreclosureDate": property_.get("foreclosureDate"),
                    "foreclosureAmount": property_.get("foreclosureAmount"),
                    "foreclosingBank": property_.get("foreclosingBank"),
                    "foreclosureJudicialType": property_.get("foreclosureJudicialType"),
                }
                
                item["Foreclosure Details"] = foreclosure_details
                item['Agent_name'] = (property_dict.get('attributionInfo').get('agentName'))
                item['Agent_phone'] = (property_dict.get('attributionInfo').get('agentPhoneNumber'))
                beds, baths = item['Beds'], item['Baths']

                item['Price History'] = property_dict.get('priceHistory')
                item['Tax History'] = property_dict.get('taxHistory')

                item['Nearby Homes'] = []
                try:
                    for nearby_home in property_dict.get('nearbyHomes',[]):
                        if 'sold' in nearby_home.get('homeStatus', '').lower():
                            if nearby_home.get('bedrooms') == beds and nearby_home.get('bathrooms') == baths:
                                item['Nearby Homes'].append(nearby_home)
                except:
                    print('Could not save Nearby Homes - ', item)

                item['Comparable Homes'] = []
                try:
                    if property_dict.get('homeValuation', {}):
                        for comp_home in property_dict.get('homeValuation', {}).get('comparables',{}).get('comps',[]):
                            if 'sold' in comp_home.get('property', {}).get('homeStatus', '').lower():
                                if (comp_home.get('property', {}).get('bedrooms') == beds and comp_home.get('property', {}).get('bathrooms') == baths):
                                    item['Comparable Homes'].append(comp_home.get('property'))
                except:
                    print('Could not save Comparable Homes - ', item)

                if property_dict.get('description'):
                    item['Event Description'] = property_dict.get('description').replace('\n','').replace('\t','')

        self.send_to_safa_crm(item)

        os.makedirs(os.path.dirname(self.database_csv_file_path), exist_ok=True)
        path = self.database_csv_file_path
        file_exists = os.path.isfile(path)
        with open(path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Zpid'])
            if not file_exists:
                writer.writeheader()
            writer.writerow({'Zpid': item.get('Zpid')})
        print('New property ZPID has been saved inside the Property Database CSV file || ',item.get('Zpid'))

        yield item
        self.new_properties.append(item)


    def close(self, reason):        # Saving old+new properies in old_properties.json at the end of the scipt.
        print(' *** Close method is being called at the end of the scipt. Reason =', reason, ' ***')
        all_properties = self.old_properties + self.new_properties

        os.makedirs(os.path.dirname(self.old_json_file_path), exist_ok=True)
        with open(self.old_json_file_path, 'w') as json_file:
            json.dump(all_properties, json_file, indent=4)
        print(f"Saved {len(all_properties)} properties to {self.old_json_file_path}")
        print(f"Spider closed. {len(self.new_properties)} new properties added.")


    def send_to_safa_crm(self, item):
        print("Welcome to SAFA CRM Method")
        # Send item data to Safa CRM API here
        try:
            url = "http://34.228.119.194/api/zillow/add_lead"
            headers = {
                'x-api-key': '3BABE16B9C7C9BBD',
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=json.dumps(item))
            print(f"Safa CRM for {item['Zpid']} response: {response.text}, ", )
        except:
            pass
