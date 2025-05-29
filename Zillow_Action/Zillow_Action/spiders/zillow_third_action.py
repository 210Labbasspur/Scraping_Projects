import os
import json
import scrapy
from copy import deepcopy


class zillow_third_action(scrapy.Spider):
    name = 'zillow_third_action'
    prefix = 'https://www.zillow.com'
    url = 'https://www.zillow.com/async-create-search-page-state'
    headers = {'Content-Type': 'application/json'}
    data = {
            'searchQueryState': {
                'isMapVisible': True,
                'mapBounds': {
                    'west': -92.43985490625002,
                    'east': -75.16934709375002,
                    'south': 25.142289758144372,
                    'north': 30.29416135224398,
                },
                'usersSearchTerm': 'FL',
                'regionSelection': [
                    {
                        'regionId': 14,
                        'regionType': 2,
                    },
                ],
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
                    'isForSaleForeclosure': {
                        'value': False,
                    },
                    'isPreMarketPreForeclosure': {
                        'value': True,
                    },
                    'doz': {
                        'value': '60',
                    },
                    'price': {
                        # 'max': 200000,
                        # 'min': 150000,
                    },

                },
                'isListVisible': True,
                'mapZoom': 6,
                'category': 'cat1',
                'pagination': {
                    'currentPage': 2,
                },
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
            'requestId': 15,
            'isDebugRequest': False,
        }
    custom_settings = { 'FEEDS': { f'Output/Third_Action/Zillow_Third_Action.json': { 'format': 'json', 'overwrite': True, 'encoding': 'utf-8', }, } }

    count = 1
    properties_database = []
    new_properties = []

    json_file_path = "Output/Third_Action/Zillow_Third_Action.json"
    def start_requests(self):
        yield scrapy.Request('https://quotes.toscrape.com/', callback=self.pre_parse)

    def pre_parse(self, response):
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r') as f:
                self.properties_database = json.load(f)
            if self.properties_database:  #####  Saving old_properties.json in new_properties.json
                for property in self.properties_database:
                    yield property
        else:
            self.properties_database = []


        ##  Extracting data using price range because Zillow only allows 25 pages pagination
        initial = 0
        inc = 25000
        final = 700000
        for i in range(initial, final+1, inc):
            if i + inc <= final:
                start = i
                end = i + inc
                page_no = 1
                offset = 0
                payload = deepcopy(self.data)
                payload['searchQueryState']['pagination']['currentPage'] = page_no
                payload['searchQueryState']['filterState']['price']['min'] = start
                payload['searchQueryState']['filterState']['price']['max'] = end
                print(f"start = {start} || End = {end} || Payloads = {payload}")
                yield scrapy.Request(url=self.url, body=json.dumps(payload), method='PUT', callback=self.parse, headers=self.headers,
                                     meta={'page_no':page_no,'offset':offset, 'payload':payload})

        #### This one is called at the end from price range || from = 700k --> To= Unlimited (Any Price)
        page_no = 1
        offset = 0
        payload = deepcopy(self.data)
        payload['searchQueryState']['pagination']['currentPage'] = page_no
        payload['searchQueryState']['filterState']['price']['min'] = 700000
        print(f"start = 700000 || End = infinite || Payloads = {payload}")
        yield scrapy.Request(url=self.url, body=json.dumps(payload), method='PUT', callback=self.parse, headers=self.headers,
                             meta={'page_no':page_no,'offset':offset, 'payload':payload})


    def parse(self, response):
        offset = response.meta['offset']
        data = json.loads(response.text)
        if data:
            for house in data.get('cat1').get('searchResults').get('listResults'):
                offset += 1
                scrape_property = True

                for property_data in self.properties_database:
                    database_zpid = property_data.get('Zpid','')
                    if database_zpid == house.get('zpid'):
                        print('This property from Website exists in the database')
                        if 'sold' in house.get('statusText').lower():
                            print('This property is sold, remove it from JSON')
                            self.properties_database.remove(property_data)
                        scrape_property = False
                        break   ##  This break is important - Keep it

                if scrape_property == True:
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
                    item['Agent_name'] = ''
                    item['Agent_phone'] = ''
                    item['Event Description'] = ''

                    item['Listing Photos'] = []
                    if house.get('carouselPhotos'):
                        for images in house.get('carouselPhotos'):
                            item['Listing Photos'].append(images.get('url'))
                    item['Complete_url'] = house.get('detailUrl')
                    item['URL'] = house.get('detailUrl')
                    yield response.follow(url=house.get('detailUrl'), callback=self.parse_detail, headers=self.headers, meta={'item':item})


            total_offset = data.get('cat1').get('searchList').get('totalResultCount')
            print(f"Current-offset = {offset} || Total-offset are : ", total_offset)
            if offset < total_offset:
                page_no = response.meta['page_no'] + 1
                payload = response.meta['payload']
                payload['searchQueryState']['pagination']['currentPage'] = page_no
                yield scrapy.Request(url=self.url, body=json.dumps(payload), method='PUT', callback=self.parse, headers=self.headers,
                                     meta={'page_no':page_no,'offset':offset, 'payload':payload})

    def parse_detail(self, response):
        item = response.meta['item']
        json_data = response.css('#__NEXT_DATA__ ::text').get('').strip()
        data = json.loads(json_data)
        if data.get('props').get('pageProps').get('componentProps').get('gdpClientCache'):
            r_data = json.loads(data.get('props').get('pageProps').get('componentProps').get('gdpClientCache'))

            property_dict = {}
            for value in r_data.values():
                nested_dict = value if isinstance(value, dict) else None
                property_dict = nested_dict.get('property') if nested_dict.get('property') else None

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

                item['Agent_name'] = (property_dict.get('attributionInfo').get('agentName'))
                item['Agent_phone'] = (property_dict.get('attributionInfo').get('agentPhoneNumber'))
                item['Price History'] = property_dict.get('priceHistory')
                item['Tax History'] = property_dict.get('taxHistory')

                foreclosure = dict()
                foreclosure['foreclosingBank'] = property_dict.get('foreclosingBank','')
                foreclosure['foreclosureAmount'] = property_dict.get('foreclosureAmount','')
                foreclosure['foreclosureAuctionCity'] = property_dict.get('foreclosureAuctionCity','')
                foreclosure['foreclosureAuctionDescription'] = property_dict.get('foreclosureAuctionDescription','')
                foreclosure['foreclosureAuctionFilingDate'] = property_dict.get('foreclosureAuctionFilingDate','')
                foreclosure['foreclosureAuctionLocation'] = property_dict.get('foreclosureAuctionLocation','')
                foreclosure['foreclosureAuctionTime'] = property_dict.get('foreclosureAuctionTime','')
                foreclosure['foreclosureBalanceReportingDate'] = property_dict.get('foreclosureBalanceReportingDate','')
                foreclosure['foreclosureDate'] = property_dict.get('foreclosureDate','')
                foreclosure['foreclosureDefaultDescription'] = property_dict.get('foreclosureDefaultDescription','')
                foreclosure['foreclosureDefaultFilingDate'] = property_dict.get('foreclosureDefaultFilingDate','')
                foreclosure['foreclosureJudicialType'] = property_dict.get('foreclosureJudicialType','')
                foreclosure['foreclosureLoanAmount'] = property_dict.get('foreclosureLoanAmount','')
                foreclosure['foreclosureLoanDate'] = property_dict.get('foreclosureLoanDate','')
                foreclosure['foreclosureLoanOriginator'] = property_dict.get('foreclosureLoanOriginator','')
                foreclosure['foreclosurePastDueBalance'] = property_dict.get('foreclosurePastDueBalance','')
                foreclosure['foreclosurePriorSaleAmount'] = property_dict.get('foreclosurePriorSaleAmount','')
                foreclosure['foreclosurePriorSaleDate'] = property_dict.get('foreclosurePriorSaleDate','')
                foreclosure['foreclosureUnpaidBalance'] = property_dict.get('foreclosureUnpaidBalance','')
                foreclosure['foreclosureTypes'] = property_dict.get('foreclosureTypes')
                foreclosure['foreclosureMoreInfo'] = property_dict.get('foreclosureMoreInfo')
                item['Foreclosure Details'] = foreclosure

                beds, baths = item['Beds'], item['Baths']
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

        yield item
        self.new_properties.append(item)


    def close(self, reason):
        all_properties = self.properties_database + self.new_properties
        print(f"Saved {len(all_properties)} properties to {self.json_file_path}")
        print(f"Spider closed. {len(self.new_properties)} new properties added.")
