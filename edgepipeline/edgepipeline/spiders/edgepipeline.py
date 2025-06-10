import json, csv
import scrapy
from copy import deepcopy
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime


class edgepipeline(scrapy.Spider):
    name = 'edgepipeline'
    url = 'https://www.edgepipeline.com/graphql'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        # 'cookie': '__not____working__',
        # 'cookie': '_ga=GA1.1.1601168493.1721767068; _fw_crm_v=ff0b09a5-3180-4a89-b916-1411111e2226; _session_id=b4c04d537ea4e214d1f0ee33306becad; first_session=%7B%22visits%22%3A45%2C%22start%22%3A1721767068369%2C%22last_visit%22%3A1721893881436%2C%22url%22%3A%22https%3A%2F%2Fwww.edgepipeline.com%2F%22%2C%22path%22%3A%22%2F%22%2C%22referrer%22%3A%22%22%2C%22referrer_info%22%3A%7B%22host%22%3A%22%22%2C%22path%22%3A%22blank%22%2C%22protocol%22%3A%22about%3A%22%2C%22port%22%3A80%2C%22search%22%3A%22%22%2C%22query%22%3A%7B%7D%7D%2C%22search%22%3A%7B%22engine%22%3Anull%2C%22query%22%3Anull%7D%2C%22prev_visit%22%3A1721893871541%2C%22time_since_last_visit%22%3A9895%2C%22version%22%3A0.4%7D; _ga_7KEQW8XRFF=GS1.1.1721893801.8.1.1721893921.0.0.0; _ga_BSQ32KKPQ1=GS1.1.1721893802.8.1.1721893921.0.0.0',
        'origin': 'https://www.edgepipeline.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        # 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'x-requested-with': 'XMLHttpRequest',
        }
    data = {
        'operationName': 'searchableVehicles',
        'variables': {
            'page': 1,
            'perPage': 500,
            'sortBy': [
                {
                    'column': 'LANE',
                    'direction': 'ASC',
                },
                {
                    'column': 'LOT',
                    'direction': 'ASC',
                },
                {
                    'column': 'MAKE',
                    'direction': 'ASC',
                },
                {
                    'column': 'MODEL',
                    'direction': 'ASC',
                },
                {
                    'column': 'YEAR',
                    'direction': 'DESC',
                },
                {
                    'column': 'SALE_DATE',
                    'direction': 'ASC',
                },
            ],
            'filterParams': {
                'auctions': [
                    '88',
                ],
                'buyingOptions': [
                    'FACTORY_PRESALE',
                    'UNCATEGORIZED_PRESALE',
                    'DEALER_PRESALE',
                    'PUBLIC_PRESALE',
                ],
                'year': {
                    'min': 2013,
                    'max': 2021,
                },
                'odometer': {
                    'min': None,
                    'max': 120000,
                },
                'pmr': {
                    'min': None,
                    'max': 15000,
                },
                'vehicleTypes': None,
            },
        },
        'query': 'query searchableVehicles($page: Int, $perPage: Int, $sortBy: [SearchableVehiclesSortInput!], $filterParams: SearchableVehiclesCriteria) {\n  searchableVehicles(\n    page: $page\n    perPage: $perPage\n    sortBy: $sortBy\n    filterParams: $filterParams\n  ) {\n    totalCount\n    vehicles {\n      description\n      hasConditionReport\n      spinPictureCount\n      grade\n      vin\n      exteriorColor\n      mileage\n      mmrValue\n      pmrAverage\n      lights\n      isSold\n      runNumber\n      saleDate\n      auctionShortName\n      city\n      state\n      stockNumber\n      sellerStockNumber\n      checkedInAt\n      buyNowPrice\n      year\n      make\n      model\n      style\n      catalystConsignorName\n      sellerName\n      floorPrice\n      vehicleId\n      canShowAutoCheck\n      canShowCarfaxConnect\n      canShowScanVin\n      isWatched\n      watchList {\n        targetPrice\n        notes\n        __typename\n      }\n      company {\n        id\n        codeName\n        __typename\n      }\n      isSeller\n      buyNowEndAt\n      makeOfferEndAt\n      thumbnailUrl\n      titleStatus\n      edgeSlug\n      distance\n      hasConditionReport\n      eblockListing {\n        eblockId\n        __typename\n      }\n      proxyBidEndsAt\n      proxyBid {\n        amount\n        __typename\n      }\n      simulcastListing {\n        routeName\n        __typename\n      }\n      announcements\n      certifications\n      carproofUrl\n      __typename\n    }\n    __typename\n  }\n}\n',
    }

    custom_settings = {'FEED_URI': f'output/edgepipeline_watch_list_all - ({datetime.now().strftime("%d-%m-%Y")}).csv',
                       'FEED_FORMAT': 'csv',
                       'FEED_EXPORT_ENCODING': 'utf-8-sig', }


    def start_requests(self):
        username, password = '', ''     #   Reading login_credentials
        with open("input/login_credentials.csv", 'r', newline='', encoding='utf-8', errors='ignore') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                username = row['username']
                password = row['password']

        year_from, year_to, odometer_max, price_max, auction_id = None, None, None, None, None     #   Reading filters
        with open("input/filters.csv", 'r', newline='', encoding='utf-8', errors='ignore') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                year_from = float(row['year_from'])
                year_to = float(row['year_to'])
                odometer_max = float(row['odometer_max'])
                price_max = float(row['price_max'])
                auction_id = int(row['auction_id'])

        with open("input/vehicles_redflag_keywords.txt", 'r', encoding='utf-8') as file:    #   Reading vehicles Redflag keywords
            vehicles_redflag_keywords = [line.strip() for line in file]

        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.edgepipeline.com/components/login')
        time.sleep(5)
        email_field = driver.find_element('id', 'username')
        password_field = driver.find_element('id', 'password')
        email_field.send_keys(username)
        password_field.send_keys(password)
        login_button = driver.find_element(By.XPATH, "//input[@value='Sign In']")
        login_button.click()
        time.sleep(2)
        headers = self.headers
        cookiesss = ''
        for cookie in driver.get_cookies():
            cookiesss += f"{cookie.get('name')}={cookie.get('value')}; "
        cookies_dict = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
        print('Extracted Cookies are : ', type(cookiesss), cookiesss)
        headers['cookie'] = cookiesss
        self.headers['cookie'] = cookiesss
        driver.quit()

        vehicle_no = 0
        page_no = 1
        payload = deepcopy(self.data)
        payload['variables']['filterParams']['auctions'][0] = auction_id
        payload['variables']['filterParams']['year']['min'] = year_from
        payload['variables']['filterParams']['year']['max'] = year_to
        payload['variables']['filterParams']['odometer']['max'] = odometer_max
        payload['variables']['filterParams']['pmr']['max'] = price_max
        yield scrapy.Request(url=self.url, body=json.dumps(payload), method='POST', callback=self.parse, headers=self.headers,
                             cookies=cookies_dict, meta={'vehicle_no': vehicle_no, 'page_no': page_no, 'payload': payload,
                            'vehicles_redflag_keywords': vehicles_redflag_keywords, 'cookies_dict':cookies_dict})


    def parse(self, response):
        vehicle_no = response.meta['vehicle_no']
        vehicles_redflag_keywords = response.meta['vehicles_redflag_keywords']
        data = json.loads(response.text)
        total_vehicles = data.get('data', {}).get('searchableVehicles', {}).get('totalCount')

        vehicles_loop = data.get('data', {}).get('searchableVehicles', {}).get('vehicles', [])
        for vehicle in vehicles_loop:
            vehicle_no += 1
            item = dict()
            redflag_keywords = ['WONT START', 'ODOMETER PROBLEM', 'ODOMETER DISCREPANCY', 'STRUCTURAL DAMAGE', 'AIRBAG DEPLOYMENT',
                'TOTAL LOSS', 'FLOOD DAMAGE', 'TITLE BRANDED REBUILT', 'SALVAGE TITLE', 'STARTS INTERMITTENTLY', 'NOT ACTUAL MILEAGE']
            greenflag = True
            for keyword in redflag_keywords:
                if keyword.lower() in vehicle.get('announcements').lower():
                    greenflag = False
                    break

            vehicle_title = vehicle.get('description')
            for keyword in vehicles_redflag_keywords:
                if keyword.lower() in vehicle_title.lower():
                    greenflag = False
                    break

            if greenflag:
                item['Auction Name'] = vehicle.get('auctionShortName')
                item['Picture Count'] = vehicle.get('spinPictureCount')
                item['Run Number'] = vehicle.get('runNumber')
                item['Stock #'] = vehicle.get('stockNumber')
                item['Year'] = vehicle.get('year')
                item['Make'] = vehicle.get('make')
                item['Model'] = vehicle.get('model')
                item['Style'] = vehicle.get('style')
                item['Color'] = vehicle.get('exteriorColor')
                item['Odometer'] = vehicle.get('mileage')
                if vehicle.get('hasConditionReport'):
                    item['CR'] = 'Yes'
                elif not vehicle.get('hasConditionReport'):
                    item['CR'] = 'No'
                item['Grade'] = vehicle.get('grade')
                item['Sale Date'] = vehicle.get('saleDate')
                if '-' in vehicle.get('runNumber'):
                    lane, part2 = vehicle.get('runNumber').split('-')
                    item['Lane'] = lane.upper()
                item['VIN'] = vehicle.get('vin')
                item['Sold Amount'] = ''
                item['Watch Notes'] = ''

                codename = vehicle.get('company').get('codeName')
                stocknumber = vehicle.get('stockNumber')
                vehicleid = vehicle.get('vehicleId')
                carfax_url = (f'https://www.edgepipeline.com/components/carfax_connect/redirect_to_report_url?redirect_url=https%3A%2F%2Fwww.edgepipeline.com%2Fcomponents%2Fvehicle%2Fdetail'
                              f'%2F{codename}%2F{stocknumber}&amp;code_name={codename}&amp;vehicle_id={vehicleid}')
                print(vehicle_no, "CARFAX : ", carfax_url)
                yield scrapy.Request(url=carfax_url, callback=self.carfax, headers=self.headers, meta={'item': item})


        # #########      Pagination
        print('\n Total Vehicles : ', total_vehicles, ' ||||||   and Scraped Vehicles : ', vehicle_no)
        if vehicle_no < total_vehicles:
            cookies_dict = response.meta['cookies_dict']
            page_no = response.meta['page_no'] + 1
            payload = response.meta['payload']
            payload['variables']['page'] = page_no
            yield scrapy.Request(url=self.url, body=json.dumps(payload), method='POST', callback=self.parse, headers=self.headers,
                                 cookies=cookies_dict, meta={'vehicle_no': vehicle_no, 'page_no': page_no, 'payload': payload,
                                       'vehicles_redflag_keywords': vehicles_redflag_keywords, 'cookies_dict': cookies_dict})

    def carfax(self, response):
        item = response.meta['item']

        greenflag = True

        ###     Accidents
        no_of_accidents = 0
        for accident in response.css('.accident-damage-initial-group'):
            for event in accident.css('.accident-damage-record'):
                no_of_accidents += 1
                type_of_accidents = event.css('.accident-damage-record-comments .comments-group-outer-line ::text').get('').strip()
                if 'SEVERE' in type_of_accidents.upper() or 'TOTAL LOSS' in type_of_accidents.upper():
                    greenflag = False
        if no_of_accidents > 2:
            greenflag = False

        ###     Recall
        if response.xpath("//strong[contains(text(),'Manufacturer Safety recall issued')]/text()").get('').strip():
            recall_remedy = response.xpath("//li[contains(text(),'Remedy Available')]/text()").get('').strip()
            if 'remedy not yet available' in response.text.lower():
                greenflag = False
                recall_remedy = response.xpath("//li[contains(text(),'Remedy Not Yet Available')]/text()").get('').strip()

        ###     odometer-check
        odometer_check = response.xpath("//*[contains(@id,'odometer-check')]")
        for oc in odometer_check.css('::text').getall():
            if 'discrepancy' in oc.lower():
                greenflag = False
                break

        if greenflag:
            yield item
