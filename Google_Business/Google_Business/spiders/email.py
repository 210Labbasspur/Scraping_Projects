import csv
import re
import datetime
from copy import deepcopy
import scrapy
import pandas as pd

class EmailSpider(scrapy.Spider):
    name = "email"
    custom_settings = {
        # 'FEED_URI': f'output/Google_Business -  {datetime.datetime.now().strftime("%d-%m-%Y")} (With Emails).csv',
        # 'FEED_FORMAT': 'csv',
        # 'FEED_EXPORT_ENCODING': 'utf-8',
        ########################################################################################################
        'FEED_URI': f'output/Google_Business - {datetime.datetime.now().strftime("%d-%m-%Y")} (With Emails).xlsx',
        'FEED_FORMAT': 'xlsx',
        'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
        'FEED_EXPORT_ENCODING': 'utf-8',
        ########################################################################################################

        'HTTPERROR_ALLOW_ALL': True,
    }

    start_urls = ['https://quotes.toscrape.com/']

    def is_valid_email(self, email):
        # Regular expression pattern for a basic email format
        pattern = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


    def parse(self, response):
        scraped_data_1 = []
        # for scraped_list in list(csv.DictReader(open('google_business_canada_dougraeca_final.csv', 'r'))):
        #     if scraped_list.get('Bussiness_Contact') not in scraped_data_1:
        #         scraped_data_1.append(scraped_list.get('Bussiness_Contact'))
        #         yield scraped_list

        # df = pd.read_excel('google_business_flanders_andre_media_without_email.xlsx')
        # data_dict = df.to_dict(orient='records')
        # keywords = [x for x in csv.DictReader(open('input/keywords.csv', encoding='Latin-1'))]
        # for p in list(csv.DictReader(open(f'output/Google_Business - {datetime.datetime.now().strftime("%d-%m-%Y")}.csv', 'r'))):
        # for p in list(csv.DictReader(open(f'output/Google_Business - {datetime.datetime.now().strftime("%d-%m-%Y")}.csv', 'r', encoding='Latin-1'))):
        # for p in list(csv.DictReader(open(f'output/Google_Business - 13-03-2025.csv', 'r', encoding='utf-8'))):
        for p in list(csv.DictReader(open(f'output/Google_Business - Los Angeles.csv', 'r', encoding='utf-8'))):
            item = deepcopy(p)
            item['Email'] = ''
            try:
                search_url = item.get('Bussiness_Website')
                # search_url = item.get('domain')
                if search_url:
                    if 'https' in search_url:
                        pass
                    else:
                        search_url = f'https://{search_url}'
                    yield scrapy.Request(
                        url=search_url,
                        callback=self.parse_emails,
                        errback=self.handle_error,
                        meta={'item': item},
                        dont_filter=True,
                    )
                else:
                    print('No Business_Website available in input file')
                    # yield item

            except:
                print('Cant visit website')
                # yield item

    def parse_emails(self, response):
        item = response.meta['item']
        final_emails = []
        try:
            # Improved regex for TLDs
            regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

            # Extract email addresses using the regex
            matches = re.findall(regex, response.text)

            if matches:
                extracted_emails = list(set(matches))  # Remove duplicates
                for email in extracted_emails:
                    if '.png' not in email and '.jpg' not in email and 'wix@' not in email and 'wixpress.' not in email and '@sentry.io' not in email:
                        final_emails.append(email)
                item['Email'] = final_emails
                print("Extracted emails : ", final_emails)
                yield item
            else:
                print("No email addresses found in the text.", item)
                yield item

        except re.error as e:
            print(f"Error: Invalid regex pattern - {e}")
            yield item
        ######## You can add more specific exception handling here

        # item['Emails'] = final_emails
        # yield item

    def handle_error(self, failure):        ####        #### https://www.olx.ro/d/oferta/schimb-apartament-IDiO4EZ.html
        meta = failure.request.meta
        item = meta.get('item')
        print('Couldnt visit the website :', item)
        yield item
