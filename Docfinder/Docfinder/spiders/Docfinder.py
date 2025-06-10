import csv
import json
import scrapy
import datetime


class Docfinder(scrapy.Spider):
    name = 'Docfinder'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    custom_settings = {
        'FEED_URI': f'output/Docfinder - {datetime.datetime.now().strftime("%d-%m-%Y")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }

    count = 1
    def start_requests(self):
        keywords = []
        postcodes = []
        with open("input/Docfinder_input_Keyword.csv", 'r', newline='', encoding='utf-8', errors='ignore') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                keyword = row['Keyword']
                if keyword:
                    keywords.append(keyword)
        with open("input/Docfinder_input_Postcode.csv", 'r', newline='', encoding='utf-8', errors='ignore') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                postcode = row['Postcode']
                if postcode:
                    postcodes.append(postcode)
        count = 1
        for keyword in keywords:
            for postcode in postcodes:
                detail_url = f'https://www.docfinder.at/suche?what={keyword}&where={postcode}&userSubmitted=1&originalWhat={keyword}'
                print(count, keyword, postcode)
                count += 1
                yield scrapy.Request(detail_url, callback=self.parse, headers=self.headers)


    def parse(self, response):
        loop = response.css('.search-result')
        for doc in loop:
            doc_url = doc.xpath(".//*[contains(@class,'top')]/parent::a[1]/@href").get('').strip()
            print(self.count, doc_url)
            self.count += 1
            yield response.follow(doc_url, callback=self.detail_parse, headers=self.headers)

        next_page = response.css('a.icon-right ::attr(href)').get('').strip()
        if next_page:
            yield response.follow(next_page, callback=self.parse, headers=self.headers)


    def detail_parse(self, response):
        item = dict()
        json_text = response.xpath("//*[contains(@type,'application/ld+json')]/text()").get('').strip()
        data = json.loads(json_text)
        if data:
            item['Name'] = data.get('mainEntity',{}).get('name','')

            street_address = data.get('mainEntity',{}).get('address', {}).get('streetAddress','')
            postal_code = data.get('mainEntity',{}).get('address', {}).get('postalCode','')
            address_locality = data.get('mainEntity',{}).get('address', {}).get('addressLocality','')
            item['Street'] = street_address
            item['PostCode'] = postal_code
            item['City'] = address_locality
            item['Location'] = f'{street_address}, {postal_code} {address_locality}'

            profession_payment = response.css('.professions span ::text').getall()
            item['Profession'] = profession_payment[0].strip()
            item['Type of Payment'] = profession_payment[1].strip() if len(profession_payment) > 1 else ''

            item['E-mail'] = data.get('mainEntity',{}).get('email','')
            item['Phone No'] = data.get('mainEntity',{}).get('telephone','')
            item['Fax'] = data.get('mainEntity',{}).get('faxNumber','')
            item['Website'] = data.get('mainEntity',{}).get('url','')

            opening_hours = []
            for opening_hour in data.get('mainEntity',{}).get('openingHoursSpecification',[]):
                day = opening_hour.get('dayOfWeek','')
                opens = opening_hour.get('opens','')
                closes = opening_hour.get('closes','')
                opening_hours.append(f'{day} : {opens}-{closes}')
            item['Opening Hours'] = ', '.join(e.strip() for e in opening_hours)

            item['Rating'] = data.get('mainEntity',{}).get('aggregateRating',{}).get('ratingValue','')
            item['No of Reviews'] = data.get('mainEntity',{}).get('aggregateRating',{}).get('reviewCount','')
            item['Image URL'] = data.get('mainEntity',{}).get('image','')

        item['Detail URL'] = response.url
        yield item
