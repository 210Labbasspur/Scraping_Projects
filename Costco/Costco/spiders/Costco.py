import re
import json
import scrapy
import gspread
import datetime


class Costco(scrapy.Spider):
    name = 'Costco'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }

    custom_settings = {
        'FEED_URI': f'output/Costco - {datetime.datetime.now().strftime("%d-%m-%Y")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',

        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
            "scrapy_poet.InjectionMiddleware": 543,
        },
        "REQUEST_FINGERPRINTER_CLASS": "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ZYTE_API_KEY": "f1a2c59640d149368709f4d367049039",  # Please enter your API Key here
        "ZYTE_API_TRANSPARENT_MODE": True,
        # "ZYTE_API_EXPERIMENTAL_COOKIES_ENABLED": True,
    }

    handle_httpstatus_list = [400, 401, 403, 404, 500, 502, 503, 504, 520]
    handle_httpstatus_all = True

    def start_requests(self):
        google_sheet_link = 'https://docs.google.com/spreadsheets/d/1Av8PdgXnakDiF8ss7qGVs0blPIi1uOK_YUU2ikq20rM/edit?gid=0#gid=0'
        gc = gspread.service_account('creds.json')
        spreadsheet = gc.open("Costco_Sheet")
        worksheet = spreadsheet.get_worksheet(0)
        # Assuming the "Item No" column is the first column (A)
        item_no_column = worksheet.col_values(1)  # 1 means column A
        item_nos = item_no_column[1:]  # Skip the first element (header)
        for item_no in item_nos:
            detail_url = f'https://www.costco.com/.product.{item_no}.html'
            yield scrapy.Request(detail_url, callback=self.parse, headers=self.headers,
                                 meta={'item_no': item_no, 'browserHtml': True},  dont_filter=True,)


    def parse(self, response):
        item_no = response.meta['item_no']
        item = dict()

        item['Item No'] = item_no
        if response.xpath("//*[contains(@automation-id,'productName')]/text()").get('').strip():
            item['Availability'] = 'Available'
            item['Item Title'] = response.xpath("//*[contains(@automation-id,'productName')]/text()").get('').strip() or 'Not Found'

            match = re.search(r"priceMin\s*:\s*'(\d+(\.\d+)?)'", response.text)
            if match:
                item['Item Price'] = match.group(1)
            else:
                item['Item Price'] = 'Not Found'

            item['Item Images'] = 'Not Found'
            images_list = []
            images_tag_text = response.xpath("//*[contains(text(),'reactObj.imageViewer')]/text()").get('').strip()
            images_tag_text = images_tag_text[:-1].replace('reactObj.imageViewer = ','')
            fixed_images_tag_text = (images_tag_text.replace("'", '"').replace('mainImageSize :','"mainImageSize":').replace('thumbImageSize:','"thumbImageSize":').replace(
                'zoomSize:', '"zoomSize":').replace("itemDetail:", '"itemDetail":').replace("swatch:", '"swatch":').replace(
                "swatchImage:", '"swatchImage":').replace("status:", '"status":').replace("imageDetails:",'"imageDetails":').replace(
                "fileName:", '"fileName":').replace("cdn_url:", '"cdn_url":').replace("priority:", '"priority":')
                .replace("language:", '"language":').replace("optionList :", '"optionList":').replace("productID:", '"productID":')
                .replace("businessUnit:", '"businessUnit":').replace("productDefaultImageUrl:", '"productDefaultImageUrl":')
                .replace("videoItem:", '"videoItem":').replace("role:", '"role":').replace("options:", '"options":')
                .replace("tracks:", '"tracks":').replace("kind:", '"kind":').replace("srclang:", '"srclang":')
                .replace("label:", '"label":').replace("src:", '"src":').replace("sources:", '"sources":')
                .replace("type:", '"type":').replace("poster:", '"poster":').replace("srclang:", '"srclang":')
                .replace("itemDetailsList:", '"itemDetailsList":').replace("itemId:", '"itemId":'))

            images_json = json.loads(fixed_images_tag_text)
            if images_json:
                for check in images_json.get('itemDetailsList',[]):
                    if check.get('itemDetail',{}).get('itemId','') == item_no:
                        for image in check.get('itemDetail',{}).get('imageDetails',[]):
                            images_list.append(image.get('cdn_url'))
            if images_list:
                item['Item Images'] = ', '.join(e for e in images_list)

            product_details = response.xpath("//*[contains(text(),'Product Details')]/parent::div[1]")
            product_details = product_details.css("::text").getall()
            if product_details:
                item['Product Details'] = ' '.join(e.strip().replace('[ProductDetailsESpot_Tab1]','').replace('\xa0','') for e in product_details)
            else:
                item['Product Details'] = 'Not Found'

            item['Item URL'] = response.url
            yield item


        elif 'return proxied.apply(this, [].slice.call(arguments));' in response.text:  #   We need to request again
            item['Item URL'] = response.url
            detail_url = response.url
            yield scrapy.Request(detail_url, callback=self.parse, headers=self.headers,
                                 meta={'item_no': item_no, 'browserHtml': True}, dont_filter=True,)


        elif response.status != 200:
            print(f"Received {response.status} from {response.url}")
            if 'costcobusinessdelivery' in response.url:
                item = dict()
                item['Item No'], item['Availability'] = item_no, 'Not Available'
                item['Item Title'], item['Item Price'], item['Item Images'], item['Product Details'] = '', '', '', ''
                item['Item URL'] = response.url
                yield item
            else:
                detail_url = response.url.replace('costco', 'costcobusinessdelivery')
                print(f'Lets go to {detail_url}')
                yield scrapy.Request(detail_url, callback=self.parse, headers=self.headers,
                                     meta={'item_no': item_no, 'browserHtml': True}, dont_filter=True)


        else:
            item['Availability'] = 'Not Available'
            item['Item Title'], item['Item Price'], item['Item Images'], item['Product Details'] = '', '', '', ''
            item['Item URL'] = response.url
            yield item
