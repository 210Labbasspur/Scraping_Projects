import scrapy

class AllMenus(scrapy.Spider):
    # custom_settings = {'FEED_URI': 'All_Menus Record.csv',
    #                    'FEED_FORMAT': 'csv',
    #                    'FEED_EXPORT_ENCODING': 'utf-8-sig', }
    name = 'AllMenus'
    prefix = "https://www.allmenus.com"
    url = "https://www.allmenus.com/"
    headers = {
      'authority': 'www.allmenus.com',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
      'cache-control': 'max-age=0',
      # 'cookie': '_ga=GA1.2.1568185738.1702303645; _gid=GA1.2.1868128355.1702480467; _gat_UA-1071671-1=1',
      'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'none',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        for states in response.css('.state-list a'):#[:5]:
            state_url = self.prefix + states.css('::attr(href)').get('').strip()
            yield scrapy.Request(url=state_url, headers=self.headers, callback=self.states)

    def states(self, response):
        for rest in response.css('.s-col-xs-12:nth-child(3) .s-col-lg-3 a'):#[:1]:
            restaurant_url = self.prefix + rest.css('::attr(href)').get('').strip() + '-/'
            yield scrapy.Request(url=restaurant_url, headers=self.headers, callback=self.Restaurant)

    def Restaurant(self, response):
        for rest_list in response.css('.restaurant-list-item'):#[:5]:
            rest_url = self.prefix + rest_list.css('a::attr(href)').get('').strip()
            yield scrapy.Request(url=rest_url, headers=self.headers, callback=self.detail)

    def detail(self, response):
        item = dict()
        summary = response.css('.restaurant-summary ::text').getall()
        item['Name'] = summary[1].strip()
        item['Phone No'] = response.css('.phone a::text').get('').strip()
        item['Address'] = response.css('.menu-address ::text').get('').strip()
        item['Website'] = response.css('.menu-link::attr(href)').get('').strip()
        item['Cuisine'] = response.css('.cuisine a::text').getall()

        m_t = 0
        menu_t = response.css('.menu-item span::text, .h5 ::text').extract()
        if response.css('.menu-container'):
            menu_type = dict()
            for menu_con in response.css('.menu-container'):
                m_con = dict()
                for menu_cat in menu_con.css('.menu-category'):
                    m_cat = []
                    count = 1
                    for menu_i in menu_cat.css('.menu-items'):
                        menu = dict()
                        menu['menu_id'] = count
                        count += 1
                        menu['item'] = menu_i.css('.item-title::text').get('').strip()
                        menu['item-price'] = menu_i.css('.item-price::text').get('').strip()
                        menu['item-description'] = menu_i.css('.description ::text').get('').strip()
                        m_cat.append(menu)
                    m_con[menu_cat.css('.menu-section-title::text').get('').strip()] = m_cat
                menu_type[(menu_t[m_t]).strip()] = m_con
                m_t += 1
            item["JSON"] = menu_type

        item['Page URL'] = response.xpath("//link[contains(@rel,'canonical')]/@href").get('').strip()
        yield item
