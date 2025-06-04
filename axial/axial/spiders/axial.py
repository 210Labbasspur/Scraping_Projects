############            axial
import json
import scrapy
from datetime import datetime
from copy import deepcopy


class axial(scrapy.Spider):
    name = 'axial'
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'no-cache',
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
    custom_settings = {
        'FEED_URI': f'output/Axial - {datetime.now().strftime("%d-%m-%Y")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }

    count = 1
    def start_requests(self):
        # url = 'https://www.axial.net/forum/companies/united-states-family-offices/1/'
        ###############################################################################
        # url = 'https://www.axial.net/forum/companies/private-equity-firms/'
        url = 'https://www.axial.net/forum/companies/united-states-private-equity-firms/1/'
        yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)
        url = 'https://www.axial.net/forum/companies/canada-private-equity-firms/'
        yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        for category in response.css('.teaser1-buttons a'):
            category_url = category.css('::attr(href)').get('').strip()
            company_slug = category_url.split('/')[-1]
            company_url = f'https://api.axial.net/account/accounts/?slug={company_slug}'
            print(self.count, company_slug, category_url)
            self.count += 1
            yield scrapy.Request(url=company_url, callback=self.detail_parse, headers=self.headers)

        next_page = response.css('a.icon-arrow-right ::attr(href)').get('').strip()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse, headers=self.headers)


    def detail_parse(self, response):
        data = json.loads(response.text)

        if data.get('data',[]):
            info = data.get('data',[])[0]
            item = dict()
            item['Company Name'] = info.get('name')
            id = info.get('id')

            item['Street Address 1'] = []
            item['Street Address 2'] = ''
            item['City'] = ''
            item['State'] = ''
            item['Zip Code'] = ''
            item['Country'] = ''
            item['Industries'] = ''
            for e in range(4):
                item[f'Team Member {e + 1}'] = ''

            primary_office =  info.get('primary_office')
            if primary_office:
                # item['Street Address 1'] = ', '.join(e for e in primary_office.get('street_address',[]))
                for e in primary_office.get('street_address'):
                    if e:
                        item['Street Address 1'].append(e)
                item['Street Address 1'] = ', '.join(e for e in item['Street Address 1'])
                item['City'] = primary_office.get('city')
                item['State'] = primary_office.get('region')
                item['Zip Code'] = primary_office.get('postal_code')
                item['Country'] = primary_office.get('country')

            if id:
                team = f'https://api.axial.net/account/accounts/{id}/members?is_active=false'
                offices = f'https://api.axial.net/account/accounts/{id}/offices'
                industries = f'https://api.axial.net/account/accounts/{id}/industries'

                yield scrapy.Request(url=team, callback=self.team_parse, headers=self.headers,
                                     meta={'item':item, 'offices':offices, 'industries':industries})
        else:
            yield {}


    def team_parse(self, response):
        data = json.loads(response.text)
        item = response.meta['item']
        offices = response.meta['offices']
        industries = response.meta['industries']
        if data.get('data'):
            for index, info in enumerate(data.get('data'), start=1):
                item[f'Team Member {index}'] = info.get('first_name') + ' ' + info.get('last_name')

        if offices:
            yield scrapy.Request(url=offices, callback=self.offices_parse, headers=self.headers,
                                 meta={'item': item, 'industries': industries})


    def offices_parse(self, response):
        data = json.loads(response.text)
        item = response.meta['item']
        industries = response.meta['industries']
        # item['Street Address 2'] = []
        # if data.get('data'):
        #     for info in data.get('data'):
        #         if info.get('type_code') == "SAT":
        #             for e in info.get('street_address'):
        #                 if e:
        #                     item['Street Address 2'].append(e)
        #             item['Street Address 2'] = ', '.join(e for e in item['Street Address 2'])
        item['Street Address 2'] = []
        if data.get('data'):
            for info in data.get('data'):
                if info.get('type_code') == "SAT":
                    for e in info.get('street_address'):
                        if e:
                            item['Street Address 2'].append(e)  # Append while still a list
            item['Street Address 2'] = ', '.join(item['Street Address 2'])  # Convert to string after loop

        if industries:
            yield scrapy.Request(url=industries, callback=self.industries_parse, headers=self.headers, meta={'item': item})


    def industries_parse(self, response):
        data = json.loads(response.text)
        item = response.meta['item']
        item['Industries'] = []
        industries = []
        if data.get('data'):
            for e in data.get('data', {}):
                if e:
                    industries.append(e.get('name',''))
            # item['Industries'] = ', '.join(e for e in data.get('data',[]))
        item['Industries'] = ', '.join(e for e in industries)
        # if industries:
        #     for e in industries:
        #         if e:
        #             # item['Industries'] = ', '.join(e.strip() for e in industries)
        #             item['Industries'] = ', '.join(e.strip())

        yield item
