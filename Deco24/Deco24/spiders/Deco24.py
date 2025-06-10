import json

import scrapy
import math
from copy import deepcopy
class Deco24(scrapy.Spider):
    name = 'Deco24'
    url = "https://www.deco24.hu/akcio?infinite_page={}"
    headers = {
        'authority': 'www.deco24.hu',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': 'UnasServiceProxyID=s40~ProxyOK; UnasID=515933ab5f2d429e9a93078512fc4bd1; UN_last_prod=a%3A1%3A%7Bi%3A0%3Bs%3A6%3A%22BCB88Y%22%3B%7D; UN_cart_0=a%3A2%3A%7Bs%3A4%3A%22cikk%22%3Ba%3A1%3A%7Bi%3A1%3Bs%3A6%3A%22BCB88Y%22%3B%7Ds%3A2%3A%22db%22%3Ba%3A1%3A%7Bi%3A1%3Bd%3A9%3B%7D%7D-----EndCart-----; _ga=GA1.1.834055863.1708354996; _gcl_au=1.1.1885187259.1708370107; BarionMarketingConsent.2570633324=1; UN_cookie_close=1; UN_cookie_allow=1; _ga_Q1K0YT72K9=GS1.1.1708370107.2.1.1708370224.0.0.0; ba_sid=a0c67147-994a-41ec-941f-2c70f03ee09e; ba_sid.2570633324=03eec041-7f6e-4e7a-bed5-156e54bd2a65; ba_vid.2570633324=place_ba_vid%2Cd3ab36769d6d694aa1a79a3572093b4c%2C1708355005310%2C1708370230832%2C1708370230832%2C03eec041-7f6e-4e7a-bed5-156e54bd2a65%2C1',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    custom_settings = {'FEED_URI': 'Deco24 Records .csv',
                       'FEED_FORMAT': 'csv',
                       'FEED_EXPORT_ENCODING': 'utf-8-sig', }

    aval_url = "https://www.deco24.hu/shop_ajax/ajax_cart.php"
    aval_payload = {
        'get_ajax': '1',
        'result_type': 'json',
        'lang_master': 'hu',
        'action': 'add',
        'sku': '',
        'qty': '1000',
        'product_param': '',
    }
    aval_headers = {
        'authority': 'www.deco24.hu',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.deco24.hu',
        # 'referer': 'https://www.deco24.hu/songmics-furdoszoba-sarokpolc-allithato-feher-85-305cm',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    def start_requests(self):
        yield scrapy.Request(url=self.url.format(1), headers=self.headers, callback=self.parse)

    def parse(self, response):
        total_products = int(response.xpath("//span[contains(text(),'termék')]/preceding-sibling::span/text()").get('').strip())
        entries_per_page = 0
        for product in response.css('.product__name'):
            entries_per_page += 1
        final_page = math.ceil(total_products/entries_per_page)
        yield scrapy.Request(url=self.url.format(final_page), headers=self.headers, callback=self.final_parse)

    def final_parse(self, response):
        entries_per_page = 0
        for product in response.css('.product__name'):
            entries_per_page += 1
            product_url = product.css('a::attr(href)').get('').strip()
            product_name = product.css('a::text').get('')
            yield scrapy.Request(url=product_url, headers=self.headers, callback=self.detail)

    def detail(self, response):
        item = dict()
        item['Name'] = response.css('.line-clamp--3-12::text').get('').strip()
        SKU = response.css('.artdet__sku-value ::text').get('').strip()
        item['SKU'] = response.css('.artdet__sku-value ::text').get('').strip()

        item['Price'] = (response.css(f'#price_net_brutto_{SKU}::text').get('').strip()).replace(' ',',') + ' (Ft)'
        item['Sale Price'] = (response.css(f'#price_akcio_brutto_{SKU}::text').get('').strip()).replace(' ',',') + ' (Ft)'

        item['Weight (Kg)'] = response.xpath("//span[contains(text(),'Súly')]/parent::div/parent::div/following-sibling::div/div/text()").get('').strip()
        item['Brand'] = response.xpath("//span[contains(text(),'Márka')]/parent::div/parent::div/following-sibling::div/div/text()").get('').strip()
        item['Warrenty'] = response.xpath("//span[contains(text(),'Garancia')]/parent::div/parent::div/following-sibling::div/div/text()").get('').strip()
        item['Size'] = response.xpath("//span[contains(text(),'Méret')]/parent::div/parent::div/following-sibling::div/div/text()").get('').strip()
        item['Material'] = response.xpath("//span[contains(text(),'Anyag')]/parent::div/parent::div/following-sibling::div/div/text()").get('').strip()

        payload = deepcopy(self.aval_payload)
        payload['sku'] = SKU
        yield scrapy.FormRequest(url=self.aval_url, formdata=payload, headers=self.aval_headers, method='POST',
                                 callback=self.aval_detail, meta={'item': item,'Prod_url':response.url})

    def aval_detail(self, response):
        item = response.meta.get('item')
        body_str = response.body.decode('utf-8')
        data = json.loads(body_str)

        quantity = data.get('qty_all', None)
        if quantity is not None:
            item['Available Quantity'] = quantity

        item['Product URL'] = response.meta.get('Prod_url')
        yield item


