import re
import scrapy

class GAF(scrapy.Spider):
    name = 'GAF'
    url = "https://www.gaf.com/en-ca/roofing-contractors"
    prefix = "https://www.gaf.com"
    headers = {
      'authority': 'www.gaf.com',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
      'cache-control': 'max-age=0',
      # 'cookie': 'file_download=flushed; file_download=flushed; ai_user=vIfJCTfB8HkroaQUjumBi3|2023-07-10T16:08:33.673Z; _gid=GA1.2.2057139752.1689005320; ApplicationGatewayAffinityCORS=ff6a676c4453b7cfb884f25f3d524f14; ApplicationGatewayAffinity=ff6a676c4453b7cfb884f25f3d524f14; ASP.NET_SessionId=ku0orkcgwmodtkhu1wyrdbh1; OptanonAlertBoxClosed=2023-07-10T16:08:55.022Z; website#lang=en-CA; AKA_A2=A; SC_ANALYTICS_GLOBAL_COOKIE=36f05aafe6cf4a2c88e6c4d429073974|True; redirectUrl=https://www.gaf.com/en-ca/roofing-contractors/ma/hudson; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Jul+10+2023+09%3A20%3A32+GMT-0700+(Pacific+Daylight+Time)&version=202306.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=df8b98d1-b143-4ffa-a164-af4dc59dc1b0&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0007%3A1%2CC0004%3A1&geolocation=FR%3BIDF&AwaitingReconsent=false; RT="z=1&dm=gaf.com&si=8e9ae669-d601-4f37-b795-6ca74117ec44&ss=ljx25k2a&sl=5&tt=sqd&bcn=%2F%2F02179910.akstat.io%2F&rl=1&hd=fg23&r=723442715afcd03b0fc99ce272bd8739&obo=1"; _ga=GA1.2.1776234034.1689005320; _gat_UA-12712361-2=1; ai_session=SOFmlxGvcWDt/1e4wvHl8Z|1689005318885|1689006136383; _ga_NZXTQY46ZN=GS1.1.1689005320.1.1.1689006177.60.0.0; RT="z=1&dm=www.gaf.com&si=8e9ae669-d601-4f37-b795-6ca74117ec44&ss=ljx25k2a&sl=5&tt=sqd&bcn=%2F%2F02179910.akstat.io%2F&rl=1&hd=fg23&r=723442715afcd03b0fc99ce272bd8739&obo=1&ul=itbd"',
      'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'none',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    custom_settings = {
        'FEED_URI': 'new GAF.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }
    def get_address_parts(self, contact_detail):
        try:
            states = re.findall(r'\b[A-Z]{2}\b', contact_detail)
            if len(states) == 2:
                state = states[-1]
            else:
                state = states[0]
        except:
            state = ''
        try:
            street = contact_detail.rsplit(state, 1)[0].strip().rstrip(',').strip()
        except:
            street = ''
        try:
            zip_code = re.search(r"(?!\A)\b\d{5}(?:-\d{4})?\b", contact_detail).group(0)
        except:
            zip_code = ''

        return {
            'street': street,
            'state': state,
            'zipcode': zip_code
        }

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers)

    def parse(self, response):
        for states in response.css('.directory-top-level__serving-block__item a')[:5]:
            state_url = self.prefix+states.css('::attr(href)').get('')
            yield response.follow(url=state_url, callback=self.city_page, headers=self.headers)
        # yield response.follow(url='https://www.gaf.com/en-ca/roofing-contractors/ma',
        #                       callback=self.city_page, headers=self.headers)
    def city_page(self, response):
        for cities in response.css('.state-level-directory-listing__item a')[:5]:
            cities_url = self.prefix + cities.css("::attr(href)").get('')
            yield response.follow(url=cities_url, callback=self.listing_page, headers=self.headers)
        # next_page = response.css('.contractor-pagination__arrow--right::attr(href)').get('').strip()
        # if next_page:
        #     yield response.follow(url=next_page, callback=self.city_page, headers=self.headers)
        # yield response.follow(url='https://www.gaf.com/en-ca/roofing-contractors/ma/abington', callback=self.listing_page, headers=self.headers)

    def listing_page(self, response):
        for listing in response.css('.contractor-results__item'):
            roofing_name = listing.css('.contractor-result-card__name::text').get('').strip()
            roofing_url = self.prefix + listing.css('.contractor-result-card__image-overlay-wrapper ::attr(href)').get('')
            yield response.follow(url=roofing_url, callback=self.detail_page, headers=self.headers)
        # next_list = response.css('.contractor-pagination__arrow--right::attr(href)').get('').strip()
        # if next_list:
        #     yield response.follow(url=next_list, callback=self.listing_page, headers=self.headers)
        # yield response.follow(url='https://www.gaf.com/en-ca/roofing-contractors/residential/viola-roofing-contracting-inc-1000008',
        #                       callback=self.detail_page, headers=self.headers)

    def detail_page(self, response):
        item = dict()
        item['Name'] = response.css('.contractor-profile-hero-banner__name ::text').get('').strip()
        Address = self.get_address_parts(response.css('.contractor-profile-hero-banner__address ::text').get(''))
        item['Street'] = Address.get('street', '')
        item['State'] = Address.get('state', '')
        item['Zip Code'] = Address.get('zipcode', '')
        item['Rating'] = response.css('.contractor-result-card__stars-rating ::text').get('').strip()
        item['No_of_Reviews'] = response.css('.contractor-profile-hero-banner__amount ::text').get('').strip()
        item['No_of_Reviews'] = (item['No_of_Reviews'].replace('(','')).replace(')','')
        item['Social_Sites'] = response.css('.contractor-profile-hero-banner__social-image ::attr(href)').getall()
        item['Image'] = self.prefix + response.css('.contractor-profile-hero-banner__image-wrapper img::attr(src)').get('').strip()
        item['Contact'] = response.css('.contractor-profile-hero-banner__cta-block ::attr(title)').get('').strip()

        item['about'] = response.css('.contractor-about-block__content ::text').get()
        item['Member_Since'] = response.xpath(
            '//div[contains(text(),"Member Since:")]/following-sibling::div/text()').get('')
        item['Certification'] = response.css('.at-a-glance-block__detail--certifications a::text').get('').strip()
        item['Project_Photos'] = ', '.join(
            data.css('img::attr(src)').get('').strip() for data in response.css('.contractor-projects-block__item'))

        item['Google_Rating'] = response.css('#panel-reviews-google .gaf-reviews-listing-overview__stars-rating ::text').get('').strip()
        item['No of Google_Reviews'] = response.css('#panel-reviews-google .gaf-reviews-listing-overview__rating-amount ::text').get('').strip()
        item['No of Google_Reviews'] = (item['No of Google_Reviews'].replace('(', '')).replace(')', '')
        item['Google_Reviews'] = ', '.join(
            (data.css('.gaf-reviews-listing__quote::text').get('') +' by ' + data.css('.gaf-reviews-listing__author::text').get(''))
            .strip() for data in response.xpath("//*[contains(@class, 'gaf-reviews-listing__item col-xs-12 col-sm-6 col-lg-4')]"))

        item['GAF_Rating'] = response.css('#panel-reviews-gaf .gaf-reviews-listing-overview__stars-rating ::text').get('').strip()
        item['No of GAF_Reviews'] = response.css('#panel-reviews-gaf .gaf-reviews-listing-overview__rating-amount ::text').get('').strip()
        item['No of GAF_Reviews'] = (item['No of GAF_Reviews'].replace('(', '')).replace(')', '')
        item['GAF_Reviews'] = ', '.join(
            (data.css('.gaf-reviews-listing__quote::text').get('') +' by ' + data.css('.gaf-reviews-listing__author::text').get(''))
            .strip() for data in response.xpath("//*[contains(@class, 'gaf-reviews-listing__item col-12 col-sm-4 col-lg-3')]"))

        item['Awards'] = ', '.join(
            (data.css('h3.awards-block__name::text').get('') +' , ' + data.css('.awards-block__content::text').get('')).strip()
            for data in response.xpath("//*[contains(@class, 'awards-block__item col-12 col-sm-6 col-lg-3')]"))

        yield item