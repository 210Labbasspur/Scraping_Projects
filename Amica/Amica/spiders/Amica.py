import csv
import scrapy
import json
import pgeocode

class Amica(scrapy.Spider):
    name = "Amica"
    request_api = 'https://www.amica.com/bin/amica/repair-locations.js?city={}&state={}&county={}' \
                  '%20County&country=United%20States&zipCode={}&latitude={}&longitude={}&state_long_name='
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '_bcvm_vrid_3225545383923425390=420731720543130988TE4C19659D2854F55B0E764E8AA144811006CC9A9A6E45393C2D9E505A30B0AFA30105B78D82B3E04CAC5E8195D23F580E103B533B8833229A54CECD77E2F8C5B; dtCookie=v_4_srv_13_sn_C79630E06BED2412365339C8BDF1EC06_perc_100000_ol_0_mul_1_app-3A0b997ea3dfb85b77_1; BIGipServerwww.amica.com.app~www.amica.com_pool=!ylySS2KNFathXVj7tX0gvl6V5wENrQExFmFsj3iYpHhyLvHdAv5T+IwE4K9eJKblTuRXguqYKxOiUA==; _bcvm_vid_3225545383923425390=420732559664166360TFD33AF7C85FCFD4F401C64A286EFC1540F236225AD050E569CF72C2E9EE6B4D8BA507DCBE359AAFA5831B1C7921AE8D52DF21F05F41E02BEFF96C1C322D3A753; TS01c37a3d=015e89ced89b299a8fb679ae160f5bc16626a5a36fea0f7127a041b7a078e839b64e2f13e0727b387a587f2956b66b9a7db632a0b3f6fd904ff2dfae0a18812a8a61bdff51f4038237699ea9586dabfdb798555fa8; bc_pv_end=; TSddb03d4b027=0841262a8cab20006905ee080a7a53501f94efbfdd943d163821426be9f33fd0e1ad5b61ef1fa8ad085b4fa03e113000c174bf3d6d3cf0eb21fb02d344404498d46d6f8c1492f663f6d413e8fef9da09dc7c16403f16a57af60c4b12b5cbfcc7; TS01c37a3d=015e89ced858e1077756592d367cc6df8e7aa7dcb608feeffb8aa49180210eaaebf0059650242033e88bfbbb0bbb5dbc70bcae43588e3ca60ab3e222f4b2149aba9b61a97d076dddc038fe8decbd8c0bea0f37481c; TSddb03d4b027=0841262a8cab2000cef4bcad4e3c8d7ca06d8b22567c4ea936ab09d3e8fde4eadce5fc3d3172158f084cb6fcf5113000826e28568afe57c110b03a60cdf3987b35dcf6a0a0460291f6e99dcb46573ffb68216115528e53ed2bd82122a6449aa7',
        'Referer': 'https://www.amica.com/en/claim-center/find-an-auto-repair-shop.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    # custom_settings = {
    #     'FEED_URI': 'Amica_Shops.csv',
    #     'FEED_FORMAT': 'csv',
    #     'FEED_EXPORT_ENCODING': 'utf-8-sig',
    #     }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request_code = self.get_search_code()

    def get_search_code(self):
        with open('US_Zipcodes.csv', 'r', encoding='utf-8-sig') as reader:
            return list(csv.DictReader(reader))

    def start_requests(self):
        nomi = pgeocode.Nominatim('us')
        for check in self.request_code:
            zipcode = check['Representative ZIP Code']
            city = check['Capital City']
            state = check['Abbreviation']
            lat = str(nomi.query_postal_code(zipcode).latitude)
            lon = str(nomi.query_postal_code(zipcode).longitude)
            yield scrapy.Request(url=self.request_api.format(city, state, city, zipcode, lat, lon), headers=self.headers)

    def parse(self, response):
        if response.body:
            data = json.loads(response.body)
            item = dict()
            for Results in data:
                item['Shop_Name'] = Results.get('contact','').get('name','')

                item['Street_Address'] = Results.get('location','').get('address','').get('streetAddress','')
                item['City'] = Results.get('location','').get('address','').get('city','')
                item['State'] = Results.get('location','').get('address','').get('state','')
                item['Zipcode'] = Results.get('location','').get('address','').get('zipCode','')

                item['Landline'] = Results.get('contact','').get('phones','')[0].get('areaCode','') + '-' + \
                    Results.get('contact', '').get('phones', '')[0].get('exchange', '') + '-' + \
                    Results.get('contact', '').get('phones', '')[0].get('number', '')

                if Results.get('contact','').get('phones','')[1]:
                    item['Facsimile'] = Results.get('contact','').get('phones','')[1].get('areaCode','') + '-' + \
                        Results.get('contact', '').get('phones', '')[1].get('exchange', '') + '-' + \
                        Results.get('contact', '').get('phones', '')[1].get('number', '')

                if Results.get('contact','').get('email',''):
                    item['Email'] = Results.get('contact','').get('email','')[0].get('email','')

                item['Latitude'] = Results.get('location', '').get('coordinates', '').get('latitude', '').get('decimal','')
                item['Longitude'] = Results.get('location', '').get('coordinates', '').get('longitude', '').get('decimal','')

                yield item



