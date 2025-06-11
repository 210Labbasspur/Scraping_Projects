import scrapy

class Erni(scrapy.Spider):
    name = 'Erni'
    prefix = "https://www.erni.com"
    url = "https://www.erni.com/en/products-and-solutions/electronic-connectors/m8-and-m12-connectors?tx_solr%5Bpage%5D=1"
    headers = {
        'authority': 'www.erni.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        # 'cookie': 'cookieconsent_optin_status=allow; avsite_optin_statistic=optin; avsite_optin_remarketing=optin; _ga=GA1.2.1133717487.1702367437; _gid=GA1.2.1549997742.1702367437',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    custom_settings = {'FEED_URI': 'Erni Record.csv',
                       'FEED_FORMAT': 'csv',
                       'FEED_EXPORT_ENCODING': 'utf-8-sig', }

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        for product in response.css('.teaser--withborder'):
            product_url = self.prefix + product.css('a::attr(href)').get('')
            yield scrapy.Request(url=product_url, headers=self.headers, callback=self.detail)
        next_page = response.css('.next ::attr(href)').get('').strip()
        if next_page:
            yield scrapy.Request(url=self.prefix + next_page, headers=self.headers, callback=self.parse)

    def detail(self, response):
        item = dict()
        item['Part-No'] = response.css('.kickertext::text').get('').strip()
        item['Product'] = response.css('.like-h3::text').get('').strip()
        item['Sub-Title'] = response.css('.subtitle::text').get('').strip()
        item['Image'] = self.prefix + response.css('.object--fit::attr(src)').get('').strip()

        item['Applications'] = response.xpath("//div[contains(text(),'Applications')]/following-sibling::div/text()").get('').strip()
        item['M8/M12 Application'] = response.xpath("//div[contains(text(),'M8/M12 Application')]/following-sibling::div/text()").get('').strip()
        item['Orientation'] = response.xpath("//div[contains(text(),'Orientation')]/following-sibling::div/text()").get('').strip()
        item['No. of Pins'] = response.xpath("//div[contains(text(),'No. of Pins')]/following-sibling::div/text()").get('').strip()
        item['Termination'] = response.xpath("//div[contains(text(),'Termination')]/following-sibling::div/text()").get('').strip()
        item['o-ring'] = response.xpath("//div[contains(text(),'o-ring')]/following-sibling::div/text()").get('').strip()
        item['Current Rating'] = response.xpath("//div[contains(text(),'Current Rating')]/following-sibling::div/text()").get('').strip()
        item['Air- and creepage distance'] = response.xpath("//div[contains(text(),'Air- and creepage distance')]/following-sibling::div/text()").get('').strip()
        item['Gender'] = response.xpath("//div[contains(text(),'Gender')]/following-sibling::div/text()").get('').strip()
        item['Coding'] = response.xpath("//div[contains(text(),'Coding')]/following-sibling::div/text()").get('').strip()
        item['Mating Cycles'] = response.xpath("//div[contains(text(),'Mating Cycles')]/following-sibling::div/text()").get('').strip()
        item['Standard'] = response.xpath("//div[contains(text(),'Standard')]/following-sibling::div/text()").get('').strip()
        item['Assembly Height'] = response.xpath("//div[contains(text(),'Assembly Height')]/following-sibling::div/text()").get('').strip()
        item['Max Operating Temp'] = response.xpath("//div[contains(text(),'Max Operating Temperature')]/following-sibling::div/text()").get('').strip()
        item['Configuration'] = response.xpath("//div[contains(text(),'Configuration')]/following-sibling::div/text()").get('').strip()
        item['Packaging'] = response.xpath("//div[contains(text(),'Packaging')]/following-sibling::div/text()").get('').strip()

        item['Cable Type'] = response.xpath("//div[contains(text(),'Cable Type')]/following-sibling::div/text()").get('').strip()
        item['Cable Length'] = response.xpath("//div[contains(text(),'Cable Length')]/following-sibling::div/text()").get('').strip()
        item['Connector left'] = response.xpath("//div[contains(text(),'Connector left')]/following-sibling::div/text()").get('').strip()
        item['Connector right'] = response.xpath("//div[contains(text(),'Connector right')]/following-sibling::div/text()").get('').strip()
        item['Connector right'] = response.xpath("//div[contains(text(),'Connector right')]/following-sibling::div/text()").get('').strip()
        item['Shield'] = response.xpath("//div[contains(text(),'Shield')]/following-sibling::div/text()").get('').strip()
        item['Anti Twist Protection'] = response.xpath("//div[contains(text(),'Anti Twist Protection')]/following-sibling::div/text()").get('').strip()
        item['Loaded Pins'] = response.xpath("//div[contains(text(),'Loaded Pins')]/following-sibling::div/text()").get('').strip()
        item['Material'] = response.xpath("//div[contains(text(),'Material')]/following-sibling::div/text()").get('').strip()
        item['Color'] = response.xpath("//div[contains(text(),'Color')]/following-sibling::div/text()").get('').strip()
        item['Data Rate'] = response.xpath("//div[contains(text(),'Data Rate')]/following-sibling::div/text()").get('').strip()
        item['Transmission Category'] = response.xpath("//div[contains(text(),'Transmission Category')]/following-sibling::div/text()").get('').strip()

        item['Drawing PDF'] = self.prefix + response.xpath("//span[contains(text(),'Drawing PDF')]/"
                                         "parent::div/following-sibling::div//a/@href").get('').strip()
        item['Drawing DXF'] = self.prefix + response.xpath("//span[contains(text(),'Drawing DXF')]/"
                                         "parent::div/following-sibling::div//a/@href").get('').strip()
        item['Model 3D'] = self.prefix + response.xpath("//span[contains(text(),'Model 3D')]/"
                                         "parent::div/following-sibling::div//a/@href").get('').strip()
        item['Catalog'] = self.prefix + response.xpath("//span[contains(text(),'Catalog')]/"
                                         "parent::div/following-sibling::div//a/@href").get('').strip()

        item['Product URL'] = response.xpath("//link[contains(@rel,'canonical')]/@href").get('').strip()

        yield item
