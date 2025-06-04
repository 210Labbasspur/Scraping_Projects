import scrapy

class LocalStore(scrapy.Spider):
    name = 'ASAdirectory'
    url = "https://ww2.amstat.org/consultantdirectory/index.cfm?fuseaction=searchresults"
    prefix = 'https://ww2.amstat.org/consultantdirectory/'
    # custom_settings = {
    #     'FEED_URI': 'ASA_Directory.csv',
    #     'FEED_FORMAT': 'csv',
    #     'FEED_EXPORT_ENCODING': 'utf-8-sig',
    # }
    headers = {
      'authority': 'ww2.amstat.org',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
      'cache-control': 'max-age=0',
      'cookie': 'JSESSIONID=B1C5863185788CCCE83CD0E06E3F046F.cfusion; _sp_ses.ae38=*; _sp_id.ae38=e314548f35d99f7b.1688402670.4.1688573494.1688566323.09237cc2-5acc-48f4-8812-2588d7ed9229',
      'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'cross-site',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers)

    def parse(self, response):
        item = dict()
        for category in response.css('tr+ tr td:nth-child(1)'):#[:1]:
            consultant_url = self.prefix+category.css('::attr(href)').get('')
            item['Detail_URL'] = consultant_url
            yield response.follow(url=consultant_url, callback=self.detail_page, headers=self.headers,  meta={'item': item})

    def detail_page(self, response):
        item = response.meta['item']

        item['Name'] = response.css('h4::text').get('').strip()
        item['Affiliation'] = response.css('td tr:nth-child(1) strong ::text').get('').strip()

        item['Email'] = response.css('#profile a ::text').get('').strip()
        item['Phone#'] = response.css('tr:nth-child(2) td+ td ::text').get('').strip()

        item['Address'] = response.css('td td tr:nth-child(3) td+ td ::text').get('').strip()

        area_of_expertise = response.css('tr:nth-child(6) td:nth-child(1) ::text').extract()
        item['Area of Expertise'] = ', '.join([str(item).strip() for item in area_of_expertise if item])

        app_specialities = response.css('tr:nth-child(6) td+ td ::text').getall()
        item['Application Specialities'] = ','.join([str(item).strip() for item in app_specialities if item])

        pertinent_education = response.css('tr:nth-child(9) td:nth-child(1) ::text').getall()
        item['Pertinent Education'] = ','.join([str(item).strip() for item in pertinent_education if item])

        language_fluency = response.css('tr:nth-child(9) td+ td ::text').getall()
        item['Language Fluency (in addition to English)'] = ','.join([str(item).strip() for item in language_fluency if item])


        yield item

