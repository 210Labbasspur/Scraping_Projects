import json
import scrapy
from datetime import datetime
from copy import deepcopy


class emp(scrapy.Spider):
    name = 'emp'
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
        'FEED_URI': f'output/EMP - {datetime.now().strftime("%d-%m-%Y")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }

    data = {
        'ppp': '-1',
        # 'ppp': '768',
    }
    def start_requests(self):
        url = 'https://www.engineeredmarineproducts.com'
        yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        count = 1
        for category in response.css('#menu-applications-1 .menu-item-object-product_cat a'):
            category_url = category.css('::attr(href)').get('').strip()
            print(count, category_url)
            count += 1
            payload = deepcopy(self.data)
            # # yield scrapy.FormRequest(url=category_url, method='POST', formdata=payload, callback=self.listing_parse,
            # #                          headers=self.headers)
            yield scrapy.Request(url=category_url, callback=self.listing_parse, headers=self.headers)
        complete_url = 'https://www.engineeredmarineproducts.com/page/1/?s&product_cat=0&post_type=product'

    def listing_parse(self, response):
        total_products = response.xpath("//*[contains(text(),'Showing')]/text()").get('').strip()
        print('Total products are : ', total_products)
        for product in response.css('.product-item__body .woocommerce-LoopProduct-link'):
            product_url = product.css('::attr(href)').get('').strip()
            yield scrapy.Request(url=product_url, callback=self.detail_parse, headers=self.headers)

        next_page = response.css('a.next ::attr(href)').get('').strip()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.listing_parse, headers=self.headers)


    def detail_parse(self, response):
        item = dict()

        name = response.url.split('/')[-2]
        item['Product Name'] = name
        image_url = f'https://www.engineeredmarineproducts.com/wp-content/uploads/{name}.jpg'
        item['Image URL'] = image_url
        item['SKU'] = ''
        sku_data = response.xpath("//*[contains(@class,'yoast-schema-graph yoast-schema-graph--woo')]/text()").get('').strip()
        if sku_data:
            data = json.loads(sku_data)
            item['SKU'] = data.get('@graph',[])[0].get('sku','')
            item['Product Name'] = data.get('@graph',[])[0].get('name','')
            image_url = f'https://www.engineeredmarineproducts.com/wp-content/uploads/{name}.jpg'
            item['Image URL'] = image_url

        categories = response.css('.loop-product-categories a::text').getall()
        item['Categories'] = ', '.join(c.strip() for c in categories)

        for e in range(6):
            item[f'Description_{e+1}'] = ''
        descriptions = response.css('.electro-description p, .electro-description h1')
        d_index = 1
        for description in descriptions:
            desc = ', '.join(e.strip() for e in description.css('::text').getall())
            if desc:
                item[f'Description_{d_index}'] = ' '.join(e.strip().replace('\ufeff','') for e in description.css('::text').getall())
                d_index += 1

        item['Product_URL'] = response.url
        yield item
