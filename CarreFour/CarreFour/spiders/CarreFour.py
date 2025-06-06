import scrapy
import csv
import json
import mysql.connector


class CarreFour(scrapy.Spider):
    name = 'CarreFour'
    url = 'https://www.carrefour.fr/promotions?noRedirect=1&page={}'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
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
        "ZYTE_API_KEY": "ENTER_YOUR_KEY_HERE",  # Please enter your API Key here
        "ZYTE_API_TRANSPARENT_MODE": True,
        "ZYTE_API_EXPERIMENTAL_COOKIES_ENABLED": True,
    }

    def start_requests(self):
        category_urls = []
        with open("input/CarreFour Input URLs.csv", 'r', newline='', encoding='utf-8', errors='ignore') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                url = row['Category_URL']
                if url:
                    category_urls.append(url)

        for category_url in category_urls:
            page_no = 1
            yield scrapy.Request(category_url, callback=self.parse, headers=self.headers, meta={'page_no': page_no})

    def parse(self, response):
        page_no = response.meta['page_no']
        data = json.loads(response.text)
        if data:
            for product in data.get('data',[]):
                code = product.get('attributes',{}).get('ean','')
                offerServiceId = product.get('attributes',{}).get('offerServiceId','')

                item = dict()
                item['Product Name'] = product.get('attributes',{}).get('title','')
                item['Product Image'] = ''
                if product.get('attributes',{}).get('images',{}).get('paths',[]):
                    item['Product Image'] = product.get('attributes',{}).get('images',{}).get('paths',[])[0]

                offer = product.get('attributes',{}).get('offers',{}).get(f'{code}',{}).get(f'{offerServiceId}',{})
                item['Price'], item['Price per Unit'], item['Red Flag Text'] = '', '', ''
                if offer:
                    item['Price'] = offer.get('attributes',{}).get('price',{}).get('price')
                    item['Price per Unit'] = offer.get('attributes',{}).get('price',{}).get('perUnitLabel')
                    item['Red Flag Text'] = offer.get('attributes',{}).get('promotion',{}).get('label','')

                categories = []
                for category in product.get('attributes',{}).get('categories',[]):
                    categories.append(category.get('label',''))
                item['Category'] = ', '.join(category for category in categories)

                slug = product.get('attributes',{}).get('slug','')
                detail_url = f'https://www.carrefour.fr/p/{slug}-{code}'
                item['Detail URL'] = detail_url


                '''     Saving Data Inside the Database     '''
                db_name = 'CarreFour_Database'
                table_name = 'CarreFour_Record'
                field_names = item.keys()                                               # Get the keys from 'item'
                db_config = {'user': 'root', 'host': 'localhost', 'password': '', }     # Connect to MySQL server

                db = mysql.connector.connect(**db_config)
                cursor = db.cursor()

                # Step 1: Check if the database exists
                cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
                database_exists = cursor.fetchone()

                if not database_exists:
                    # Step 2: Create a new database
                    cursor.execute(f"CREATE DATABASE {db_name}")
                    cursor.execute(f"USE {db_name}")
                    ## Step 3: Create a new table
                    create_table_query = f"CREATE TABLE {table_name} ({','.join(f'`{field}` TEXT' for field in field_names)})"
                    cursor.execute(create_table_query)
                else:
                    cursor.execute(f"USE {db_name}")                    # Step 2: Use the existing database
                    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")  # Step 3: Check if the table exists
                    table_exists = cursor.fetchone()
                    if not table_exists:                                # Step 4: Create a new table
                        create_table_query = f"CREATE TABLE {table_name} ({','.join(f'`{field}` TEXT' for field in field_names)})"
                        cursor.execute(create_table_query)

                # Step 4: Insert values into the corresponding columns
                insert_data_query = f"INSERT INTO {table_name} ({','.join(f'`{field}`' for field in field_names)}) VALUES ({','.join(['%s'] * len(field_names))})"
                insert_data_values = tuple(item[field] for field in field_names)

                cursor.execute(insert_data_query, insert_data_values)
                db.commit()
                cursor.close()
                db.close()



            total_pages = data.get('meta',{}).get('totalPage')
            print('Total Pages are :', total_pages)
            if page_no < total_pages:
                next_page_url = data.get('links',{}).get('next','')
                yield response.follow(next_page_url, callback=self.parse, headers=self.headers, meta={'page_no': page_no + 1})

