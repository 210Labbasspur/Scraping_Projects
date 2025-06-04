import re
import csv
import json
import scrapy
import datetime
from copy import deepcopy


class Nihr(scrapy.Spider):
    name = "Nihr"
    url = 'https://bepartofresearch-api.nihr.ac.uk/search/json-params/cd'
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }
    custom_settings = {
        'FEED_URI': f'output/Nihr - {datetime.datetime.now().strftime("%d-%m-%Y")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }
    json_data = {
        'dist': 20,
        'facetDef': {
            'Gender': None,
            'Study Status': [
                'Recruiting',
            ],
            'Updated Within': None,
            'Age Range': None,
            'Health Tag': None,
            'Health Category': None,
        },
        'latLon': '',
        'offset': 0,
        'openurl': 'yes',
        'query': '*',
        'rows': 500,
        'sortBy': None,
        'sortOrder': None,
    }

    def start_requests(self):
        offset = 0
        payload = deepcopy(self.json_data)
        payload['offset'] = offset
        yield scrapy.Request(self.url, callback=self.parse, method='POST', body=json.dumps(payload),
                                 headers=self.headers, meta={'offset': offset})


    def parse(self, response):
        offset = response.meta['offset']
        data = json.loads(response.text)
        if data:
            for result in data.get('data',{}).get('results',[]):
                offset += 1
                id = result.get('id')
                detail_url = f'https://bepartofresearch.nihr.ac.uk/trial-details/trial-detail?trialId={id}&location=&distance='
                print(offset, id)

                item = dict()
                for i in range(7):
                    i += 1
                    item[f'Contact Name{i}'], item[f'First Name{i}'], item[f'Last Name{i}'] = '', '', ''
                item.update({f'Address{i}': '' for i in range(1, 8)})
                item.update({f'Phone{i}': '' for i in range(1, 8)})
                item.update({f'Email{i}': '' for i in range(1, 8)})
                item['Acronym'], item['Condition'], item['Overall Study Start Date'], item['Overall Study End Date'], = '', '', '', ''
                item['Target Number of Participants'], item['Countries of Recruitment'], item['Study Participating Centre'],item['Organisation'] = '', '', '', ''
                item['Funder type'] = ''
                item.update({f'Funder Name{i}': '' for i in range(1, 8)})

                item['Condition'] = ', '.join(e for e in result.get('condition',[]))
                item['Organisation'] = result.get('publicTitle','')
                yield scrapy.Request(detail_url, callback=self.detail_parse, headers=self.headers, meta={'item':item})


        total_results = data.get('data',{}).get('numFound')
        print('Total Results are : ', total_results)
        if offset < total_results:
            payload = deepcopy(self.json_data)
            payload['offset'] = offset
            yield scrapy.Request(self.url, callback=self.parse, method='POST', body=json.dumps(payload),
                                 headers=self.headers, meta={'offset': offset})


    def detail_parse(self, response):
        item = response.meta['item']

        contact_info = None
        funders = None
        for div in response.css('div.collapsable'):
            for sub_div in div.css('::text').getall():
                if 'Contact information' in sub_div.strip():
                    contact_info = div
                if 'Funders/Sponsors' in sub_div.strip():
                    funders = div

        for index, person in enumerate(contact_info.css('p'), start=1):
            if 'More information about' in person.css('::text').get('').strip().replace('\n',' ').replace('\t','').replace('  ',''):
                pass
            else:
                contact_name = person.css('::text').get('').strip().replace('\n',' ').replace('\t','').replace('  ','').replace('- ','')
                item[f'Contact Name{index}'] = contact_name
                parts = contact_name.split()
                titles = ["Dr", "Prof", "A/Prof", "Ms", "Mrs"]
                if parts[0] in titles:
                    parts.pop(0)
                item[f'First Name{index}'] = parts[0]  # The first part is First_Name
                item[f'Last Name{index}'] = parts[-1]  # The last part is Last_Name
                if person.xpath(".//a[contains(@href,'tel:')]"):
                    item[f'Phone{index}'] = person.xpath(".//a[contains(@href,'tel:')]/text()").get('').strip()
                if person.xpath(".//a[contains(@href,'mailto:')]"):
                    item[f'Email{index}'] = person.xpath(".//a[contains(@href,'mailto:')]/text()").get('').strip()

        for index, address in enumerate(response.xpath("//*[contains(@class,'locations-list list-unstyled')]/li"), start=1):
            item[f'Address{index}'] = ', '.join(e.strip().replace('\n',' ') for e in address.css('::text').getall())

        funder_text = funders.css('p::text').get('').strip().replace('\n',' ').replace('\r','').replace('  ','')
        match = re.search(r'and funded by (.*)', funder_text, re.IGNORECASE)
        funders_list = []
        if match:
            funders_str = match.group(1)
            funders_list = [funder.strip().strip(".") for funder in funders_str.split(";") if funder.strip()]
        for index, funder in enumerate(funders_list, start=1):
            if 'Grant Codes' in funder:
                pass
            else:
                item[f'Funder Name{index}'] = funder if funder else ''

        item['Overall Study Start Date'] = response.xpath("//*[contains(@class,'key-dates-from')]/span[1]/text()").get('').strip()
        item['Overall Study End Date'] = response.xpath("//*[contains(@class,'key-dates-from')]/following-sibling::span[1]/span[1]/text()").get('').strip()
        item['Detail_URL'] = response.url

        yield item
