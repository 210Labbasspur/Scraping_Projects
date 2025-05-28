# -*- coding: utf-8 -*-
import csv, unicodedata
import re
import scrapy
import datetime
from urllib.parse import quote_plus, urljoin
from scrapy import Request
# from scrapy.utils.response import open_in_browser

class GoogleSpider(scrapy.Spider):
    # name = 'google_business_city_country'
    name = 'google_business'

    new_listings_url_t = 'https://www.google.com/localservices/prolist?ssta=1&src=2&q={q}&lci={page}'
    new_details_url_t = 'https://www.google.com/localservices/prolist?g2lbs=AP8S6ENgyDKzVDV4oBkqNJyZonhEwT_VJ6_XyhCY8jgI2NcumLHJ7mfebZa8Yvjyr_RwoUDwlSwZt5ofLQk3D079b7a0tYFMAl-OvnNjzh2HzyjZNDGO0bloXZTJ8ttkCFt5rwXuqt_u&hl=en-PK&gl=pk&ssta=1&oq={q}&src=2&sa=X&scp=CgASABoAKgA%3D&q={q}&ved=2ahUKEwji7NSKjZiAAxUfTEECHdJnDF8QjdcJegQIABAF&slp=MgBAAVIECAIgAIgBAJoBBgoCFxkQAA%3D%3D&spp={id}'
   #test_checking_is  = 'https://www.google.com/localservices/prolist?ssta=1&src=2&q=list%20of%20home%20inspection%20companies%20minnesota&ved=2ahUKEwimyP_W6veDAxUCAToCHVoAC_AQjdcJegQIABAF&slp=MgBAAVIECAIgAIgBAA%3D%3D&scp=ChNnY2lkOmhvbWVfaW5zcGVjdG9yEgAaACoOSG9tZSBpbnNwZWN0b3I6AkAB&lci=60'
    listings_url_t = 'https://www.google.com/search?sxsrf=ACYBGNS1OuAlrwXrWvHCe01W6jx80oL9jA:1581870852554&q={q}&npsic=0&rflfq=1&rlha=0&rllag=-33868535,151194512,2415&tbm=lcl&ved=2ahUKEwiN1fyRwNbnAhUHVBUIHdOxBdIQjGp6BAgLEFk'
    RETRY_HTTP_CODES = [400, 403, 407, 408, 429, 500, 502, 503, 504, 405, 503, 520]
    handle_httpstatus_list = [400, 401, 402, 403, 404, 405, 406, 407, 409, 500, 501, 502, 503, 504,
                              505, 506, 507, 509]
    scraped_bussinesses = list()
    headers = {
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        'content-type': "application/json",
        'accept-language': "en-US,en;q=0.9",
        'X-Crawlera-Region': 'SE'
    }
    keywords = [x for x in csv.DictReader(open('input/keywords.csv', encoding='Latin-1'))]
    locations = [x for x in csv.DictReader(open('input/locations.csv', encoding='Latin-1'))]
    search_keyword = '{keyword}'
    base_url = 'https://www.google.ca/'
    start_urls = ["https://quotes.toscrape.com/"]
    business_urls = []
    custom_settings = {
        ########################################################################################################
        'FEED_URI': f'output/Google_Business - {datetime.datetime.now().strftime("%d-%m-%Y")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
        ########################################################################################################
        # 'FEED_URI': f'output/Google_Business - {datetime.datetime.now().strftime("%d-%m-%Y")}.xlsx',
        # 'FEED_FORMAT': 'xlsx',
        # 'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
        # 'FEED_EXPORT_ENCODING': 'utf-8',
        ########################################################################################################
    }

    def parse(self, response, *args):
        for keyword in self.keywords:
            for location in self.locations:
                # search_keyword = (f"{keyword.get('keywords', '')} in {location.get('postcode', '')}, {location.get('city', '')}, "
                #                   f"{location.get('country', '')}")
                search_keyword = (f"{keyword.get('keywords', '')} in {location.get('postcode', '')}, {location.get('country', '')}")
                query = self.search_keyword.format(keyword=search_keyword)
                url = self.new_listings_url_t.format(q=quote_plus(query), page=0)
                meta = {'keyword': search_keyword, 'start': 0, 'location': f"{location.get('postcode', '')}",
                        'query': query}

                yield Request(url=url, callback=self.parse_new_data, meta=meta)

    def parse_new_data(self, response):
        if response.css('div[jsname="AECrIc"]'):
            for listing_selector in response.css('div[jscontroller="xkZ6Lb"]'):
                listing_id = listing_selector.css('::attr(data-profile-url-path)').get('').replace(
                    '/localservices/profile?spp=', '')
                in_type = listing_selector.css('span.hGz87c::text').get('').strip()
                response.meta['type'] = in_type
                details_url = self.new_details_url_t.format(
                    q=quote_plus(response.meta['keyword']),
                    id=listing_id)
                Name = listing_selector.css('.xYjf2e::text').get('').strip()
                Address = listing_selector.css('.hGz87c span::text').getall()[-1] if listing_selector.css(
                    '.hGz87c span::text').getall() else ''
                if f"{Name} {Address}" not in self.business_urls:
                    self.business_urls.append(f"{Name} {Address}")
                    yield scrapy.Request(url=details_url, callback=self.parse_new_details,
                                         meta=response.meta)

            keyword = response.meta['keyword']
            location = response.meta['location']
            start = response.meta['start'] + 20
            query = response.meta['query']
            url = self.new_listings_url_t.format(q=quote_plus(query), page=start)
            meta = {'keyword': keyword, 'start': start, 'location': location, 'query': query}
            if response.css('div[jscontroller="xkZ6Lb"]'):
                yield Request(url=url, callback=self.parse_new_data, meta=meta)

    def parse_new_details(self, response):
        item = dict()
        item['Bussiness_Name'] = response.css('div.tZPcob::text').get('').strip()
        item['Address'] = response.css('div.fccl3c span::text').get('').strip()
        item['ZipCode'] = response.meta['location']
        item['Bussiness_Contact'] = response.css('div.eigqqc::text').get('').strip()
        item['Email'] = ''
        item['Website'] = response.css('a.iPF7ob::attr(href)').get('').strip().replace('/url?sa=i&source=web&rct=j&url=','')
        item['Bussiness_Website'] = response.css('a.iPF7ob::attr(href)').get('').strip().replace('/url?sa=i&source=web&rct=j&url=','')

        item['Type_of_Business'] = response.meta['keyword'].split('in')[0]
        # item['search query'] = response.meta['query']
        # item['City'] = response.meta['location']
        # item['Type'] = response.meta['keyword']
        item['Keywords'] = response.meta['keyword']
        # item['Location'] = response.meta['location']
        # item['ZipCode'] = response.meta['location']

        # item['Menu_Link'] = ''
        # item['Logo/Image URL'] = ''
        # item['Base Price'] = ''
        # item['Delivery Fee'] = ''
        # item['Latitude'] = ''
        # item['Longitude'] = ''

        item['Bussiness_Name'] = response.css('div.tZPcob::text').get('').strip()
        item['Address'] = response.css('div.fccl3c span::text').get('').strip()
        item['ZipCode'] = response.meta['location']
        item['Bussiness_Contact'] = response.css('div.eigqqc::text').get('').strip()
        item['Business_Region'] = response.meta['location']     ##  This saves the city from the input location file
        item['Contact_No'] = response.css('div.eigqqc::text').get('').strip().replace(' ', '').replace('-','').replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

        item['Business_URL'] = response.url
        item['Bussiness_Duration'] = response.css('div.FjZRNe::text').get('').strip()
        item['Bussiness_Website'] = response.css('a.iPF7ob::attr(href)').get('').strip().replace('/url?sa=i&source=web&rct=j&url=','')
        item['Bussiness_Service'] = response.xpath('//*[contains(text(), "Services:")]/following::text()[1]').get('').strip()
        item['Bussiness_Serving_Area'] = ', '.join(response.css('div.oR9cEb ::text').getall())
        item['Review_Count'] = response.css('.pNFZHb div.leIgTe::text').get('').strip().replace('(', '').replace(')', '')
        item['Rating'] = response.css('.pNFZHb div.rGaJuf::text').get('').strip()
        item['Description'] = response.css('h3.NwfE3d+div::attr(data-long-text)').get('').strip()
        item['Review_Type'] = response.meta['type']
        item['Google_Map_Link'] = response.css('a[aria-label="Directions"]::attr(href)').get('').strip()


        sttr = 'script:contains("hash: {}")'.format("'4'")
        sttr = 'script:contains("nonce: M37zc4jqsavLs-9DU4C9Eg")'.format("'4'")
        script = response.css(sttr).get('{}')
        days = ['Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday']
        opening_time = []
        for day in days:
            match = re.search(f'"{day}",(.*?)false', script)
            if match:
                hours = match.group(1).split('[["')[-1].split('"')[0]
                opening_time.append(f'{day}: {hours}')
        item['Opening_Hours'] = ' / '.join(opening_time)

        yield item

    def remove_accents(self, string):
        normalized = unicodedata.normalize('NFD', string)
        return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')




'''
https://www.google.com/localservices/prolist?g2lbs=AP8S6ENgyDKzVDV4oBkqNJyZonhEwT_VJ6_XyhCY8jgI2NcumLHJ7mfebZa8Yvjyr_RwoUDwlSwZt5ofLQk3D079b7a0tYFMAl-OvnNjzh2HzyjZNDGO0bloXZTJ8ttkCFt5rwXuqt_u&hl=en-PK&gl=pk&ssta=1&oq=Thai%20Restaurants%20in%20Santa%20Barbara%2C%20usa&src=2&sa=X&q=list%20of%20home%20inspection%20companies%20minnesota&ved=2ahUKEwiwg8yO6_eDAxU3MDoCHXexB6UQjdcJegQIABAF&spp=CgwvZy8xaGMxc250eTE66AJXaXNRQUJBQkVBSWlJMmh2YldVZ2FXNXpjR1ZqZEdsdmJpQmpiMjF3WVc1cFpYTWdiV2x1Ym1WemIzUmhtZ0VqUTJoYVJGTlZhRTVOUnpsdVV6QldTbEV3Um01VFZWRXlUVmhTVEZwVldsSkZRVVdxQVlzQkNna3ZiUzh3TVd3d2JYY0tDUzl0THpBeVpERjZPQW9JTDIwdk1EUjVhMmNRQVNvZElobG9iMjFsSUdsdWMzQmxZM1JwYjI0Z1kyOXRjR0Z1YVdWektBQXlIeEFCSWhzdnhPQ3ZFdHhDcHlxWmFSSDhOTUZ2ZGRLUTVRbDBfcWFkWldVeUp4QUNJaU5vYjIxbElHbHVjM0JsWTNScGIyNGdZMjl0Y0dGdWFXVnpJRzFwYm01bGMyOTBZY0lCSndoLUlpTkRhRnBFVTFWb1RrMUhPVzVUTUZaS1VUQkdibE5WVVRKTldGSk1XbFZhVWtWQlJRPT0%3D&slp=MgBAAVIECAIgAGgBiAEAmgEGCgIXGRAA&scp=ChNnY2lkOmhvbWVfaW5zcGVjdG9yEiAiCG1hcCBhcmVhKhQNIAKyGhW5oEPIHadb4holp7mqyBoAKhJCdWlsZGluZyBpbnNwZWN0b3I6AkAB

https://www.google.com/localservices/prolist?g2lbs=AP8S6ENgyDKzVDV4oBkqNJyZonhEwT_VJ6_XyhCY8jgI2NcumLHJ7mfebZa8Yvjyr_RwoUDwlSwZt5ofLQk3D079b7a0tYFMAl-OvnNjzh2HzyjZNDGO0bloXZTJ8ttkCFt5rwXuqt_u&hl=en-PK&gl=pk&ssta=1&oq=INFOTEC%20Home%20Inspection&src=2&sa=X&q=INFOTEC%20Home%20Inspection&ved=0CAUQjdcJahgKEwjgufm88veDAxUAAAAAHQAAAAAQzgE&scp=ChNnY2lkOmhvbWVfaW5zcGVjdG9yEgAaACoSQnVpbGRpbmcgaW5zcGVjdG9y&slp=MgBAAVIECAIgAIgBAJoBBgoCFxkQAA%3D%3D&spp=Cg0vZy8xMXFtbTkzc3Z6OpgCV2g4UUFCQUJFQUlpRjJsdVptOTBaV01nYUc5dFpTQnBibk53WldOMGFXOXVtZ0VqUTJoYVJGTlZhRTVOUnpsdVV6QldTbEV3Um01VFZWSnZaRlJhY1ZGVlpETkZRVVdxQVYwUUFTb2JJaGRwYm1admRHVmpJR2h2YldVZ2FXNXpjR1ZqZEdsdmJpZ0FNaDhRQVNJYktBNXpvcUozV1ZxVWJzT2c5YVA2R2FFUlZSaFpaZVdpV3h4Vk1oc1FBaUlYYVc1bWIzUmxZeUJvYjIxbElHbHVjM0JsWTNScGIyN0NBU2NJZmlJalEyaGFSRk5WYUU1TlJ6bHVVekJXU2xFd1JtNVRWVkp2WkZSYWNWRlZaRE5GUVVVPQ%3D%3D


'https://www.google.com/localservices/prolist?g2lbs=AP8S6ENgyDKzVDV4oBkqNJyZonhEwT_VJ6_XyhCY8jgI2NcumLHJ7mfebZa8Yvjyr_RwoUDwlSwZt5ofLQk3D079b7a0tYFMAl-OvnNjzh2HzyjZNDGO0bloXZTJ8ttkCFt5rwXuqt_u&hl=en-PK&gl=pk&ssta=1&oq=list%20of%20home%20inspection%20companies%20minnesota&src=2&sa=X&scp=CgASABoAKgA%3D&q=list%20of%20home%20inspection%20companies%20minnesota&ved=2ahUKEwji7NSKjZiAAxUfTEECHdJnDF8QjdcJegQIABAF&slp=MgBAAVIECAIgAIgBAJoBBgoCFxkQAA%3D%3D&spp={id}'

https://www.google.com/localservices/prolist?g2lbs=AP8S6ENgyDKzVDV4oBkqNJyZonhEwT_VJ6_XyhCY8jgI2NcumLHJ7mfebZa8Yvjyr_RwoUDwlSwZt5ofLQk3D079b7a0tYFMAl-OvnNjzh2HzyjZNDGO0bloXZTJ8ttkCFt5rwXuqt_u&hl=en-PK&gl=pk&ssta=1&oq=list%20of%20home%20inspection%20companies%20minnesota&src=2&sa=X&scp=CgASABoAKgA%3D&q=list%20of%20home%20inspection%20companies%20minnesota&ved=2ahUKEwji7NSKjZiAAxUfTEECHdJnDF8QjdcJegQIABAF&slp=MgBAAVIECAIgAIgBAJoBBgoCFxkQAA%3D%3D&spp=CgsvZy8xdHRwOXoxeDroAldpc1FBQkFCRUFJaUkyaHZiV1VnYVc1emNHVmpkR2x2YmlCamIyMXdZVzVwWlhNZ2JXbHVibVZ6YjNSaG1nRWpRMmhhUkZOVmFFNU5Semx1VXpCV1NsRXdSbTVUVlZKcVRraGFNVm93ZEVKRlFVV3FBWXNCQ2drdmJTOHdNV3d3YlhjS0NTOXRMekF5WkRGNk9Bb0lMMjB2TURSNWEyY1FBU29kSWhsb2IyMWxJR2x1YzNCbFkzUnBiMjRnWTI5dGNHRnVhV1Z6S0FBeUh4QUJJaHN2eE9DdkV0eENweXFaYVJIOE5NRnZkZEtRNVFsMF9xYWRaV1V5SnhBQ0lpTm9iMjFsSUdsdWMzQmxZM1JwYjI0Z1kyOXRjR0Z1YVdWeklHMXBibTVsYzI5MFljSUJKd2gtSWlORGFGcEVVMVZvVGsxSE9XNVRNRlpLVVRCR2JsTlZVbXBPU0ZveFdqQjBRa1ZCUlE9PQ%3D%3D
https://www.google.com/localservices/prolist?g2lbs=AP8S6ENgyDKzVDV4oBkqNJyZonhEwT_VJ6_XyhCY8jgI2NcumLHJ7mfebZa8Yvjyr_RwoUDwlSwZt5ofLQk3D079b7a0tYFMAl-OvnNjzh2HzyjZNDGO0bloXZTJ8ttkCFt5rwXuqt_u&hl=en-PK&gl=pk&ssta=1&oq=&src=2&sa=X&scp=CgASABoAKgA%3D&q=&ved=2ahUKEwji7NSKjZiAAxUfTEECHdJnDF8QjdcJegQIABAF&slp=MgBAAVIECAIgAIgBAJoBBgoCFxkQAA%3D%3D&spp=CgsvZy8xdHRwOXoxeDroAldpc1FBQkFCRUFJaUkyaHZiV1VnYVc1emNHVmpkR2x2YmlCamIyMXdZVzVwWlhNZ2JXbHVibVZ6YjNSaG1nRWpRMmhhUkZOVmFFNU5Semx1VXpCV1NsRXdSbTVUVlZKcVRraGFNVm93ZEVKRlFVV3FBWXNCQ2drdmJTOHdNV3d3YlhjS0NTOXRMekF5WkRGNk9Bb0lMMjB2TURSNWEyY1FBU29kSWhsb2IyMWxJR2x1YzNCbFkzUnBiMjRnWTI5dGNHRnVhV1Z6S0FBeUh4QUJJaHN2eE9DdkV0eENweXFaYVJIOE5NRnZkZEtRNVFsMF9xYWRaV1V5SnhBQ0lpTm9iMjFsSUdsdWMzQmxZM1JwYjI0Z1kyOXRjR0Z1YVdWeklHMXBibTVsYzI5MFljSUJKd2gtSWlORGFGcEVVMVZvVGsxSE9XNVRNRlpLVVRCR2JsTlZVbXBPU0ZveFdqQjBRa1ZCUlE9PQ%3D%3D
https://www.google.com/localservices/prolist?g2lbs=AP8S6ENgyDKzVDV4oBkqNJyZonhEwT_VJ6_XyhCY8jgI2NcumLHJ7mfebZa8Yvjyr_RwoUDwlSwZt5ofLQk3D079b7a0tYFMAl-OvnNjzh2HzyjZNDGO0bloXZTJ8ttkCFt5rwXuqt_u&hl=en-PK&gl=pk&ssta=1&oq=list%20of%20home%20inspection%20companies%20minnesota&src=2&sa=X&scp=CgASABoAKgA%3D&q=&ved=2ahUKEwji7NSKjZiAAxUfTEECHdJnDF8QjdcJegQIABAF&slp=MgBAAVIECAIgAIgBAJoBBgoCFxkQAA%3D%3D&spp=CgsvZy8xdHRwOXoxeDroAldpc1FBQkFCRUFJaUkyaHZiV1VnYVc1emNHVmpkR2x2YmlCamIyMXdZVzVwWlhNZ2JXbHVibVZ6YjNSaG1nRWpRMmhhUkZOVmFFNU5Semx1VXpCV1NsRXdSbTVUVlZKcVRraGFNVm93ZEVKRlFVV3FBWXNCQ2drdmJTOHdNV3d3YlhjS0NTOXRMekF5WkRGNk9Bb0lMMjB2TURSNWEyY1FBU29kSWhsb2IyMWxJR2x1YzNCbFkzUnBiMjRnWTI5dGNHRnVhV1Z6S0FBeUh4QUJJaHN2eE9DdkV0eENweXFaYVJIOE5NRnZkZEtRNVFsMF9xYWRaV1V5SnhBQ0lpTm9iMjFsSUdsdWMzQmxZM1JwYjI0Z1kyOXRjR0Z1YVdWeklHMXBibTVsYzI5MFljSUJKd2gtSWlORGFGcEVVMVZvVGsxSE9XNVRNRlpLVVRCR2JsTlZVbXBPU0ZveFdqQjBRa1ZCUlE9PQ%3D%3D

https://www.google.com/localservices/prolist?ssta=1&src=2&q=list%20of%20home%20inspection%20companies%20minnesota&ved=2ahUKEwimyP_W6veDAxUCAToCHVoAC_AQjdcJegQIABAF&slp=MgBAAVIECAIgAIgBAA%3D%3D&scp=ChNnY2lkOmhvbWVfaW5zcGVjdG9yEgAaACoOSG9tZSBpbnNwZWN0b3I6AkAB&lci=60


'''
