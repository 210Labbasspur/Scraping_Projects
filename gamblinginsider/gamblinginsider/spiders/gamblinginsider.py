import scrapy
import csv
import smtplib
import ssl
from email.mime.text import MIMEText

class gamblinginsider(scrapy.Spider):
    name = 'gamblinginsider'
    url = 'https://www.gamblinginsider.com/gambling-news/1'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'json-naming-strategy': 'camel',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
    }

    news_database = []
    URL_database = []
    def start_requests(self):
        keywords = []
        with open('input/keywords.csv', 'r', newline='', encoding='utf-8', errors='ignore') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                keyword = row['Keyword']
                if keyword:
                    keywords.append(keyword)

        with open("database/News_Database.csv", 'r', newline='', encoding='utf-8', errors='ignore') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                news_url = row['News_URL']
                if news_url:
                    self.URL_database.append(news_url)

        yield scrapy.Request(url=self.url, callback=self.parse, headers=self.headers, meta={'keywords':keywords})

    def parse(self, response):
        keywords = response.meta['keywords']
        for news in response.xpath("//*[contains(@class,'row mb-1 mb-3 g-0 bg-white box-content')]"):
            title = news.css('h3 a ::text').get('').strip()
            for keyword in keywords:
                if keyword.lower() in title.lower():
                    item = dict()
                    item['Keyword'] = keyword
                    item['Title'] = title.strip()
                    item['Date'] = news.css('span.date ::text').get('').strip()
                    news_url = news.css('h3 a ::attr(href)').get('').strip()
                    item['News_URL'] = news.css('h3 a ::attr(href)').get('').strip()

                    enter_in_database = True
                    for check_url in self.URL_database:
                        if check_url == news_url:
                            print('This News URL already exists in Database: ', news_url)
                            enter_in_database = False
                            break
                    if enter_in_database:
                        self.news_database.append(item)
                        with open("database/News_Database.csv", 'a', newline='', encoding='utf-8') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([news_url])
                            print('This new News URL have been stored inside the database ', news_url)

                    break

        next_page = response.xpath("//*[contains(@class,'page-item active')]/following-sibling::li[1]/a[1]/@href").get('').strip()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse, headers=self.headers, meta={'keywords': keywords})


    def closed(self, reason):
        news_data = self.news_database
        if news_data:
            smtp_port = 587
            smtp_server = "smtp.gmail.com"
            email_from = 'mike.ulrich.tv@gmail.com'
            email_to = 'syedhassanmujtabasherazi@gmail.com'
            pswd = 'fghijhvqeduqlvcw'       # email_app_passwords

            subject = 'Alert - ' + ', '.join(set(entry["Keyword"] for entry in news_data))
            body_text = "\n\n".join(f"{entry['Title']}\n{entry['News_URL']}" for entry in news_data)
            message = MIMEText(body_text)
            message['Subject'] = subject
            message['From'] = email_from
            message['To'] = email_to
            simple_email_content = ssl.create_default_context()
            try:
                print('Connecting to server...')
                TIE_server = smtplib.SMTP(smtp_server, smtp_port)
                TIE_server.starttls(context=simple_email_content)
                TIE_server.login(email_from, pswd)
                print('Connected to Server')
                print(f'Sending email to {email_to}')
                TIE_server.sendmail(email_from, email_to, message.as_string())
                print(f'Sending email from {email_from}')
            except Exception as e:
                print(e)
            finally:
                TIE_server.quit()
        else:
            print('Either all news are already forwarded on Email or no new News to forward')
