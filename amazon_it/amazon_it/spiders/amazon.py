import glob
import re

import openpyxl
from scrapy import Spider, Request


class AmazonSpider(Spider):
    name = 'amazon'

    base_url = 'https://www.amazon.it/'

    custom_settings = {
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_DELAY': 1,

        'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter',},

        'RETRY_TIMES': 15,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404, 408],
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 3,
        'AUTOTHROTTLE_MAX_DELAY': 7,

        'FEEDS': {
            f'output/Amazon Products by EAN with description images2.xlsx': {
                'format': 'xlsx',
                # 'overwrite': True
            },
        }
    }

    headers = {
        'authority': 'www.amazon.it',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'session-id=261-6757973-4005923; session-id-time=2082787201l; i18n-prefs=EUR; ubid-acbbe=262-6081462-1277331; csm-hit=tb:s-72X6THS2R9XDWNT58PNZ|1706872459107&t:1706872459907&adb:adblk_no; session-token=xN7wHxADYgVAKd9pOI6xcsdqAAVJAGvHOzJ4DIIO4u0qvuVLt/j/uBYFfeTfLUnHbmYgZz/WEcLF2YtpYjiQTgeBS8t+sfcwsqAsV7hSzi1JUdMkbXtkn1GRVlPx1D6E+dYwYn0TzrjRdXkH8hFtC6/BRgC+F1iO1xxK4/KbyHavoM+CPv92R531J7ksqTJSk16V92BW1kAHRiZPUtZa0JcpA4rst7ziTXTsUq4vRUAFK2Z0uUt3VuxcRUeCDE9dGSwAc8LNpyOuJurqbsNJEBmSpym5x+mKJ8wEG5wL0KBrzrip2Swivuq7E3+94veR1QlzSKqLuEa6PscHJKJ0Clh0VJmBML7iqjkHzQKskZM=',
        'device-memory': '8',
        'downlink': '1.35',
        'dpr': '1.25',
        'ect': '3g',
        'rtt': '400',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1.25',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-viewport-width': '1536',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'viewport-width': '1536',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.seen_asins = [row['ASIN'] for row in self.get_sku_and_price_from_file()]
        self.input_rows = self.read_asins_from_csv()
        self.scraped_items = []
        self.items_returned = False

    def start_requests(self):
        yield Request(url=self.base_url, headers=self.headers)

    def parse(self, response, **kwargs):
        for asin in self.input_rows:
            if not asin:
                continue

            if asin in self.seen_asins:
                continue

            url = f'https://www.amazon.it/dp/{asin}'

            yield Request(url=url, headers=self.headers, callback=self.parse_detail)

    def parse_detail(self, response):
        # product_variants_asins = response.css('#variation_color_name li[data-defaultasin] ::attr(data-defaultasin)').getall()
        # variant_request = response.meta.get('variant_request', False)
        # if not variant_request and product_variants_asins:
        #     for v_asin in product_variants_asins:
        #         url = f'https://www.amazon.it/dp/{v_asin}'
        #
        #         yield Request(url, headers=self.headers, callback=self.parse_detail, meta={'variant_request': True}, dont_filter=True)

        short_technical_detail = '\n'.join([':'.join(row.css('.a-size-base ::text').getall()).strip() for row in response.css('.a-normal.a-spacing-micro tr')]) or ''
        about_product = '\n'.join([li.css('::text').get('').strip() for li in response.css('.a-unordered-list.a-spacing-mini li')]).strip()
        technical_detail = '\n'.join([':'.join(row.css('.a-size-base ::text').getall()).strip() for row in response.css('#technicalSpecifications_section_1 tr')])

        description = f"{short_technical_detail} {about_product} {technical_detail}".strip()

        try:
            asin = re.search(r'/dp/(\w+)', response.url).group(1)
        except:
            return

        amazon = ''.join([a for a in response.url.split('/') if 'www.amazon' in a])
        images = self.get_images(response)
        description_images = list(set(response.css('#aplus ::attr(src)').getall()))
        main_description = response.css('#productDescription ::text').getall()

        item = dict()
        item['ASIN'] = re.search(r'/dp/(\w+)', response.url).group(1)
        item['Title'] = response.css('#productTitle ::text').get('').strip()
        item['Images'] = ', '.join(images)
        item['Description Images'] = ', '.join(description_images)
        item['image_urls'] = description_images
        item['Description'] = ' '.join(main_description).strip()
        item['Product Details'] = '\n'.join([x.strip() for x in response.css('#productFactsDesktopExpander ::text').getall() if x.strip()]) or description
        item['URL'] = f'{amazon}/dp/{asin}'

        self.scraped_items.append(item)

        yield item

    def read_asins_from_csv(self):
        filename = glob.glob('input/*.txt')[0]
        with open(filename, mode='r', encoding='utf-8') as txt_file:
            return [line.strip() for line in txt_file.readlines() if line.strip()]

    def get_images(self, response):
        image_urls = []
        images = response.css('.a-nostyle.a-button-list.a-vertical img::attr(src)').getall() or response.css('.a-spacing-small.item img::attr(src)').getall()

        for index, image_url in enumerate(images):
           image_urls.append(image_url.split('._')[0] + '._AC_SX569_.jpg')

        return image_urls

    def get_sku_and_price_from_file(self):
        workbook = openpyxl.load_workbook('output/Amazon Products by EAN with description images.xlsx')

        sheet = workbook.worksheets[0]

        data = []

        column_names = [cell.value for cell in sheet[1]]

        # Iterate over rows in the sheet, starting from the second row
        for row in sheet.iter_rows(values_only=True, min_row=2):
            # Create a dictionary by combining column names and row values
            row_dict = {column_names[i]: row[i] for i in range(len(column_names))}
            data.append(row_dict)

        workbook.close()

        return data

