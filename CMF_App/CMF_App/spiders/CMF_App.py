#################       CMF_App

import json, re, csv, scrapy
from copy import deepcopy
from scrapy.selector import Selector

class CMF_App(scrapy.Spider):
    name = 'CMF_App'

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        # 'cookie': 'JSESSIONID=5831B29CA6152921230A927C2C19FA37; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; _gcl_au=1.1.78660972.1716318682; OptanonAlertBoxClosed=2024-05-21T19:11:38.074Z; _gid=GA1.2.730351489.1716318699; _gat_UA-84202635-11=1; arp_scroll_position=300; AWSALBAPP-0=AAAAAAAAAABVdrD1UpMc0kxEcxe5dtlFtZ7aAiEojv39PWbDG+KOY8QtI1PKcdRa++nMkmU8w5Syop0EXco5WSLh/b5BlKCc5mcS9fpTkhjR52uRUOqh82ag9LTcQY6n4aKPg/S6TrRS4w==; _ga=GA1.2.374264585.1716318682; OptanonConsent=isIABGlobal=false&datestamp=Wed+May+22+2024+01%3A16%3A33+GMT%2B0500+(Pakistan+Standard+Time)&version=6.26.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1&geolocation=%3B&AwaitingReconsent=false; _ga_1WLEWC49T8=GS1.1.1716318682.1.1.1716322597.0.0.0',
        'faces-request': 'partial/ajax',
        # 'origin': 'https://catalog.mann-filter.com',
        'priority': 'u=1, i',
        # 'referer': 'https://catalog.mann-filter.com/EU/tur/catalog/MANN-FILTER%20Katalog%20Europa/Ya%C4%9F%20filtresi/W%2011%20024',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    data1 = {
        'javax.faces.ViewState': '',
        'productDetail': 'productDetail',
        'productDetail:productDetailTabPanel-value': 'productDetail:productDetailUsageTab',
        'javax.faces.partial.render': '@component',
        'rfExt': 'null',
        'AJAX:EVENTS_COUNT': '1',
        'javax.faces.partial.ajax': 'true',
        # 'javax.faces.source': 'productDetail:productDetailUsageTab',
        'javax.faces.partial.execute': 'productDetail:productDetailUsageTab @component',
        'org.richfaces.ajax.component': 'productDetail:productDetailUsageTab',
        'productDetail:productDetailUsageTab': 'productDetail:productDetailUsageTab',
    }

    data2 = {
        'javax.faces.ViewState': '',
        'name': 'FORD',
        'javax.faces.source': '',
        'javax.faces.partial.execute': '',
        'org.richfaces.ajax.component': '',
        # 'productDetail:j_idt381': 'productDetail:j_idt381',
        'javax.faces.partial.render': '@component',
        'productDetail': 'productDetail',
        'productDetail:productDetailTabPanel-value': 'productDetail:productDetailUsageTab',
        'rfExt': 'null',
        'AJAX:EVENTS_COUNT': '1',
        'javax.faces.partial.ajax': 'true',
    }
    data3 = {
        'javax.faces.ViewState': '',
        'name': '',
        'javax.faces.source': '',
        'javax.faces.partial.execute': '',
        'org.richfaces.ajax.component': '',
        # 'productDetail:j_idt383': 'productDetail:j_idt383',
        'productDetail': 'productDetail',
        'productDetail:productDetailTabPanel-value': 'productDetail:productDetailUsageTab',
        'javax.faces.partial.render': '@component',
        'rfExt': 'null',
        'AJAX:EVENTS_COUNT': '1',
        'javax.faces.partial.ajax': 'true',
    }

    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000
        },
        "REQUEST_FINGERPRINTER_CLASS": "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ZYTE_API_KEY": '' ,
        "ZYTE_API_TRANSPARENT_MODE": True,
        # "ZYTE_API_EXPERIMENTAL_COOKIES_ENABLED": True,
    }

    def start_requests(self):
        yield scrapy.Request(url='https://catalog.mann-filter.com/EU/tur', callback=self.parse,  #headers=self.headers
                             )

    def parse(self, response):
        payload = deepcopy(self.data1)
        # viewstate_value = response.xpath('//*[@id="j_id1:javax.faces.ViewState:0"]/text()').get()
        viewstate_value = response.xpath('//*[@id="j_id1:javax.faces.ViewState:0"]/@value').get()

        payload['javax.faces.ViewState'] = viewstate_value
        url = 'https://catalog.mann-filter.com/EU/tur/catalog/MANN-FILTER%20Katalog%20Europa/Ya%C4%9F%20filtresi/W%2011%20024'
        yield scrapy.FormRequest(url=url, formdata=payload, method='POST', callback=self.parse_app, #headers=self.headers,
                                 meta={'url':url})

    def parse_app(self, response):
        selector = Selector(text=response.text)
        j_id_loop = selector.xpath("//span[contains(@id,'productDetail:j_idt')]/@id").getall()
        if j_id_loop:
            j_id2 = j_id_loop[-1]
            loop = selector.xpath("//*[contains(@class,'advancedLi li_lv_1')]")
            for index, categories in enumerate(loop):
                cat_name = categories.css('.label_lv1 ::text').get('').strip()

                req_j_id_text = categories.xpath("//span[contains(@id,'productDetail:j_idt')]/@id").get('').strip()
                payload = deepcopy(self.data2)
                # viewstate_value = response.xpath('//*[@id="j_id1:javax.faces.ViewState:0"]/text()').get()
                viewstate_value = response.xpath(f'//*[@id="j_id1:javax.faces.ViewState:{index}"]/@value').get()

                payload['javax.faces.ViewState'] = viewstate_value
                payload['name'] = cat_name
                payload['javax.faces.source'] = req_j_id_text
                payload['javax.faces.partial.execute'] = f'{req_j_id_text} @component'
                payload['org.richfaces.ajax.component'] = req_j_id_text
                payload[req_j_id_text] = req_j_id_text

                url = response.meta['url']
                yield scrapy.FormRequest(url=url, formdata=payload, method='POST', callback=self.parse_app_category, #headers=self.headers,
                                         meta={'url':url,'j_id2':j_id2, 'cookiejar': index})

    def parse_app_category(self, response):
        selector = Selector(text=response.text)
        for index, sub_categories in enumerate(selector.xpath("//*[contains(@class,'label_lv2')]")):
            sub_cat_name = sub_categories.css('::text').get('').strip()

            req_j_id_text = response.meta['j_id2']

            payload = deepcopy(self.data3)
            # viewstate_value = response.xpath('//*[@id="j_id1:javax.faces.ViewState:0"]/text()').get()
            viewstate_value = response.xpath(f'//*[@id="j_id1:javax.faces.ViewState:0"]/@value').get()
            payload['javax.faces.ViewState'] = viewstate_value
            payload['name'] = sub_cat_name
            payload['javax.faces.source'] = req_j_id_text
            payload['javax.faces.partial.execute'] = f'{req_j_id_text} @component'
            payload['org.richfaces.ajax.component'] = req_j_id_text
            payload[req_j_id_text] = req_j_id_text
            url = response.meta['url']
            yield scrapy.FormRequest(url=url, formdata=payload, method='POST', callback=self.parse_app_detail, #headers=self.headers,
                                     meta={'url':url,'cookiejar':response.meta['cookiejar']} )

    def parse_app_detail(self, response):
        selector = Selector(text=response.text)
        count = 1
        for Rows in selector.css('.row'):
            item = dict()
            item['Ser'] = count
            count += 1
            item['Vehicle Type'] = Rows.css('.vehicle_type a ::text').get('').strip()
            item['Vehicle Motor'] = Rows.css('.vehicle_motor .tableContent ::text').get('').strip()
            item['Vehicle Hub (ccm)'] = Rows.css('.vehicle_hub .tableContent ::text').get('').strip()
            item['Vehicle kW'] = Rows.css('.vehicle_kw .tableContent ::text').get('').strip()
            item['Vehicle HP (PS)'] = Rows.css('.vehicle_hp .tableContent ::text').get('').strip()
            item['Year of Manufacture'] = (Rows.css('.vehicle_year .tableContent ::text').get('').strip()
                                           .replace('\t','').replace('\n','').replace('→',''))
            yield item
