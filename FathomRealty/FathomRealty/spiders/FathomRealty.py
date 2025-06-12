import copy
import json
import scrapy

class FathomRealty(scrapy.Spider):
    name = 'FathomRealty'
    url = "https://api.naberly.com/graphql"
    headers = {
        'authority': 'api.naberly.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'content-type': 'application/json',
        'origin': 'https://www.fathomrealty.com',
        'referer': 'https://www.fathomrealty.com/',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    json_data = {
        'operationName': 'searchAgents',
        'variables': {
            'specialtiesFilter': [],
            'languageFilter': [],
            'pageNumber': 1,
            'photosOnly': 'all',
            'pageSize': 24,
        },
        'query': 'query searchAgents($tenantId: String, $search: String, $filter: String, $languageFilter: [String], $specialtiesFilter: [String], $photosOnly: String, $pageNumber: Int, $pageSize: Int) {\n  searchAgents(tenantId: $tenantId, search: $search, filter: $filter, languageFilter: $languageFilter, specialtiesFilter: $specialtiesFilter, photosOnly: $photosOnly, pageNumber: $pageNumber, pageSize: $pageSize) {\n    agents {\n      firstName\n      lastName\n      email\n      id\n      phoneNumber\n      photo\n      languages\n      specialties\n      licenses {\n        id\n        abbreviation\n        license_number\n        state\n        __typename\n      }\n      __typename\n    }\n    cities {\n      value\n      poly\n      bounds\n      coords\n      __typename\n    }\n    zipcodes {\n      value\n      coords\n      __typename\n    }\n    totalCount\n    success\n    __typename\n  }\n}\n',
    }
    custom_settings = {
        'FEED_URI': 'FathomRealty2.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }
    Agent_Count = 1
    next_page = 1
    def start_requests(self):
        payload = copy.deepcopy(self.json_data)
        payload['variables']['pageNumber'] = '1'
        json_str = json.dumps(payload)
        yield scrapy.Request(url=self.url, method="POST", headers=self.headers, body=json_str, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        for agent in data['data']['searchAgents']['agents']:
            item = dict()
            item['First_Name'] = agent.get('firstName','')
            item['Last_Name'] = agent.get('lastName','')
            item['Email'] = agent.get('email','')
            item['ID'] = agent.get('id','')
            item['Phone_No'] = agent.get('phoneNumber','')
            if agent.get('languages',''):
                item['Language'] = agent.get('languages','')
            if agent.get('specialties',''):
                item['Specialties'] = agent.get('specialties','')
            if agent.get('licenses',''):
                item['Licenses'] = agent.get('licenses','')
            item['image_urls'] = ''
            if agent.get('photo',''):
                rel_img_urls = agent.get('photo','')
                item['image_urls'] = self.url_join(rel_img_urls, response)
            self.Agent_Count += 1
            yield item

        self.next_page += 1
        if self.Agent_Count <= data['data']['searchAgents']['totalCount']:
            payload = copy.deepcopy(self.json_data)
            payload['variables']['pageNumber'] = str(self.next_page)
            json_str = json.dumps(payload)
            yield scrapy.Request(url=self.url, method="POST", headers=self.headers, body=json_str, callback=self.parse)

    # item['image_urls'] = self.url_join(rel_img_urls, response)
    def url_join(self, rel_img_urls, response):
        joined_urls = []
        joined_urls.append(response.urljoin(rel_img_urls))
        return joined_urls
