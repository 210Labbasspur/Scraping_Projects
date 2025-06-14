#################           finviz_old

import csv
import os
import re
from collections import OrderedDict
from datetime import datetime
import scrapy
from scrapy import Spider, Request


class FinvizSpider(Spider):
    name = 'finviz'
    base_url = 'https://finviz.com/'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }

    custom_settings = {
        'CONCURRENT_REQUESTS': 4,
        'DOWNLOAD_DELAY': 1,
        'FEEDS': {
            f'output/Finviz {datetime.now().strftime("%Y-%m-%d %H-%M")}.csv': {
                'format': 'csv',
            },
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_urls = self.read_input_urls()
        self.last_scrapped_items = {row['URL']: row for row in self.read_previously_scrapped_items()}
        d=1

    def start_requests(self):
    #     url = 'https://finviz.com/login_submit.ashx'
    #     data = {'email': 'imexinco@gmail.com', 'password': 'Stallion', 'remember': 'true', }
    #     yield scrapy.FormRequest(url, method='POST', formdata=data, headers=self.headers, callback=self.login_parse)
    #
    # def login_parse(self, response):
    #     print('self.base_url is : ', self.base_url)
    #     yield Request(url=self.base_url, headers=self.headers, callback=self.parse, dont_filter=True)
    #
    # def parse(self, response, **kwargs):
        for url in self.input_urls:
            print('Lets scrape this url : ', url)
            yield Request(url=url, headers=self.headers, callback=self.parse_listings)


    def parse_listings(self, response):
        listing_table = response.css('[class="styled-row is-bordered is-rounded is-hoverable is-striped has-color-text"]')

        for row in listing_table:
            url = row.css('.tab-link ::attr(href)').get('')
            item = OrderedDict()
            item['Ticker'] = row.css('.tab-link ::text').get('')
            item['Company'] = row.css('td:nth-child(3) ::text').get('')
            item['Sector'] = row.css('td:nth-child(4) ::text').get('')
            item['Industry'] = row.css('td:nth-child(5) ::text').get('')
            item['Country'] = row.css('td:nth-child(6) ::text').get('')

            item['Price'] = row.css('td:nth-child(9) ::text').get('').strip()
            item['Change'] = row.css('td:nth-child(10) ::text').get('').strip()
            item['Volume'] = row.css('td:nth-child(11) ::text').get('').strip().replace(',','')
            price = row.css('td:nth-child(9) ::text').get('').strip()
            volume = row.css('td:nth-child(11) ::text').get('').strip().replace(',','')
            price_volume = float(price) * float(volume)
            item['Price X Volume'] = round(price_volume, 3)

            item['URL'] = response.urljoin(url)
            print('Item is : ',item)
            yield Request(url=response.urljoin(url), headers=self.headers, callback=self.parse_volume, meta={'item': item})

        next_page_url = response.css('#screener_pagination .is-next::attr(href)').get('')
        if next_page_url:
            print('Next Page URL is : ', next_page_url)
            yield Request(url=response.urljoin(next_page_url), headers=self.headers, callback=self.parse_listings)


    def parse_volume(self, response):
        item = response.meta.get('item')
        current_rel_volume = response.css('td:contains("Rel Volume") + td ::text').get('0')
        # current_rel_volume = response.css('td:contains("Rel Volume") + td ::text').get('0')
        percentage_change = ''
        current_price_volume = item['Price X Volume']
        price_volume_percentage_change = ''

        previous_item = self.last_scrapped_items.get(item['URL'])
        if previous_item:
            last_rel_volume = previous_item['Rel Volume']
            percentage_change = self.percentage_change(old_value=float(last_rel_volume), new_value=float(current_rel_volume))
            d=1

            last_price_volume = previous_item['Price X Volume']
            price_volume_percentage_change = self.percentage_change(old_value=float(last_price_volume), new_value=float(current_price_volume))
            d=1

        item['Rel Volume'] = current_rel_volume
        # item['Avg Volume'] = response.xpath("//*[contains(text(),'Avg Volume')]/following-sibling::td[1]//text()").get('').strip()

        # item['Market Cap'] = response.xpath("//*[contains(text(),'Market Cap')]/following-sibling::td[1]//text()").get('').strip()
        # item['Income'] = response.xpath("//*[contains(text(),'Income')]/following-sibling::td[1]//text()").get('').strip()
        # item['Shs Outstand'] = response.xpath("//*[contains(text(),'Shs Outstand')]/following-sibling::td[1]//text()").get('').strip()
        # item['Shs Float'] = response.xpath("//*[contains(text(),'Shs Float')]/following-sibling::td[1]//text()").get('').strip()
        # item['Insider Own'] = response.xpath("//*[contains(text(),'Insider Own')]/following-sibling::td[1]//text()").get('').strip()
        # item['Short Float'] = response.xpath("//*[contains(text(),'Short Float')]/following-sibling::td[1]//text()").get('').strip()
        # item['Short Ratio'] = response.xpath("//*[contains(text(),'Short Ratio')]/following-sibling::td[1]//text()").get('').strip()
        fields = ['Insider Own', 'Short Float', 'Short Ratio', 'Trades', 'Avg Volume',
                    'Shs Float', 'Shs Outstand','Income', 'Market Cap',
                 # 'xxxxxxxxxxxx', 'xxxxxxxxxxxx', 'xxxxxxxxxxxx', 'xxxxxxxxxxxx',
                 ]
        for field in fields:
            if response.xpath(f"//*[contains(text(),'{field}')]/following-sibling::td[1]//text()").get('').strip():
                item[field] = response.xpath(f"//*[contains(text(),'{field}')]/following-sibling::td[1]//text()").get('').strip()
            else:
                item[field] = response.xpath(f"//*[contains(text(),'{field}')]/parent::*/following-sibling::td[1]//text()").get('').strip()


        if response.xpath("//*[contains(text(),'Short Interest')]/following-sibling::td[1]//text()").get('').strip():
            item['Short Interest'] = response.xpath("//*[contains(text(),'Short Interest')]/following-sibling::td[1]//text()").get('').strip()
        else:
            item['Short Interest'] = response.xpath("//*[contains(text(),'Short Interest')]/parent::*/following-sibling::td[1]//text()").get('').strip()

        # item['Trades'] = response.xpath("//*[contains(text(),'Trades')]/following-sibling::td[1]//text()").get('').strip()

        shortinterest = item['Short Interest'].replace('K','').replace('M','').replace('B','')
        print(f"Price: {item['Price']}, Short Interest: {item['Short Interest']} || and filtered interest :{shortinterest}")
        shortinterest_price = float(item['Price']) * float(shortinterest)
        item['Short Interest  X Price'] = round(shortinterest_price, 3)
        # item['xxxxxxxxxxxx'] = response.xpath("//*[contains(text(),'xxxxxxxxxxxx')]/following-sibling::td[1]/b/text()").get('').strip()
        # item['xxxxxxxxxxxx'] = response.xpath("//*[contains(text(),'xxxxxxxxxxxx')]/following-sibling::td[1]/b/text()").get('').strip()

        item['RSI'] = response.xpath("//*[contains(text(),'RSI')]/following-sibling::td[1]//text()").get('').strip()
        ####    Need to understand New News and make a logic for it
        # item['New News'] = response.xpath("//*[contains(text(),'xxxxxxxxxxxx')]/following-sibling::td[1]/b/text()").get('').strip()

        item['Percentage Change'] = percentage_change
        item['Percentage Change (Price X Volume)'] = price_volume_percentage_change

        item['Todays News'] = ''
        todays_news = []
        for news in response.xpath("//*[contains(@class,'cursor-pointer has-label')]"):
            date_str = news.xpath(".//td[1]/text()").get('').strip()
            time_pattern = re.compile(r'^\d{1,2}:\d{2}(AM|PM)$')

            print("Date String is : ", date_str)
            if 'Today' in date_str:
                print('Hurray, We have found date string ', date_str)
                news_link = news.css(".tab-link-news ::attr(href)").get('').strip()
                todays_news.append(news_link)
            elif time_pattern.match(date_str):
                print('Hurray, We have found date string ', date_str)
                news_link = news.css(".tab-link-news ::attr(href)").get('').strip()
                todays_news.append(news_link)
            else:       # This date is not today, stop processing
                break

        item['Todays News'] = ', '.join(e.strip() for e in todays_news)


        item['URL'] = response.url
        yield item



    def percentage_change(self, old_value, new_value):
        try:
            change = ((new_value - old_value) / old_value) * 100
            return round(change, 2)
        except ZeroDivisionError:
            return ""

    def read_previously_scrapped_items(self):
        try:
            latest_input_file = self.get_latest_file_path()
            with open(latest_input_file, mode='r', encoding='utf-8') as csv_file:
                return list(csv.DictReader(csv_file))
        except:
            return []

    def get_latest_file_path(self):
        folder_path = 'output'
        files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
        latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))

        return os.path.join(folder_path, latest_file)

    def read_input_urls(self):
        with open('input/urls.txt', mode='r', encoding='utf-8') as txt_file:
            return [line.strip() for line in txt_file.readlines() if line.strip()]

