############            email_phone

import csv
import re
import datetime
from copy import deepcopy
import scrapy
import pandas as pd

class email_phone(scrapy.Spider):
    name = "email_phone"
    custom_settings = {
        # 'FEED_URI': f'output/Google_Business -  {datetime.datetime.now().strftime("%d-%m-%Y")} (With Emails).csv',
        # 'FEED_FORMAT': 'csv',
        # 'FEED_EXPORT_ENCODING': 'utf-8',
        ########################################################################################################
        'FEED_URI': f'output/With Email_&_PhoneNo - {datetime.datetime.now().strftime("%d-%m-%Y")}.xlsx',
        'FEED_FORMAT': 'xlsx',
        'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
        'FEED_EXPORT_ENCODING': 'utf-8',
        ########################################################################################################
        'HTTPERROR_ALLOW_ALL': True,
    }

    start_urls = ['https://quotes.toscrape.com/']
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sx-platform': 'web-next',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'x-client-type': 'web',
    }

    def is_valid_email(self, email):
        # Regular expression pattern for a basic email format
        pattern = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def parse(self, response):
        scraped_data_1 = []
        for p in list(csv.DictReader(open(f'input/domain3_5may_net_1 (1).csv', 'r', encoding='utf-8'))):
            item = deepcopy(p)
            item['Email(s)'], item['Phone(s)'] = '',''
            try:
                # search_url = item.get('Bussiness_Website')
                search_url = item.get('domain')
                if search_url:
                    if 'https' in search_url:
                        pass
                    else:
                        search_url = f'https://{search_url}'
                    yield scrapy.Request(
                        url=search_url,
                        headers=self.headers,
                        callback=self.parse_emails,
                        errback=self.handle_error,
                        meta={'item': item},
                        dont_filter=True,
                    )
                else:
                    print('No Business_Website available in input file')
                    yield item

            except:
                print('Cant visit website')
                yield item

    def parse_emails(self, response):
        item = response.meta['item']
        final_emails = []
        final_phones = []
        try:
            # Improved regex for emails
            email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
            # Regex for phone numbers (supports formats like: 123-456-7890, (123) 456-7890, +61 412 345 678, etc.)
            phone_regex = r"\(\d{3}\)\s\d{3}-\d{4}"

            # Extract email addresses
            email_matches = re.findall(email_regex, response.text)
            if email_matches:
                extracted_emails = list(set(email_matches))  # Remove duplicates
                for email in extracted_emails:
                    if all(x not in email for x in ['.png', '.jpg', 'wix@', 'wixpress.', '@sentry.io']):
                        final_emails.append(email)

            # Extract phones
            phone_matches = re.findall(phone_regex, response.text)
            if phone_matches:
                final_phones = list(set(phone_matches))  # remove duplicates

            item['Email(s)'] = final_emails
            item['Phone(s)'] = final_phones
            # print("Extracted emails:", final_emails)
            # print("Extracted phone numbers:", final_phones)
            yield item

        except re.error as e:
            print(f"Error: Invalid regex pattern - {e}")
            yield item

    def handle_error(self, failure):
        meta = failure.request.meta
        item = meta.get('item')
        print('Couldnt visit the website :', item)
        yield item
