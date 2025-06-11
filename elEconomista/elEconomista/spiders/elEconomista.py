##########          elEconomista

import time
import scrapy

class elEconomista(scrapy.Spider):
    name = 'elEconomista'
    prefix1 = 'https://ranking-empresas.eleconomista.es'
    url1 = "https://ranking-empresas.eleconomista.es/sector-3513.html"
    headers1 = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': '_ga=GA1.3.1558138848.1713888945; _gid=GA1.3.1043295208.1713888945; JSESSIONID=DA0BB48C8872E88B6C2FFD2A5F7B36A1.directorio_tomcat1; _gid=GA1.2.1043295208.1713888945; _ga=GA1.1.1558138848.1713888945; _ga_W4Y1EQ1180=GS1.2.1713889204.1.0.1713889204.60.0.0; _ga_X57MLCTDPF=GS1.1.1713888945.1.1.1713889281.0.0.0; arp_scroll_position=4080; _ga_DGRC77G6MT=GS1.1.1713889203.1.1.1713889322.0.0.0; JSESSIONID=ADF2734A8EC278721AFB81DE5011CEE8.directorio_tomcat1',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    # url2 = 'https://empresite.eleconomista.es/Actividad/ELECTRICA-GUIXES-ENERGIA-SL/'
    url2 = 'https://empresite.eleconomista.es/Actividad/{}/'
    headers2 = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'max-age=0',
        'content-length': '0',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': '_gid=GA1.2.1043295208.1713888945; JSESSIONID=5C49B705B8C955346EA72D0EE4E02E80.directorio_tomcat1; COOKIEMESH="c7a4ee7c7cefcc78"; _ga=GA1.3.1558138848.1713888945; _gid=GA1.3.1043295208.1713888945; _ga_X57MLCTDPF=GS1.1.1713888945.1.1.1713890805.0.0.0; _ga=GA1.2.1558138848.1713888945; _ga_DGRC77G6MT=GS1.1.1713889203.1.1.1713890832.0.0.0; _ga_W4Y1EQ1180=GS1.2.1713889204.1.1.1713890832.5.0.0; arp_scroll_position=37',
        'origin': 'https://empresite.eleconomista.es',
        'priority': 'u=0, i',
        'referer': 'https://empresite.eleconomista.es/Actividad/SUMINISTRO-DE-GAS-Y-ELECTRICIDAD/',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    custom_settings = {
        'FEED_URI': 'Output/elEconomista.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',

        'HTTPERROR_ALLOW_ALL': True,
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000
        },
        "REQUEST_FINGERPRINTER_CLASS": "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ZYTE_API_KEY": "",  # Please enter your API Key here

        "ZYTE_API_TRANSPARENT_MODE": True,
        # "ZYTE_API_EXPERIMENTAL_COOKIES_ENABLED": True,
    }

    count = 1
    def start_requests(self):
        yield scrapy.Request(url=self.url1, headers=self.headers1)

    def parse(self, response):
        for company in response.css('td.tal a'):
            company_name = company.css('::text').get('').strip()
            URL1 = company.css('::attr(href)').get('').strip()
            print(f'{self.count} # Company name is : {company_name} and its url is {URL1}')
            self.count += 1

            updated_company_name = company_name.replace(' ','-').replace('.','').replace("Ñ", "N")
            updated_url = self.url2.format(updated_company_name)
            yield scrapy.Request(url=updated_url, callback=self.search_company, headers=self.headers2,
                                 meta={'company_name':company_name,'URL1':URL1})

        '''             Pagination             '''
        next_page = response.xpath("//*[contains(text(),'»')]/@href").get('').strip()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse, headers=self.headers1)

    def search_company(self, response):
        company_name = response.meta['company_name']
        for company in response.css('div.cardCompanyBox h3 a'):
            if (company.css('::text').get('').strip()).lower() == (company_name).lower():
                company_new_url = company.css('::attr(href)').get('').strip()
                yield scrapy.Request(url=company_new_url, callback=self.detail_parse, headers=self.headers2,
                                     meta={'URL1':response.meta['URL1']})
                # time.sleep(2)


    def detail_parse(self, response):
        item = dict()
        item['Business Name'] = response.xpath("//*[contains(text(),'Razón social')]/following-sibling::span[1]/text()").get('').strip()    #

        item['Address'] = response.xpath("//*[contains(text(),'Dirección')]/parent::div[1]/following-sibling::span[1]/text()").get('').strip()    #
        item['Phone'] = response.xpath("//*[contains(text(),'Teléfono')]/parent::div[1]/following-sibling::span[1]/span[1]/text()").get('').strip()    # Phone

        web = response.xpath("//*[contains(text(),'Web')]/parent::div[1]/following-sibling::a")    # Web
        if web.css('::attr(href)').get('').strip() != "/Publicar_Empresa":
            item['Web'] = web.css("::text").get('').strip()

        email = response.xpath("//*[contains(text(),'Email')]/parent::div[1]/following-sibling::a")    # Email
        if email.css('::text').get('').strip() != "Añadir Email":
            # item['Email'] = email.xpath(".//*[contains(@href,'mailto:')]/text()").get('').strip()
            item['Email'] = email.css("::text").get('').strip()

        item['CIF'] = response.xpath("//*[contains(text(),'CIF')]/following-sibling::span[1]/text()").get('').strip()    # CIF
        item['Legal Form'] = response.xpath("//*[contains(text(),'Forma jurídica')]/following-sibling::span[1]/text()").get('').strip()    #
        item['Sector'] = response.xpath("//*[contains(text(),'Sector')]/following-sibling::span[1]/text()").get('').strip()    # Sector
        item['Constitution Date'] = response.xpath("//*[contains(text(),'Fecha de constitución')]/following-sibling::span[1]/text()").get('').strip()    #
        item['Last Change Date'] = response.xpath("//*[contains(text(),'Fecha último cambio')]/following-sibling::span[1]/text()").get('').strip()    #

        item['Social Object'] = response.xpath("//*[contains(text(),'Objeto social')]/following-sibling::span[1]/text()").get('').strip()    #
        item['Commercial Registry'] = response.xpath("//*[contains(text(),'Registro Mercantil')]/following-sibling::span[1]/text()").get('').strip()    #
        item['Trade Names'] = response.xpath("//*[contains(text(),'Denominaciones comerciales')]/following-sibling::span[1]/text()").get('').strip()    #
        item['Activity'] = response.xpath("//*[contains(text(),'Actividad')]/following-sibling::span[1]/text()").get('').strip()    #
        item['CNAE Activity'] = response.xpath("//*[contains(text(),'Actividad CNAE')]/following-sibling::span[1]/text()").get('').strip()    #

        item['URL1'] = response.meta['URL1']
        item['URL2'] = response.url

        yield item
        # time.sleep(5)


