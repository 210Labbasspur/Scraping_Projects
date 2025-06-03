import csv
import scrapy
import json
# import pgeocode

class AmeriGas(scrapy.Spider):
    name = "AmeriGas"
    request_api = 'https://www.amerigas.com/api/search?query=%7BsearchResults(cityStateZipLocation:%22{}%22,' \
                  'distance:20,pageIndex:0,pageSize:500)%7BtotalCount,totalPageCount,latitude,longitude,city,state,' \
                  'cynchServiceable,propaneTaxiServiceable,locations%7Bid,distance,locationType,locationTypeName,name,' \
                  'address1,address2,city,state,zip,officeUrl,latitude,longitude,phone,twentyFourSeven,priority,allowWalkins,' \
                  'businessHours%7BdayOfWeek,dayOfWeekName,open,close,closed%7D%7D%7D%7D'
    headers = {
      'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
      'Accept': 'application/json, text/plain, */*',
      # 'Referer': 'https://www.amerigas.com/locations/find-propane?q=36104',
      'sec-ch-ua-mobile': '?0',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
      'sec-ch-ua-platform': '"Windows"'
    }
    custom_settings = {
        'FEED_URI': 'AmeriGas.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
        }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request_code = self.get_search_code()

    def get_search_code(self):
        with open('US_Zipcodes.csv', 'r', encoding='utf-8-sig') as reader:
            return list(csv.DictReader(reader))

    def start_requests(self):
        # yield scrapy.Request(url=self.request_api, headers=self.headers)
        # nomi = pgeocode.Nominatim('us')
        for check in self.request_code:
            zipcode = check['Representative ZIP Code']
            yield scrapy.Request(url=self.request_api.format(zipcode), headers=self.headers)

    def parse(self, response):
        if response.body:
            data = json.loads(response.body)
            item = dict()
            for Results in data.get('data', '').get('searchResults', '').get('locations', ''):
                item['Name'] = Results.get('name', '')
                item['Street_Address'] = Results.get('address1','')
                item['City'] = Results.get('city','')
                item['State'] = Results.get('state','')
                item['Zip-Code'] = Results.get('zip','')
                item['Latitude'] = Results.get('latitude','')
                item['Longitude'] = Results.get('longitude','')
                item['Phone#'] = Results.get('phone','')
                item['Loc Type'] = Results.get('locationTypeName', '')
                item['24/7 Self-Service'] = Results.get('twentyFourSeven','')
                yield item

