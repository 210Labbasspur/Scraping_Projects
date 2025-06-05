import json
import scrapy

class BeautyBrands(scrapy.Spider):
    name = 'BeautyBrands'
    url = "https://display.powerreviews.com/m/2555/l/en_US/media?filter=Social&paging.size=15&_noconfig=true&apikey=95777081-c76c-4b01-9550-e000229beb0f"
    prefix = 'https://display.powerreviews.com'
    custom_settings = {
        'FEED_URI': 'BeautyBrands11.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }
    headers = {
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'Referer': 'https://www.beautybrands.com/',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"'
    }

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers)

    def parse(self, response):
        data = json.loads(response.body)
        for result in data['results'][:15]:
            item = dict()
            if result.get('product_name') is not None:
                product_url = 'https:'+result.get('product_url','').strip()
                item['Detail_URL'] = product_url
                yield response.follow(url=product_url, callback=self.api_page, headers=self.headers, meta={'item': item})
                # yield response.follow(url='https://www.beautybrands.com/product/american+crew+3-in-1.do',
                #                       callback=self.api_page, headers=self.headers, meta={'item': item})

        next_page = self.prefix + data['paging']['next_page_url']
        if next_page:
            yield response.follow(url=next_page, callback=self.parse, headers=self.headers)

    def api_page(self, response):
        item = response.meta['item']
        item['Name'] = response.xpath("//*[contains(@itemprop,'name')]/text()").get('').strip()
        item['Item#'] = response.xpath("//*[contains(@class,'ml-product-code desktop')]/text()").get('').strip()
        item['Price'] = response.xpath("//*[contains(@itemprop,'price')]/@content").getall()
        item['Detail'] = response.css('.ml-product-desc-short ::text').getall()
        item['Why we love it'] = response.css('.love-it p::text').get('').strip()

        item['Benefits'] = ''
        benefits = response.css('#accordionTarget01 ::text').getall()
        for b in benefits:
            item['Benefits'] = c

        item['Directions'] = response.css('#accordionTarget02 .panel-body::text').get('').strip()
        item['Ingredients'] = response.css('#accordionTarget03 .panel-body::text').get('').strip()
        item['Facebook'] = response.css('.fb-xfbml-parse-ignore ::attr(href)').get('').strip()
        item['Twitter'] = response.css('.addthis_button_twitter ::attr(href)').get('').strip()

        item['Instagram'] = response.xpath("//*[contains(@class,'ml-icon ml-social-icon ml-icons-margin ml-icon-instagram')]/@href").get('').strip()
        item['Youtube'] = response.xpath("//*[contains(@class,'ml-icon ml-social-icon ml-icons-margin')]/@href").get('').strip()
        item['Pinterest'] = response.xpath("//*[contains(@class,'addthis_button_pinterest_share')]/@href").get('').strip()

        id = response.css('.ml-product-code::text').get('').strip()
        if id:
            api_url = 'https://display.powerreviews.com/m/2555/l/en_US/product/{}/reviews?apikey=95777081-c76c-4b01-9550-e000229beb0f&_noconfig=true'
            yield response.follow(url=api_url.format(id), callback=self.detail_page, headers=self.headers, meta={'item': item})
        else:
            yield item

        product_type = response.xpath("//*[contains(@class,'ml-zoom-swatch-view')]")
        if product_type:
            count=0
            for flavour in product_type:
                item['Product_Flavour'] = flavour.css('::attr(data-mlcode)').get('').strip()
                item['Image'] = flavour.css('img::attr(src)').get('').strip()
                if count is 0:
                    item['Product_type'] = 'Variable'
                else:
                    item['Product_type'] = 'Variation'
                count=count+1
                yield item


    def detail_page(self, response):
        item = response.meta['item']
        data = json.loads(response.body)
        item['Reviews'] = data['paging']['total_results']

        yield item
