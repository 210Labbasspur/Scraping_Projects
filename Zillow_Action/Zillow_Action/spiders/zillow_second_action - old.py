# import os
# import csv
# import json
# import scrapy
# import datetime
# from copy import deepcopy
#
#
# class zillow_second_action(scrapy.Spider):
#     name = 'zillow_second_action'
#     prefix = 'https://www.zillow.com'
#     url = 'https://www.zillow.com/async-create-search-page-state'
#     data = {
#             'searchQueryState': {
#                 'isMapVisible': True,
#                 'mapBounds': {
#                     'west': -92.43985490625002,
#                     'east': -75.16934709375002,
#                     'south': 25.142289758144372,
#                     'north': 30.29416135224398,
#                 },
#                 'usersSearchTerm': 'FL',
#                 'regionSelection': [
#                     {
#                         'regionId': 14,
#                         'regionType': 2,
#                     },
#                 ],
#                 'filterState': {
#                     'sortSelection': {
#                         'value': 'globalrelevanceex',
#                     },
#                     'isForSaleByAgent': {
#                         'value': False,
#                     },
#                     'isForSaleByOwner': {
#                         'value': False,
#                     },
#                     'isNewConstruction': {
#                         'value': False,
#                     },
#                     'isComingSoon': {
#                         'value': False,
#                     },
#                     'isAuction': {
#                         'value': False,
#                     },
#                     'isForSaleForeclosure': {
#                         'value': False,
#                     },
#                     'isPreMarketPreForeclosure': {
#                         'value': True,
#                     },
#                     'price': {
#                         # 'max': 200000,
#                         # 'min': 150000,
#                     },
#                 },
#                 'isListVisible': True,
#                 'mapZoom': 6,
#                 'category': 'cat2',
#                 'pagination': {
#                     'currentPage': 2,
#                 },
#             },
#             'wants': {
#                 'cat2': [
#                     'listResults',
#                     'mapResults',
#                 ],
#                 'cat1': [
#                     'total',
#                 ],
#             },
#             'requestId': 5,
#             'isDebugRequest': False,
#         }
#     headers = {'Content-Type': 'application/json'}
#     custom_settings = { 'FEEDS': { f'Output/Zillow_Second_Action_New.json': { 'format': 'json', 'overwrite': True, 'encoding': 'utf-8', }, } }
#
#     count = 1
#     old_properties_zpids = []
#     old_properties = []
#     new_properties = []
#
#     old_json_file_path = "output/Zillow_Second_Action_Old.json"
#     database_csv_file_path = "output/Zillow_Second_Action_Database.csv"
#
#     def start_requests(self):
#         yield scrapy.Request('https://quotes.toscrape.com/', callback=self.pre_parse)
#
#     def pre_parse(self, response):
#         ##  Reading old Database JSON file to save it in Zillow_Second_Action_New.json at the end.
#         if os.path.exists(self.old_json_file_path):
#             with open(self.old_json_file_path, 'r') as f:
#                 self.old_properties = json.load(f)
#             if self.old_properties:                 #####  Saving old_properties.json in new_properties.json
#                 for property in self.old_properties:
#                     yield property
#         else:
#             self.old_properties = []
#
#         ##  Reading Database csv file
#         if os.path.exists(self.database_csv_file_path):
#             with open(self.database_csv_file_path, mode="r", encoding="utf-8") as file:
#                 reader = csv.reader(file)
#                 next(reader)  # Skip the header row
#                 self.old_properties_zpids = [row[0] for row in reader if row]  # Extract ZPIDs from the co
#         else:
#             self.old_properties_zpids = []
#         print('self.old_properties_zpids extracted from Database CSV are : ', self.old_properties_zpids)
#
#         initial = 0
#         inc = 25000
#         # final = 700000
#         final = 200000
#         for i in range(initial, final+1, inc):
#             if i + inc <= final:
#                 start = i
#                 end = i + inc
#                 page_no = 1
#                 prod_no = 0
#                 payload = deepcopy(self.data)
#                 payload['searchQueryState']['pagination']['currentPage'] = page_no
#                 payload['searchQueryState']['filterState']['price']['min'] = start
#                 payload['searchQueryState']['filterState']['price']['max'] = end
#                 yield scrapy.Request(url=self.url, body=json.dumps(payload), method='PUT', callback=self.parse, headers=self.headers,
#                                      meta={'page_no':page_no,'prod_no':prod_no, 'payload':payload})
#
#         #### This one is called at the end from price range || from = 700k --> To= Unlimited (Any Price)
#         page_no = 1
#         prod_no = 0
#         payload = deepcopy(self.data)
#         payload['searchQueryState']['pagination']['currentPage'] = page_no
#         payload['searchQueryState']['filterState']['price']['min'] = 700000
#         yield scrapy.Request(url=self.url, body=json.dumps(payload), method='PUT', callback=self.parse, headers=self.headers,
#                              meta={'page_no':page_no,'prod_no':prod_no, 'payload':payload})
#
#
#     def parse(self, response):
#         prod_no = response.meta['prod_no']
#         data = json.loads(response.text)
#         if data:
#             for house in data.get('cat2').get('searchResults').get('listResults'):
#                 prod_no += 1
#
#                 if house.get('zpid') in self.old_properties_zpids:
#                         print('This property already exists in the database', house.get('zpid'), '||', house.get('addressStreet'))
#
#                 else: # Function to save a new ZPID into the database
#                     print(prod_no, '# This is the new property, lets process this :',house.get('zpid'), '||', house.get('addressStreet'))
#                     # with open(self.database_csv_file_path, mode="a", newline="", encoding="utf-8") as file:
#                     #     writer = csv.writer(file)
#                     #     writer.writerow([house.get('zpid')])
#                     #     print('New property ZPID has been saved inside the Property Database CSV file')
#                     #
#                     item = dict()
#                     item['Zpid'] = house.get('zpid')
#                     item['Street_address'] = house.get('addressStreet')
#                     item['City'] = house.get('addressCity')
#                     item['State'] = house.get('addressState')
#                     item['ZipCode'] = house.get('addressZipcode')
#                     item['Price'] = house.get('price')
#                     item['Beds'] = house.get('beds')
#                     item['Baths'] = house.get('baths')
#                     item['Sqr_feet'] = house.get('area')
#                     item['Home_Status'] = house.get('statusText')
#                     if house.get('hdpData'):
#                         item['Zestimate'] = house.get('hdpData').get('homeInfo').get('zestimate')
#                         item['RentZestimate'] = house.get('hdpData').get('homeInfo').get('rentZestimate')
#                         item['Days_on_zillow'] = house.get('hdpData').get('homeInfo').get('daysOnZillow')
#                         item['Home_Type'] = house.get('hdpData').get('homeInfo').get('homeType')
#
#                     item['Lat_Long'] = house.get('latLong')
#                     # item['Broker_Name'] = house.get('brokerName')
#                     item['Event Description'] = ''
#
#                     item['Listing Photos'] = []
#                     if house.get('carouselPhotos'):
#                         for images in house.get('carouselPhotos'):
#                             item['Listing Photos'].append(images.get('url'))
#                     item['Complete_url'] = house.get('detailUrl')
#                     item['URL'] = house.get('detailUrl')
#                     print(prod_no, ' # Property is :', item)
#                     yield response.follow(url=house.get('detailUrl'), callback=self.parse_detail, headers=self.headers, meta={'item':item})
#
#
#             total_houses = data.get('cat2').get('searchList').get('totalResultCount')
#             print(f"Current Property : {prod_no} || Total Properties are : ", total_houses)
#             if prod_no < total_houses:
#                 page_no = response.meta['page_no'] + 1
#                 payload = response.meta['payload']
#                 payload['searchQueryState']['pagination']['currentPage'] = page_no
#                 yield scrapy.Request(url=self.url, body=json.dumps(payload), method='PUT', callback=self.parse, headers=self.headers,
#                                      meta={'page_no':page_no,'prod_no':prod_no, 'payload':payload})
#
#
#     def parse_detail(self, response):
#         item = response.meta['item']
#         json_data = response.css('#__NEXT_DATA__ ::text').get('').strip()
#         data = json.loads(json_data)
#         if data.get('props').get('pageProps').get('componentProps').get('gdpClientCache'):
#             r_data = json.loads(data.get('props').get('pageProps').get('componentProps').get('gdpClientCache'))
#             zpid = int(item['Zpid'])
#             zpid2 = {"zpid":zpid,"platform":"desktop","isDoubleScroll":True}
#             req_field = {"zpid":zpid,"platform":"DESKTOP_WEB","formType":"OPAQUE","contactFormRenderParameter":zpid2,"skipCFRD":False,"ompPlatform":"web"}
#             a_req_field = 'ForSaleShopperPlatformFullRenderQuery' + str(req_field).replace(' ','').replace('False','false').replace('True','true').replace('\'','\"')
#
#             if r_data.get(a_req_field).get('property'):
#                 item['Structure Area'] = r_data.get(a_req_field).get('property').get('resoFacts', {}).get('buildingArea', '')
#                 item['Price'] = r_data.get(a_req_field).get('property',{}).get('price')
#                 item['Type'] = next((feature.get('factValue') for feature in
#                                      r_data.get(a_req_field, {}).get('property', {}).get('resoFacts', {}).get('atAGlanceFacts', []) if
#                                      feature.get('factLabel') == 'Type'), '')
#                 item["Year Built"] = next((feature.get('factValue') for feature in
#                                            r_data.get(a_req_field, {}).get('property', {}).get('resoFacts', {}).get('atAGlanceFacts', []) if
#                                            feature.get('factLabel') == 'Year Built'), '')
#                 item['Heating'] = next((feature.get('factValue') for feature in
#                                         r_data.get(a_req_field, {}).get('property', {}).get('resoFacts', {}).get('atAGlanceFacts', []) if
#                                         feature.get('factLabel') == 'Heating'), '')
#                 item['Cooling'] = next((feature.get('factValue') for feature in
#                                         r_data.get(a_req_field, {}).get('property', {}).get('resoFacts', {}).get('atAGlanceFacts', []) if
#                                         feature.get('factLabel') == 'Cooling'), '')
#                 item['Parking'] = next((feature.get('factValue') for feature in
#                                         r_data.get(a_req_field, {}).get('property', {}).get('resoFacts', {}).get('atAGlanceFacts', []) if
#                                         feature.get('factLabel') == 'Parking'), '')
#                 item['HOA'] = next((feature.get('factValue') for feature in
#                                     r_data.get(a_req_field, {}).get('property', {}).get('resoFacts', {}).get('atAGlanceFacts', []) if
#                                     feature.get('factLabel') == 'HOA'), '')
#                 item['Lot'] = next((feature.get('factValue') for feature in
#                                     r_data.get(a_req_field, {}).get('property', {}).get('resoFacts', {}).get('atAGlanceFacts', []) if
#                                     feature.get('factLabel') == 'Lot'), '')
#                 item['Price/sqft'] = next((feature.get('factValue') for feature in
#                                            r_data.get(a_req_field, {}).get('property', {}).get('resoFacts', {}).get('atAGlanceFacts', []) if
#                                            feature.get('factLabel') == 'Price/sqft'), '')
#                 item["Offer Review Date"] = next((feature.get('factValue') for feature in
#                                                   r_data.get(a_req_field, {}).get('property', {}).get('resoFacts',{}).get('atAGlanceFacts', []) if
#                                                   feature.get('factLabel') == 'Offer Review Date'), '')
#
#                 # item['Agent_name'] = (r_data.get(a_req_field).get('property').get('attributionInfo').get('agentName'))
#                 # item['Agent_phone'] = (r_data.get(a_req_field).get('property').get('attributionInfo').get('agentPhoneNumber'))
#                 beds, baths = item['Beds'], item['Baths']
#
#                 item['Price History'] = r_data.get(a_req_field).get('property').get('priceHistory')
#                 item['Tax History'] = r_data.get(a_req_field).get('property').get('taxHistory')
#
#                 # item['Nearby Homes'] = r_data.get(a_req_field).get('property').get('nearbyHomes')
#                 item['Nearby Homes'] = []
#                 for nearby_home in r_data.get(a_req_field).get('property').get('nearbyHomes'):
#                     if 'sold' in nearby_home.get('homeStatus', '').lower():
#                         if nearby_home.get('bedrooms') == beds and nearby_home.get('bathrooms') == baths:
#                             item['Nearby Homes'].append(nearby_home)
#
#                 item['Comparable Homes'] = []
#                 if r_data.get(a_req_field).get('property').get('homeValuation', {}):
#                     for comp_home in r_data.get(a_req_field).get('property').get('homeValuation', {}).get('comparables',{}).get('comps',[]):
#                         # print('Comp Home is :', comp_home)
#                         if 'sold' in comp_home.get('property', {}).get('homeStatus', '').lower():
#                             if (comp_home.get('property', {}).get('bedrooms') == beds and comp_home.get('property', {}).get('bathrooms') == baths):
#                                 item['Comparable Homes'].append(comp_home.get('property'))
#
#             if r_data.get(a_req_field).get('property').get('description'):
#                 item['Event Description'] = r_data.get(a_req_field).get('property').get('description').replace('\n','').replace('\t','')
#
#         # Saving the property ZPID in database file
#         with open(self.database_csv_file_path, mode="a", newline="", encoding="utf-8") as file:
#             writer = csv.writer(file)
#             writer.writerow([item['Zpid']])
#             print('New property ZPID has been saved inside the Property Database CSV file')
#
#         yield item
#         self.new_properties.append(item)
#
#
#     def close(self, reason):        # Saving old+new properies in old_properties.json at the end of the scipt.
#         print(' *** Close method is being called at the end of the scipt. Reason =', reason, ' ***')
#         all_properties = self.old_properties + self.new_properties
#
#         with open(self.old_json_file_path, 'w') as json_file:
#             json.dump(all_properties, json_file, indent=4)
#
#         print(f"Saved {len(all_properties)} properties to {self.old_json_file_path}")
#         print(f"Spider closed. {len(self.new_properties)} new properties added.")
#
