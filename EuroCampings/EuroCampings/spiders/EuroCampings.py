import json
import scrapy
import datetime
from scrapy import Selector


class EuroCampings(scrapy.Spider):
    name = 'EuroCampings'
    url = 'https://search-api.acsi.eu/v1/next-search/campsites/?website=eurocampings&languageCode=en&filter[]=flex-days_flex-days-2:2&filter[]=travel-party_adults:2&sort=sort_recommended&offset={}&limit=500&view=list'
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    custom_settings = {
        'FEEDS': {
            f'Output/EuroCampings - {datetime.datetime.now().strftime("%d-%m-%Y")}.json':
            {
                'format': 'json',
                'overwrite': True,
                'encoding': 'utf-8',
            },
        }
    }

    def start_requests(self):
        offset = 0
        yield scrapy.Request(self.url.format(offset), callback=self.parse, headers=self.headers, meta={'offset':offset})


    def parse(self, response):
        data = json.loads(response.text)
        offset = response.meta['offset']
        for campsite in data.get('campsites',{}).get('results',[]):
            offset += 1
            item = dict()
            item['ID'] = campsite.get('id','')
            item['Name'] = campsite.get('name','')
            item['No_of_Reviews'] = campsite.get('reviews',{}).get('total')
            item['Rating'] = campsite.get('reviews',{}).get('score')
            item['Country'] = campsite.get('geo', {}).get('location', [None])[0]
            item['Longitude'] = campsite.get('geo',{}).get('longitude')
            item['Latitude'] = campsite.get('geo',{}).get('latitude')
            item['Address'] = ''
            item['Description'] = ' '.join(Selector(text=campsite.get('description', '')).css('::text').getall()).strip() \
                if campsite.get('description', '') else ''
            item['Images'] = campsite.get('images',[])

            detail_url = campsite.get('url','')
            yield scrapy.Request(detail_url, callback=self.detail_parse, headers=self.headers, meta={'item': item})

        total_campsite = data.get('campsites',{}).get('total')
        if offset < total_campsite:
            yield scrapy.Request(self.url.format(offset), callback=self.parse, headers=self.headers, meta={'offset': offset})


    def detail_parse(self, response):
        item = response.meta['item']
        item['Contact'] = response.css('.media__body a ::text').get('').strip()
        item['Email'] = response.xpath("//*[contains(@data-gtm,'campsite-tab-addressroute-websitetextlink2')]/text()").get('').strip()
        address = response.xpath("//*[contains(@itemprop,'address')]")
        item['Address'] = ' '.join(e.strip() for e in address.css("::text").getall())
        item['Description'] = item.get('Description') or ' '.join(e.strip() for e in response.css('.campsite-description ::text').getall())

        #####  Facilities
        item['Guide Price 1'] = response.xpath("//*[contains(text(),'Guide price 1')]/following-sibling::dd[1]/text()").get('').strip()
        item['Guide Price 2'] = response.xpath("//*[contains(text(),'Guide price 2')]/following-sibling::dd[1]/text()").get('').strip()
        opening_period = response.xpath("//*[contains(text(),'Period of opening')]/following-sibling::dd[1]")
        item['Period of Opening'] = ''.join(e.strip() for e in opening_period.css('::text').getall())
        item['Area'] = response.xpath("//*[contains(text(),'Area')]/following-sibling::dd[1]/text()").get('').strip()
        item['Altitude'] = response.xpath("//*[contains(text(),'Altitude')]/following-sibling::dd[1]/text()").get('').strip()
        touring_pitches = response.xpath("//*[contains(text(),'Number of touring pitches')]/following-sibling::dd[1]")
        item['Number of Touring Pitches'] = ''.join(e.strip() for e in touring_pitches.css('::text').getall())
        item['Number of Camper Pitches'] = response.xpath("//*[contains(text(),'Number of camper pitches')]/following-sibling::dd[1]/text()").get('').strip()
        item['Number of Permanent Pitches'] = response.xpath("//*[contains(text(),'Number of permanent pitches')]/following-sibling::dd[1]/text()").get('').strip()
        item['Number of Accommodation'] = response.xpath("//*[contains(text(),'Number of accommodation')]/following-sibling::dd[1]/text()").get('').strip()
        item['Campsite Suitable for Disabled Persons'] = response.xpath("//*[contains(text(),'Campsite suitable for disabled persons')]/following-sibling::dd[1]/text()").get('').strip()

        internet = response.xpath("//span[contains(text(),'Internet')]/parent::summary[1]/following-sibling::ul[1]")
        item['Internet'] = ', '.join(filter(None, [i.strip() for i in internet.css('::text').getall()]))

        at_reception = response.xpath("//span[contains(text(),'At the reception')]/parent::summary[1]/following-sibling::ul[1]")
        item['At the Reception'] = ', '.join(filter(None, [i.strip() for i in at_reception.css('::text').getall()]))

        pitch_amenities = response.xpath("//span[contains(text(),'Pitch amenities')]/parent::summary[1]/following-sibling::ul[1]")
        item['Pitch Amenities'] = ', '.join(filter(None, [i.strip() for i in pitch_amenities.css('::text').getall()]))

        campsite_rules = response.xpath("//span[contains(text(),'Campsite rules')]/parent::summary[1]/following-sibling::ul[1]")
        item['Campsite Rules'] = ', '.join(filter(None, [i.strip() for i in campsite_rules.css('::text').getall()]))

        dogs = response.xpath("//span[contains(text(),'Dogs')]/parent::summary[1]/following-sibling::ul[1]")
        item['Dogs'] = ', '.join(filter(None, [i.strip() for i in dogs.css('::text').getall()]))

        toilet_facilities = response.xpath("//span[contains(text(),'Toilet facilities')]/parent::summary[1]/following-sibling::ul[1]")
        item['Toilet Facilities'] = ', '.join(filter(None, [i.strip() for i in toilet_facilities.css('::text').getall()]))

        ground_vegetation = response.xpath("//span[contains(text(),'Ground and vegetation')]/parent::summary[1]/following-sibling::ul[1]")
        item['Ground and Vegetation'] = ', '.join(filter(None, [i.strip() for i in ground_vegetation.css('::text').getall()]))

        washing_cooking = response.xpath("//span[contains(text(),'Washing, washing-up, cooking')]/parent::summary[1]/following-sibling::ul[1]")
        item['Washing, Washing-up, Cooking'] = ', '.join(filter(None, [i.strip() for i in washing_cooking.css('::text').getall()]))

        food_groceries = response.xpath("//span[contains(text(),'Food, drink and groceries')]/parent::summary[1]/following-sibling::ul[1]")
        item['Food, Drink and Groceries'] = ', '.join(filter(None, [i.strip() for i in food_groceries.css('::text').getall()]))

        rental_accommodations = response.xpath("//span[contains(text(),'Rental accommodations')]/parent::summary[1]/following-sibling::ul[1]")
        item['Rental Accommodations'] = ', '.join(filter(None, [i.strip() for i in rental_accommodations.css('::text').getall()]))

        available_campsite = response.xpath("//span[contains(text(),'Available to hire at the campsite')]/parent::summary[1]/following-sibling::ul[1]")
        item['Available to Hire at the Campsite'] = ', '.join(filter(None, [i.strip() for i in available_campsite.css('::text').getall()]))

        swimming = response.xpath("//span[contains(text(),'Swimming')]/parent::summary[1]/following-sibling::ul[1]")
        item['Swimming'] = ', '.join(filter(None, [i.strip() for i in swimming.css('::text').getall()]))

        wellness = response.xpath("//span[contains(text(),'Wellness')]/parent::summary[1]/following-sibling::ul[1]")
        item['Wellness'] = ', '.join(filter(None, [i.strip() for i in wellness.css('::text').getall()]))

        beach = response.xpath("//span[contains(text(),'Beach')]/parent::summary[1]/following-sibling::ul[1]")
        item['Beach'] = ', '.join(filter(None, [i.strip() for i in beach.css('::text').getall()]))

        water_recreation = response.xpath("//span[contains(text(),'Water sports and recreation')]/parent::summary[1]/following-sibling::ul[1]")
        item['Water Sports and Recreation'] = ', '.join(filter(None, [i.strip() for i in water_recreation.css('::text').getall()]))

        for_children = response.xpath("//span[contains(text(),'For children')]/parent::summary[1]/following-sibling::ul[1]")
        item['For Children'] = ', '.join(filter(None, [i.strip() for i in for_children.css('::text').getall()]))

        sport_games = response.xpath("//span[contains(text(),'Sport and games')]/parent::summary[1]/following-sibling::ul[1]")
        item['Sport and Games'] = ', '.join(filter(None, [i.strip() for i in sport_games.css('::text').getall()]))

        recreation_adults = response.xpath("//span[contains(text(),'Recreation (adults)')]/parent::summary[1]/following-sibling::ul[1]")
        item['Recreation (Adults)'] = ', '.join(filter(None, [i.strip() for i in recreation_adults.css('::text').getall()]))

        situation_campsite = response.xpath("//span[contains(text(),'Situation of campsite')]/parent::summary[1]/following-sibling::ul[1]")
        item['Situation of Campsite'] = ', '.join(filter(None, [i.strip() for i in situation_campsite.css('::text').getall()]))

        for_motorhomes = response.xpath("//span[contains(text(),'For motorhomes')]/parent::summary[1]/following-sibling::ul[1]")
        item['For Motorhomes'] = ', '.join(filter(None, [i.strip() for i in for_motorhomes.css('::text').getall()]))

        disabled = response.xpath("//span[contains(text(),'Disabled')]/parent::summary[1]/following-sibling::ul[1]")
        item['Disabled'] = ', '.join(filter(None, [i.strip() for i in disabled.css('::text').getall()]))

        miscellaneous = response.xpath("//span[contains(text(),'Miscellaneous')]/parent::summary[1]/following-sibling::ul[1]")
        item['Miscellaneous'] = ', '.join(filter(None, [i.strip() for i in miscellaneous.css('::text').getall()]))

        popular_amenities = response.xpath("//span[contains(text(),'Popular amenities')]/parent::summary[1]/following-sibling::ul[1]")
        item['Popular Amenities'] = ', '.join(filter(None, [i.strip() for i in popular_amenities.css('::text').getall()]))



        item['Detail_URL'] = response.url
        yield item
        ########        This Commented code is to extract reviews array in output file.
        # item['Reviews'] = []
        # reviews_url = f'https://www.eurocampings.co.uk/esi/campsite/detail/{item['ID']}/reviews/?tab=reviews&reviewLocale=&reviewPage=1&reviewSort=date'
        # yield response.follow(reviews_url, callback=self.reviews_parse, headers=self.headers, meta={'item': item})


    def reviews_parse(self, response):
        item = response.meta['item']
        for review in response.css('p.review-customer-text'):
            review_text = ' '.join(e.strip() for e in review.css('::text').getall())
            item['Reviews'].append(review_text)

        next_page = response.css('a.pagination__btn--next ::attr(href)').get('').strip()
        if next_page:
            yield response.follow(next_page, callback=self.reviews_parse, headers=self.headers, meta={'item': item})
        else:
            yield item



