import scrapy
from scrapy.utils.response import open_in_browser

class AllegroMedical(scrapy.Spider):
    name = 'AllegroMedical'
    url = "https://www.allegromedical.com/site-map/"
    custom_settings = {
        'FEED_URI': 'AllegroMedical (Reviews).csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }
    headers = {
      'authority': 'www.allegromedical.com',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
      'cache-control': 'max-age=0',
      'cookie': 'PHPSESSID=4idmkjo3v5tqa97bac3e7bk9p9; form_key=pdFbj2u5Uyp2WMkv; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-cache-sessid=true; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; visitor_id=685e1447-4538-4575-b16d-b89b817836e7; visit_id=699aea83-99b4-4462-8f2b-6e05ce9a05fd; mage-messages=; form_key=pdFbj2u5Uyp2WMkv; last-view-popup=1686492500598; last-view-popup=1686492588117',
      'referer': 'https://www.allegromedical.com/',
      'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    review_url = "https://www.allegromedical.com/review/product/listAjax/id/{}/?sort=recent"
    review_headers = {
      'authority': 'www.allegromedical.com',
      'accept': 'text/html, */*; q=0.01',
      'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
      # 'cookie': 'mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-cache-sessid=true; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; visitor_id=685e1447-4538-4575-b16d-b89b817836e7; form_key=pdFbj2u5Uyp2WMkv; facebook_latest_uuid={"event":"CustomizeProduct","uuid":"ea5859df-ad95-4795-93f8-51c51ecf8606"}; PHPSESSID=uj5736v5l2uoh1blge2ussfg4r; last-view-popup=1686589695371; visit_id=debefe8a-2a8c-41f6-8933-c57c30745af8; mage-messages=; section_data_ids=%7B%22review%22%3A1686496528%2C%22company%22%3A1686668851%2C%22requisition%22%3A1686668851%7D; last-view-popup=1686669695788; private_content_version=5b8750ef951323aac435f184eb8b3ac3',
      # 'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjIwMDExODIiLCJhcCI6IjExMDMyMjMxMzAiLCJpZCI6IjNjYzI0ZmMwZWYwM2FkZGEiLCJ0ciI6ImYxN2M4ZjBjYTkyYzUyOWE4MmQ1N2I4MDllMzVlMTAwIiwidGkiOjE2ODY2Njk3MjY0NDl9fQ==',
      # 'referer': 'https://www.allegromedical.com/products/bd-luer-lok-disposable-syringe-1-ml/',
      'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      # 'traceparent': '00-f17c8f0ca92c529a82d57b809e35e100-3cc24fc0ef03adda-01',
      # 'tracestate': '2001182@nr=0-1-2001182-1103223130-3cc24fc0ef03adda----1686669726449',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
      'x-newrelic-id': 'VgYHUFdbChABVFZSDgcBX1UI',
      'x-requested-with': 'XMLHttpRequest'
    }

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers)

    def parse(self, response):
        for category in response.css('.level-1 > a'):   #[:3]:
            category_url = category.css('::attr(href)').get('')
            if category_url:
                yield response.follow(url=category_url, callback=self.listing_page, headers=self.headers)

    def listing_page(self, response):
        for list_item in response.css('.product-item-link'):
            product_url = list_item.css('::attr(href)').get('')
            if product_url:
                yield response.follow(url=product_url, callback=self.detail_page, headers=self.headers)

        next_page = response.css('.next ::attr(href)').get('')
        if next_page:
            yield response.follow(url=next_page, headers=self.headers, callback=self.listing_page)

    def detail_page(self, response):
        item = dict()
        item['Detail URL'] = response.xpath("//*[contains(@rel,'canonical')]/@href").get('').strip()
        item['Name'] = response.css('.base ::text').get('').strip()
        item['Image'] = response.css('.fotorama__img ::attr(src)').get('').strip()
        item['Item#'] = response.css('.sku .value ::text').get('').strip()
        item['Reviews'] = response.css('.add ::text').get('').strip()
        item['Brand'] = response.css('.amshopby-option-link a::text').get('').strip()
        item['Price($)'] = response.css('.price ::text').get('').strip()
        item['Details'] = response.css('#description li::text, #description strong::text, #description p::text').getall()
        item['Features'] = response.css('#bulletdescription\.tab li ::text').getall()
        item['Brand Name'] = response.xpath("//td[contains(@data-th,'Brand Name')]/text()").get('').strip()
        item['Manufacturer No'] = response.xpath("//td[contains(@data-th,'Manufacturer Number')]/text()").get('').strip()

        no_of_reviews = response.css('#tab-label-reviews-title .counter ::text').get('').strip()
        item['No of Reviews'] = no_of_reviews
        item['Review Title'] = ''
        item['Review Content'] = ''
        item['Review By'] = ''
        item['Review On'] = ''

        if response.xpath("//span[contains(@itemprop,'offers')]"):
            for options in response.xpath("//span[contains(@itemprop,'offers')]"):
                if options.css(':nth-child(1)::attr(content)').get('').strip():
                    item['Name'] = options.css(':nth-child(1)::attr(content)').get('').strip()
                if options.css(':nth-child(4)::attr(content)').get('').strip():
                    item['Price($)'] = options.css(':nth-child(4)::attr(content)').get('').strip()
                yield item
        else:
            yield item

        if no_of_reviews is not None:
            product_id = response.xpath("//*[contains(@class,'price-box price-final_price')]/@data-product-id").get('').strip()
            yield response.follow(url=self.review_url.format(str(product_id)),
                                      callback=self.review_page, headers=self.review_headers, meta={'item': item})
        else:
            yield item

    def review_page(self, response):
        item = response.meta['item']
        for review in response.xpath("//*[contains(@class,'item review-item')]"):
            item['Review Title'] = review.css('.review-title ::text').get('').strip()
            item['Review Content'] = review.css('.review-content ::text').get('').strip()
            item['Review By'] = review.css('.review-author .review-details-value ::text').get('').strip()
            item['Review On'] = review.css('.review-date .review-details-value ::text').get('').strip()
            yield item

        next_page = response.xpath("//a[contains(@class,'page')]/@href").get('').strip()
        if next_page:
            yield response.follow(url=next_page,callback=self.review_page, headers=self.review_headers, meta={'item': item})
