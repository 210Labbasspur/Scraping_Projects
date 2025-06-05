import time
import scrapy
import json
from BestGasket.items import BestgasketItem

class BestGasket(scrapy.Spider):
    # custom_settings = {'FEED_URI': 'BestGasket.csv',
    #                    'FEED_FORMAT': 'csv',
    #                    'FEED_EXPORT_ENCODING': 'utf-8-sig', }
    Count = 0
    name = 'BestGasket'
    url = "https://bestgasket.com/product-search/"
    headers = {
        'authority': 'bestgasket.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    url_1 = "https://bestgasket.com/gasket_search_{type}_api/?search_query=makeSearch"
    url_2 = "https://bestgasket.com/gasket_search_{type}_api/?search_query=setSearchByMake"
    model_payload = "MAKE_ID={make_id}"
    model_headers = {
        'authority': 'bestgasket.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://bestgasket.com',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    url_3 = "https://bestgasket.com/gasket_search_{type}_api/?search_query=setSearchByModel"
    year_payload = "MAKE_ID={make_id}&MODEL_ID={model_id}"

    url_4 = "https://bestgasket.com/gasket_search_{type}_api/?search_query=setSearchMETA"
    set_payload = "MAKE_ID={make_id}&MODEL_ID={model_id}&YEAR_ID={year_id}"

    url_5 = "https://bestgasket.com/gasket_search_{type}_api/?search_query=getFullSet"
    detail_payload = "set_id={set_id}"

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        for prod in response.css('.blog a'):#[:1]:
            item = dict()
            item['Type.'] = prod.css('::text').get('').strip()
            if item['Type.'] == 'Engine Gaskets':
                type = 'engine'
            elif item['Type.'] == 'Trans/Rear Axle/Other':
                type = 'transmission'

            yield scrapy.Request(url=self.url_1.format(type=type), headers=self.headers,
                                 callback=self.Make, meta={'item': item, 'type':type})

    def Make(self, response):
        item = response.meta['item']
        type = response.meta['type']
        data = json.loads(response.body)
        for make in data['makes']:#[:2]:
            item['Make_ID'] = make.get('make').get('ID')
            item['Brand'] = make.get('make').get('post_title')
            yield scrapy.Request(url=self.url_2.format(type=type), headers=self.model_headers,
            method="POST", body=self.model_payload.format(make_id=make.get('make').get('ID')), callback=self.Model,
                                 meta={'item': item,'m_id':make.get('make').get('ID'), 'type':type})

    def Model(self, response):
        item = response.meta['item']
        type = response.meta['type']
        m_id = response.meta['m_id']
        data = json.loads(response.body)
        for model in data['models']:#[:2]:
            item['Model_ID'] = model.get('model_id')
            item['Product Category'] = model.get('model_name')
            yield scrapy.Request(url=self.url_3.format(type=type), headers=self.model_headers, method="POST",
                    body=self.year_payload.format(make_id=m_id, model_id=model.get('model_id')),
                    callback=self.Year, meta={'item': item,'m_id':m_id, 'mo_id':model.get('model_id'), 'type':type})

    def Year(self, response):
        item = response.meta['item']
        type = response.meta['type']
        m_id = response.meta['m_id']
        mo_id = response.meta['mo_id']
        data = json.loads(response.body)
        for model in data['years']:#[:2]:
            item['Year_ID'] = model.get('year_id')
            item['Year/Model Info'] = model.get('year_name')
            yield scrapy.Request(url=self.url_4.format(type=type), headers=self.model_headers, method="POST",
            body=self.set_payload.format(make_id=m_id, model_id=mo_id, year_id=model.get('year_id')),
                                  callback=self.Sets, meta={'item': item, 'type':type})

    def Sets(self, response):
        item = response.meta['item']
        type = response.meta['type']
        data = json.loads(response.body)
        for model in data['sets']:#[:2]:
            item['Description'] = model.get('set_name')
            item['Part No.'] = model.get('set_meta').get('SET_NO')
            yield scrapy.Request(url=self.url_5.format(type=type), headers=self.model_headers, method="POST",
            body=self.detail_payload.format(set_id=model.get('set_id')), callback=self.Details, meta={'item': item})

    def Details(self, response):
        item = response.meta['item']
        data = json.loads(response.body)
        for model in data['set_gaskets']:#[:2]:
            item['Ser'] = self.Count
            self.Count += 1
            item['Qty'] = model.get('gasket').get('GASKET_QTY')
            item['Part No'] = model.get('gasket').get('PART_NO')
            item['Contents'] = model.get('gasket').get('DESCRIPTION')
            item['Set ID'] = model.get('gasket').get('set_id')
            item['Gasket ID'] = model.get('gasket').get('gasket_id')
            item['Sort Value'] = model.get('gasket').get('sort_value')

            # item['Gasket Img'] = "https://bestgasket.com" + model.get('gasket').get('gasket_image')
            gasket_img = "https://bestgasket.com" + model.get('gasket').get('gasket_image')
            # item['Gasket Img'] = self.url_join(gasket_img, response)
            download_img = BestgasketItem()
            download_img['image_urls'] = 'https://bestgasket.com' + model.get('gasket').get('gasket_image')
            download_img['image_urls'] = self.url_join(gasket_img, response)
            # yield download_img

            yield item

    def url_join(self, rel_img_urls, response):
        joined_urls = []
        joined_urls.append(response.urljoin(rel_img_urls))
        return joined_urls
