###############         FloridaHealth

import csv
from copy import deepcopy
import scrapy
import datetime

class FloridaHealth(scrapy.Spider):
    name = 'FloridaHealth'
    # url = 'https://mqa-internet.doh.state.fl.us/MQASearchServices/HealthCareProviders/IndexPaged?page=1'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    data = {
        '__RequestVerificationToken': 'JEJ_kmS5_Z0pUFaTiqFhJSmbshA5NnZ7UWxQy9lLRJ8lj1dsgKEFSy-4_JZcHnTgZLGkrr4tycFpQraoLPOj_KsGWSJtiGmm5g84ysK_SKU1',
        'SearchDto.Board': '',
        'SearchDto.Profession': '701',
        'SearchDto.LicenseNumber': '',
        'SearchDto.BusinessName': '',
        'SearchDto.LastName': '',
        'SearchDto.FirstName': '',
        'SearchDto.City': '',
        'SearchDto.County': '16',
        'SearchDto.ZipCode': '',
        'SearchDto.LicenseStatus': 'ALL',
    }
    custom_settings = {
        'FEED_URI': f'output/Florida Health - {datetime.datetime.now().strftime("%d-%m-%Y")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }

    count = 1
    def start_requests(self):
        url = 'https://mqa-internet.doh.state.fl.us/MQASearchServices/HealthCareProviders'
        yield scrapy.Request(url= url, callback=self.parse,  headers=self.headers)


    def parse(self, response):
        token = response.xpath("//*[contains(@name,'__RequestVerificationToken')]/@value").get('').strip()
        payload = deepcopy(self.data)
        payload['__RequestVerificationToken'] = token
        url = 'https://mqa-internet.doh.state.fl.us/MQASearchServices/HealthCareProviders'
        yield scrapy.FormRequest(url=url, formdata=payload, method='POST', callback=self.listing_parse, headers=self.headers,
                                 dont_filter=True,)

    def listing_parse(self, response):
        loop = response.css(".table-condensed tbody tr")
        for index, license in enumerate(loop, start=1):
            item = dict()
            license_url = license.css('a ::attr(href)').get('').strip()
            item['License'] = license.css('a ::text').get('').strip()
            item['Name'] = license.css('td:nth-child(2) ::text').get('').strip()
            item['Profession'] = license.css('td:nth-child(3) ::text').get('').strip()
            item['City'] = license.css('td:nth-child(4) ::text').get('').strip()
            item['License Status'] = license.css('td:nth-child(5) ::text').get('').strip()
            yield response.follow(url=license_url, callback=self.detail_parse, headers=self.headers, dont_filter=True,
                                  meta={'item':item})

        next_page = response.css('.PagedList-skipToNext ::attr(href)').get('').strip()
        if next_page:
            yield response.follow(url= next_page, callback=self.listing_parse,  headers=self.headers, dont_filter=True,)


    def detail_parse(self, response):
        item = response.meta['item']
        # item['Name'] = response.css('.article-header__date ::text').get('').strip()
        # item['Profession'] = response.xpath("//*[contains(@class,'article-header__content rich-text')]").get('').strip()
        # item['License Status'] = response.xpath("//*[contains(text(),'License Number')]/text()").get('').strip().replace('License Number:','')
        item['License'] = response.xpath("//*[contains(text(),'License Number')]/text()").get('').strip().replace('License Number:','')
        item['License Exp Date'] = response.xpath("//*[contains(text(),'License Expiration Date')]/following-sibling::dd[1]/text()").get('').strip()
        item['License Issue Date'] = response.xpath("//*[contains(text(),'Issue Date')]/following-sibling::dd[1]/text()").get('').strip()

        # address = response.xpath("//*[contains(text(),'Address of Record')]/following-sibling::dd[1]/text()").get('').strip()
        # address = ', '.join(e.strip() for e in response.css("dd:nth-child(18) ::text, dd:nth-child(12) ::text").getall())
        address_list = response.css("dt:contains('Address of Record') ~ dd:not(:empty)::text").getall()
        address_string = []
        for address in address_list:
            if address.strip().replace('\n','').replace('\t','').replace('\r',''):
                address_string.append(address.strip().replace('\n','').replace('\t','').replace('\r','').replace('  ',' '))
        address_string = ', '.join(address_string)
        item['Address'] = address_string.strip().replace(' ', ' ').replace('  ',' ').replace(', ,', ',')
        # address = response.xpath("//dt[contains(text(), 'Address of Record')]/following-sibling::dd[normalize-space()]/text()").getall()
        # item['Address'] = address


        controlled_substance = response.xpath("//*[contains(@data-target,'ControlledSubstance')]/parent::dt[1]/following-sibling::dd[1]/span[1]/text()").get('').strip()
        item['Controlled Substance Prescriber'] = controlled_substance
        item['Discipline of File'] = response.xpath("//*[contains(text(),'Discipline on File')]/following-sibling::dd[1]/span[1]/text()").get('').strip()
        public_complaint = response.xpath("//*[contains(@data-target,'PublicComplaint')]/parent::dt[1]/following-sibling::dd[1]/span[1]/text()").get('').strip()
        item['Public Complaint'] = public_complaint

        item['Detail_URL'] = response.url
        yield item
