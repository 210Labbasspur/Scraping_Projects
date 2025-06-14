import re
import os
import json
import random
import requests
from datetime import datetime
from urllib.parse import urljoin
from scrapy import Spider, Request
from supabase import create_client, Client


class full_transfer_markt_players(Spider):
    name = 'full_transfer_markt_players'
    base_url = 'https://www.transfermarkt.co.uk'
    url = "https://www.transfermarkt.co.uk/spieler-statistik/wertvollstespieler/marktwertetop?ajax=yw1&page=1"
    api_url = 'https://www.transfermarkt.co.uk/ceapi/transferHistory/list/{}'
    african_countries = [
        'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cape Verde',
        'Central African Republic', 'Chad', 'Comoros', 'Congo', "Cote d'Ivoire", 'DR Congo',
        'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon',
        'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya', 'Lesotho', 'Liberia', 'Libya',
        'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique',
        'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'São Tomé and Príncipe', 'Senegal', 'Seychelles',
        'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Tanzania', 'Togo',
        'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe'
    ]
    african_countries_land_id = ['4', '6', '21', '29', '30', '32', '138', '171', '35', '85', '38', '41', '193', '2',
                                 '8', '46', '162', '11', '51', '54', '59', '60', '82', '93', '95', '96', '101', '102',
                                 '105', '108', '109', '107', '115', '117', '123', '124', '139', '149', '151', '152',
                                 '156', '159', '160', '166', '168', '173', '176', '142', '187']
    fieldnames = ['date', 'kiniscore_id', 'player_first_name', 'player_middle_name', 'player_last_name',
                  'player_img', 'gender', 'player_foot', 'position', 'dob', 'height_m', 'age', 'citizenship',
                  'nationality', 'video_link', 'appearance', 'starting_eleven', 'goals_scored', 'assists',
                  'goals_per_min', 'minutes_played', 'goal_participation', 'yellow_cards', 'red_cards',
                  'transfer_date', 'club_left', 'club_joined', 'date_joined', 'market_value_euro',
                  'highest_transfer_euro', 'joined_type_fee', 'contract_expires', 'league_joined',
                  'league_level', 'season_year', 'social_media', 'player_agent_name', 'player_agent_phone',
                  'player_agent_email', 'player_agent_website', 'player_agent_mk_value', 'partner_id',
                  'player_agent_page'
                  # , 'Player URL'
                  ]

    custom_settings = {
        'CONCURRENT_REQUESTS': 4,
        # comment from here
        # "ZYTE_API_EXPERIMENTAL_COOKIES_ENABLED": True,
        # 'DOWNLOAD_HANDLERS': {
        #     "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        #     "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        # },
        # 'DOWNLOADER_MIDDLEWARES': {
        #     "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
        # },
        # 'REQUEST_FINGERPRINTER_CLASS': "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        # 'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        # 'ZYTE_API_KEY': "98fb508da034485784810ff332818248",  # TODO: Please enter you api-key
        # "ZYTE_API_TRANSPARENT_MODE": True,
        # comment to here

        # Uncommet below to get a csv output
        'FEEDS': {
            f'output/Transfer Markt Players {datetime.now().strftime("%d%m%Y%H%M")}.csv': {
                'format': 'csv',
                'fields': fieldnames

            },
        }
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    headers2 = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.transfermarkt.co.uk',
        'priority': 'u=0, i',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    '''        ######   Client's Credentials                 '''
    supabase_url = 'https://kczmkmsppqqwrlpccdnd.supabase.co/'
    supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtjem1rbXNwcHFxd3JscGNjZG5kIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIxNzgxMjgsImV4cCI6MjA0Nzc1NDEyOH0.SI21dD-2enfNd1DGw0RRMq6Eob5pPbOzeoL9NhSxuek'
    table_name = 'full_scrape'

    skipped_players = 0
    player_found = 0
    seen_urls = []

    supabase: Client = create_client(supabase_url, supabase_key)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.seen_player_ids = []
        self.supabase = self.initialize_supabase_client()  # Ensure this method sets up the client correctly


    def start_requests(self):
        ages_range = ['u17', 'u18', 'u19', 'u20', 'u21', 'u23', '23-30']
        for land_id in self.african_countries_land_id:
            for age in ages_range:
                url = f'https://www.transfermarkt.co.uk/spieler-statistik/wertvollstespieler/marktwertetop/plus/0/galerie/0?ausrichtung=alle&spielerposition_id=alle&altersklasse={age}&jahrgang=0&land_id={land_id}&kontinent_id=0&yt0=Show'
                yield Request(url=url, callback=self.parse, headers=self.headers)


    def parse(self, response, **kwargs):
        table_rows = response.css('#yw1 .inline-table .hauptlink a') or response.css('#yw0 tbody tr.even, #yw0 tbody tr.odd')
        for player in table_rows:
            self.player_found += 1
            player_url = player.css('.hauptlink ::attr(href)').get('') or player.css('::attr(href)').get('').strip()
            url = urljoin(self.base_url, player_url)
            self.seen_urls.append(url)
            print('Detail page to surf is : ', urljoin(self.base_url, player_url))
            yield Request(url=urljoin(self.base_url, player_url), callback=self.parse_detail, headers=self.headers, dont_filter=True)

        next_page = response.xpath("//*[contains(@title,'Go to the next page')]/@href").get('').strip()
        if next_page:
            next_page_url = self.base_url + next_page
            yield Request(url=next_page_url, callback=self.parse, headers=self.headers, dont_filter=True)


    def parse_detail(self, response):
        item = {key: '' for key in self.fieldnames}
        player_id = int((response.url).split("/")[-1])
        if player_id in self.seen_player_ids:
            return

        self.seen_player_ids.append(player_id)

        # item['Player URL'] = response.url
        item['date'] = datetime.now().date().strftime('%Y-%m-%d')
        item['kiniscore_id'] = self.generate_unique_key(response.url)
        item['partner_id'] = str(player_id)

        full_name = response.xpath("//*[contains(text(),'ame')]/following-sibling::span[1]/text()").get('').strip()

        if full_name and not full_name.isalpha():
            full_name = ' '.join([n.strip() for n in response.css('.data-header__headline-wrapper ::text').getall() if n.strip()]).strip()
            full_name = self.remove_numbers_and_hash(string=full_name)

        if full_name:
            name_parts = full_name.split()
            item['player_first_name'] = name_parts[0].strip() if name_parts else ""
            item['player_middle_name'] = " ".join(name_parts[1:-1]) if len(name_parts) > 2 else ""
            item['player_last_name'] = name_parts[-1].strip() if len(name_parts) > 1 else ''

        else:
            name = ' '.join(e.strip() for e in response.css(".data-header__headline-wrapper ::text").getall())
            full_name = self.remove_numbers_and_hash(string=name)
            # filtered_name = name.strip().replace('#', '')
            name_parts = full_name.split()

            item['player_first_name'] = name_parts[0].strip() if name_parts else ""
            item['player_middle_name'] = " ".join(name_parts[1:-1]) if len(name_parts) > 2 else ""
            item['player_last_name'] = name_parts[-1].strip() if len(name_parts) > 1 else ''

            # item['player_first_name'] = re.sub(r'\d', '', filtered_name)

        item['player_img'] = response.css('#fotoauswahlOeffnen img ::attr(src)').get('').strip()
        item['gender'] = 'M'
        item['player_foot'] = response.xpath("//*[contains(text(),'Foot:')]/following-sibling::span[1]/text()").get('').strip().capitalize()

        position_str = response.xpath("//*[contains(text(),'Position:')]/following-sibling::span[1]/text()").get('').strip()
        position = '-'.join(position_str.split('-')[1:]).strip().replace(' ', '-') or response.css('.data-header__label:contains("Position") .data-header__content ::text').get('').strip()

        if position.lower() == 'left':
            position = 'Left-Back'

        elif position.lower() == 'right':
            position = 'Right-Back'

        elif position.lower() == 'centre':
            position = 'Centre-Forward'

        elif position.lower() == 'Second-Striker'.lower():
            position = 'Centre-Forward'

        elif position.lower() == 'Right-Midfield'.lower():
            position = 'Right-Winger'

        elif position.lower() == 'Left-Midfield'.lower():
            position = 'Left-Winger'

        elif position.lower() == 'Defensive'.lower():
            position = 'Centre-Back'

        elif position.lower() == 'Midfield'.lower():
            position = 'Central-Midfield'

        elif position.lower() == 'Defender'.lower():
            position = 'Centre-Back'

        elif position.lower() == 'Attack'.lower():
            position = 'Centre-Forward'

        if not position:
            d = 1

        # item['position'] = position.split()[0]
        item['position'] = position

        # item['league_joined'] = self.convert_date(response.css('span.info-table__content.info-table__content--regular:contains("Joined:") + span ::text').get('').strip())
        item['league_joined'] = ''.join(response.css('.data-header__league-link ::text').getall()).strip() or response.css('.data-header__league-link img ::attr(alt)').get('')
        item['contract_expires'] = self.convert_date(response.css('span.info-table__content.info-table__content--regular:contains("Contract expires:") + span ::text').get('').strip())
        item['league_level'] = ''.join(''.join(response.css('span.data-header__label:contains("League level:") ::text').getall()).strip().split(':')[1:2]).strip()
        item['market_value_euro'] = self.parse_value(''.join(''.join(response.css('.data-header__market-value-wrapper ::text').getall()).split()[:1]))
        height_text = response.xpath("//*[contains(text(),'Height:')]/following-sibling::span[1]/text()").get('').strip()
        height_m = height_text.replace('\xa0', ' ').replace(',', '.').replace('m', '').replace(' ', '')

        try:
            item['height_m'] = round(float(height_m), 1)
        except:
            item['height_m'] = 0.0

        dob = response.xpath("//*[contains(text(),'Date of birth')]/following-sibling::span[1]/a/text()").get('').strip()
        dob_match = re.search(r'(\w{3}\s\d{1,2},\s\d{4})', dob)

        if dob_match:
            dob_str = dob_match.group(0)
            date_obj = datetime.strptime(dob_str, '%b %d, %Y').date()
            item['dob'] = date_obj.strftime('%Y-%m-%d')

        # age_match = re.search(r'\((\d+)\)', dob)
        age_match = re.search(r'\(~?\s*(\d+)\)', dob)

        if age_match:
            age = int(age_match.group(1))
            item['age'] = age

            if age < 17:
                return

            if age > 28:
                return

        citizenship = response.xpath("//*[contains(text(),'Citizenship:')]/following-sibling::span[1]/text()").getall()
        # citizenship_countries = [c.strip() for c in citizenship if c.strip()]
        # citizenship_country = ''.join(citizenship_countries[1:]) if len(citizenship_countries) > 1 else ''.join(citizenship_countries[:1])

        citizenship_country = response.css('.data-header__label:contains("Place of birth:")  img ::attr(alt)').get('') or ''.join([c.strip() for c in citizenship if c.strip().lower() in [country.lower() for country in self.african_countries]][:1])
        nationality = response.css('.data-header__label:contains("Citizenship:")  img ::attr(alt)').get('') or response.css(".flagge+ a ::text").get('').strip()

        is_african_citizenship_country = self.is_player_is_african(player_country=citizenship_country)
        is_african_nationality_country = self.is_player_is_african(player_country=nationality)

        country_matched = is_african_nationality_country or is_african_citizenship_country

        if not country_matched:
            self.skipped_players += 1
            print(f'\n\nCitizenship:{citizenship_country} Nationality:{nationality}\n')
            return

        item['starting_eleven'] = self.get_start_eleven_value(player_id=player_id)

        item['nationality'] = nationality
        item['citizenship'] = citizenship_country

        item['video_link'] = ''

        social_media = response.css('.socialmedia-icons a::attr(href)').getall()

        item['social_media'] = ', '.join(sm.strip() for sm in social_media)

        player_stats = response.xpath("//*[contains(text(),'View full stats')]/@href").get('').strip()

        if response.xpath("//*[contains(text(),'Player agent:')]/following-sibling::span[1]/a/@href").get('').strip():

            contact = self.base_url + response.xpath("//*[contains(text(),'Player agent:')]/following-sibling::span[1]/a/@href").get('').strip()

            item['player_agent_name'] = response.xpath("//*[contains(text(),'Player agent:')]/following-sibling::span[1]/a/text()").get('').strip()
            item['player_agent_page'] = contact

            yield response.follow(url=contact, callback=self.contact, headers=self.headers, meta={'item': item, 'player_stats': player_stats},dont_filter=True)

        else:
            yield response.follow(url=player_stats, callback=self.stats, headers=self.headers, meta={'item': item}, dont_filter=True)


    def contact(self, response):
        player_stats = response.meta['player_stats']

        item = response.meta['item']
        item['player_agent_phone'] = response.xpath("//*[contains(text(),'Phone:')]/following-sibling::span[1]/text()").get('').strip().replace('-', '')
        item['player_agent_email'] = response.xpath("//*[contains(text(),'Email:')]/following-sibling::span[1]/a/text()").get('').strip()
        item['player_agent_website'] = response.xpath("//*[contains(text(),'Website:')]/following-sibling::span[1]/a/text()").get('').strip().lower()

        player_agent_mk_value = response.xpath("//*[contains(text(),'Total market value')]/following-sibling::span[1]/text()").get('').strip()

        if 'm' in player_agent_mk_value:
            if re.search(r'\d', player_agent_mk_value.strip('€m')):
                item['player_agent_mk_value'] = int(float(player_agent_mk_value.strip('€m').replace('-', '')) * 1e6)

        elif 'k' in player_agent_mk_value:
            if re.search(r'\d', player_agent_mk_value.strip('€k')):
                item['player_agent_mk_value'] = int(float(player_agent_mk_value.strip('€k').replace('-', '')) * 1e3)

        yield response.follow(url=player_stats, callback=self.stats, headers=self.headers,
                              meta={'item': item}, dont_filter=True)

    def stats(self, response):
        item = response.meta['item']

        try:
            item['appearance'] = int(response.xpath("//*[contains(text(),'Total')]/following-sibling::td[2]/text()").get('').strip().replace('-', ''))
        except:
            item['appearance'] = 0

        try:
            item['goals_scored'] = int(response.xpath("//*[contains(text(),'Total')]/following-sibling::td[3]/text()").get('').strip().replace('-', ''))
        except:
            item['goals_scored'] = 0

        try:
            item['assists'] = int(
                response.xpath("//*[contains(text(),'Total')]/following-sibling::td[4]/text()").get('').strip().replace('-', ''))
        except:
            item['assists'] = 0

        try:
            item['minutes_played'] = int(response.xpath("//*[contains(text(),'Total')]/following-sibling::td[8]/text()").get('').strip().replace('.', '').replace('\'', ''))
        except:
            pass

        if response.xpath("//*[contains(text(),'Total')]/following-sibling::td[5]/text()").get('').strip() == '-':
            item['yellow_cards'] = 0

        else:
            try:
                item['yellow_cards'] = int(response.xpath("//*[contains(text(),'Total')]/following-sibling::td[5]/text()").get('').strip().replace('-', ''))
            except:
                item['yellow_cards'] = 0

        if response.xpath("//*[contains(text(),'Total')]/following-sibling::td[7]/text()").get('').strip() == '-':
            item['red_cards'] = ''

        else:
            try:
                red_card_td_num = [i for i in range(1, 10) if response.css(f'#yw1_c{i}').css('[title="Red cards"]')][0]
            except:
                red_card_td_num = 7

            sel = f"//*[contains(text(),'Total')]/following-sibling::td[{red_card_td_num}]/text()"
            item['red_cards'] = int(response.xpath(sel).get('0').strip().replace('-', '0'))

        try:
            goals_scored = int(response.xpath("//*[contains(text(),'Total')]/following-sibling::td[3]/text()").get('').strip().replace('-', ''))
        except:
            goals_scored = 0

        if goals_scored:
            try:
                item['goal_participation'] = int(item['assists']) + goals_scored
            except:
                item['goal_participation'] = 0

        else:
            try:
                item['goal_participation'] = int(item['assists'])
            except:
                item['goal_participation'] = 0

        if re.search(r'\d', response.xpath("//*[contains(text(),'Total')]/following-sibling::td[8]/text()").get('').strip()):
            minutes_played = int(response.xpath("//*[contains(text(),'Total')]/following-sibling::td[8]/text()").get('').strip().replace('.', '').replace('\'', '').replace('-', ''))

        else:
            minutes_played = 0

        if int(goals_scored) > 0:
            try:
                item['goals_per_min'] = round((float(minutes_played) / float(goals_scored)), 2)
            except:
                item['goals_per_min'] = 0

        id = item['partner_id']

        yield response.follow(url=self.api_url.format(id), callback=self.transfer, headers=self.headers,
                              meta={'item': item}, dont_filter=True)

    def transfer(self, response):
        item = response.meta['item']
        data = json.loads(response.text)

        if data['transfers']:
            try:
                date_string = data['transfers'][0]['dateUnformatted']
                date_obj = datetime.strptime(date_string, "%Y-%m-%d")
                item['transfer_date'] = date_obj.strftime("%Y-%m-%d")

                item['club_left'] = data['transfers'][0]['from']['clubName']
                item['club_joined'] = data['transfers'][0]['to']['clubName']

                date_string = data['transfers'][0]['date']
                date_obj = datetime.strptime(date_string, "%b %d, %Y")
                item['date_joined'] = date_obj.strftime("%Y-%m-%d")
            except:
                pass

            fee = data['transfers'][0]['fee']

            if 'm' in fee:
                if re.search(r'\d', fee.strip('€m')):
                    item['joined_type_fee'] = int(float(fee.strip('€m')) * 1e6)

            elif 'k' in fee:
                if re.search(r'\d', fee.strip('€k')):
                    item['joined_type_fee'] = int(float(fee.strip('€k')) * 1e3)
            else:
                try:
                    item['joined_type_fee'] = fee.replace('?', '').replace('-', '').strip()
                except:
                    pass

            if not item.get('joined_type_fee', ''):
                d=1

            transfer_values = [row.get('marketValue') for row in data.get('transfers', [])]
            item['highest_transfer_euro'] = self.find_highest_transfer_value(values=transfer_values)
            item['season_year'] = data['transfers'][0]['season']

            # capitalized_item = {key: (value.title() if isinstance(value, str) else value) for key, value in item.items()}
        else:
            return

        capitalized_item = {key: (value.title() if isinstance(value, str) and not value.startswith('http') else value) for key, value in item.items()}
        yield capitalized_item

        ####comment out return below for data to enter DB
        # return
        ####uncomment return above for it not to  enter DB

        '''  Saving data into supa-base database  '''
        print('lets save this data into supa-base database as well')
        capitalized_item = {k: (v if v != '' else None) for k, v in capitalized_item.items()}
        # response = self.supabase.table(self.table_name).insert([capitalized_item]).execute()        # Insert capitalized_item into Supabase table
        response = self.supabase.table(self.table_name).insert([item]).execute()        # Insert item into Supabase table
        if response.data:        # Handle the response based on its attributes
            print("Item inserted successfully into Supabase database.", capitalized_item)
        else:
            print("Failed to insert item into Supabase database.")



    def get_start_eleven_value(self, player_id):
        url = f'https://www.transfermarkt.co.uk/ceapi/player/{player_id}/performance'
        response = requests.get(url, headers=self.headers)
        try:
            start_eleven = round(json.loads(response.text)[0].get('startElevenPercent', 0), 2)
        except:
            start_eleven = ''
        return start_eleven


    def is_player_is_african(self, player_country):
        if not player_country.strip():
            return False
        for country in self.african_countries:
            if country.strip().lower() == player_country.strip().lower():
                return True
            if country.lower() in player_country.lower() or player_country in country.lower():
                return True
        return False


    def generate_unique_key(self, response_url):
        '''  extract the ID and apply the Caesar cipher with a shift of 3       '''
        player_id = re.search(r'(\d+)$', response_url).group(1)
        # Apply Caesar Cipher (shift 3 backwards)
        shifted_id = ''.join(str((int(digit) - 3) % 10) for digit in player_id)
        print(f"Extracted ID: {player_id}", f" || Shifted ID: {shifted_id}")
        return shifted_id

        """Generate a unique six-digit key and ensure it doesn't repeat."""
        # file_path = 'input/urls.txt'
        # try:
        #     def load_used_keys(file_path):            # Load used keys from the file
        #         if not os.path.exists(file_path):
        #             return set()
        #         with open(file_path, "r") as file:
        #             used_keys = {line.strip() for line in file}
        #         return used_keys
        # except:
        #     return set()
        #
        # def save_used_key(file_path, key):        # Save the newly generated key to the file
        #     with open(file_path, "a") as file:
        #         file.write(f"{key}\n")
        #
        # def generate_key(used_keys, response_url):        # Generate a unique six-digit key
        #     response_url = response_url
        #     while True:
        #         key = str(random.randint(100000, 999999))
        #         if key not in used_keys:
        #             used_keys.add(key)
        #             save_used_key(file_path, key)
        #             return key
        #
        # used_keys = load_used_keys(file_path)        # Main logic to generate and return a unique key
        # return generate_key(used_keys, response_url)


    def parse_value(self, value):
        """Convert a string value to a float, considering 'm' and 'k' units."""
        if not value.strip():
            return None

        if value == '-':
            return None

        value = value.replace('€', '').replace(',', '')
        if 'm' in value:
            return float(value.replace('m', '')) * 1e6
        elif 'k' in value:
            return float(value.replace('k', '')) * 1e3
        else:
            return float(value)

    def find_highest_transfer_value(self, values):
        """Find the highest numerical value in the list."""
        parsed_values = [self.parse_value(value) for value in values if self.parse_value(value) is not None]
        if not parsed_values:
            return None
        highest_value = max(parsed_values)
        return highest_value


    def convert_date(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, '%b %d, %Y')
            return date_obj.strftime('%Y-%m-%d')
        except:
            return ''


    def countries_with_code(self, country):
        country_with_code = {'Afghanistan': '1', 'Albania': '3', 'Algeria': '4', 'American Samoa': '239',
                   'American Virgin Islands': '234',
                   'Andorra': '5', 'Angola': '6', 'Anguilla': '232', 'Antigua and Barbuda': '7', 'Argentina': '9',
                   'Armenia': '10', 'Aruba': '233', 'Australia': '12', 'Austria': '127', 'Azerbaijan': '13',
                   'Bahamas': '14',
                   'Bahrain': '15', 'Bangladesh': '16', 'Barbados': '17', 'Belarus': '18', 'Belgium': '19',
                   'Belize': '20',
                   'Benin': '21', 'Bermuda': '211', 'Bhutan': '22', 'Bolivia': '23', 'Bonaire': '269',
                   'Bosnia-Herzegovina': '24',
                   'Botsuana': '25', 'Brazil': '26', 'British India': '276', 'British Virgin Islands': '231',
                   'Brunei Darussalam': '27', 'Bulgaria': '28', 'Burkina Faso': '29', 'Burundi': '30', 'Cambodia': '79',
                   'Cameroon': '31', 'Canada': '80', 'Cape Verde': '32', 'Cayman Islands': '229',
                   'Central African Republic': '138', 'Chad': '171', 'Chile': '33', 'China': '34',
                   'Chinese Taipei': '164',
                   'Christmas Island': '248', 'Colombia': '83', 'Comoros': '35', 'Congo': '85', 'Cookinseln': '238',
                   'Costa Rica': '36', "Cote d'Ivoire": '38', 'Crimea': '278', 'Croatia': '37', 'CSSR': '220',
                   'Cuba': '88',
                   'Curacao': '260', 'Cyprus': '188', 'Czech Republic': '172', 'Denmark': '39', 'Djibouti': '41',
                   'Dominica': '42', 'Dominican Republic': '43', 'DR Congo': '193', 'East Germany (GDR)': '222',
                   'Ecuador': '44',
                   'Egypt': '2', 'El Salvador': '45', 'England': '189', 'Equatorial Guinea': '8', 'Eritrea': '46',
                   'Estonia': '47', 'Eswatini': '162', 'Ethiopia': '11', 'Falkland Islands': '250',
                   'Faroe Islands': '208',
                   'Federated States of Micronesia': '111', 'Fiji': '48', 'Finland': '49', 'France': '50',
                   'French Guiana': '252',
                   'Gabon': '51', 'Georgia': '53', 'Germany': '40', 'Ghana': '54', 'Gibraltar': '266', 'Greece': '56',
                   'Greenland': '243', 'Grenada': '55', 'Guadeloupe': '251', 'Guam': '241', 'Guatemala': '58',
                   'Guernsey': '271',
                   'Guinea': '59', 'Guinea-Bissau': '60', 'Guyana': '61', 'Haiti': '62', 'Honduras': '66',
                   'Hongkong': '218',
                   'Hungary': '178', 'Iceland': '73', 'India': '67', 'Indonesia': '68', 'Iran': '71', 'Iraq': '70',
                   'Ireland': '72', 'Isle of Man': '270', 'Israel': '74', 'Italy': '75', 'Jamaica': '76', 'Japan': '77',
                   'Jersey': '272', 'Jordan': '78', 'Jugoslawien (SFR)': '223', 'Kazakhstan': '81', 'Kenya': '82',
                   'Kiribati': '246', 'Korea, North': '86', 'Korea, South': '87', 'Kosovo': '244', 'Kuwait': '89',
                   'Kyrgyzstan': '90', 'Laos': '91', 'Latvia': '92', 'Lebanon': '94', 'Lesotho': '93', 'Liberia': '95',
                   'Libya': '96', 'Liechtenstein': '97', 'Lithuania': '98', 'Luxembourg': '99', 'Macao': '219',
                   'Macedonia': '274', 'Madagascar': '101', 'Malawi': '102', 'Malaysia': '103', 'Maldives': '104',
                   'Mali': '105',
                   'Malta': '106', 'Marshall Islands': '257', 'Martinique': '207', 'Mauritania': '108',
                   'Mauritius': '109',
                   'Mayotte': '277', 'Mexico': '110', 'Moldova': '112', 'Monaco': '113', 'Mongolia': '114',
                   'Montenegro': '216',
                   'Montserrat': '235', 'Morocco': '107', 'Mozambique': '115', 'Myanmar': '116', 'Namibia': '117',
                   'Nauru': '118',
                   'Nepal': '119', 'Netherlands': '122', 'Netherlands Antilles': '227', 'Netherlands East India': '255',
                   'Neukaledonien': '236', 'New Zealand': '120', 'Nicaragua': '121', 'Niger': '123', 'Nigeria': '124',
                   'Niue': '261', 'North Macedonia': '100', 'Northern Ireland': '192',
                   'Northern Mariana Islands': '268',
                   'Norway': '125', 'Oman': '126', 'Pakistan': '128', 'Palau': '129', 'Palestine': '240',
                   'Panama': '130',
                   'Papua New Guinea': '131', 'Paraguay': '132', "People's republic of the Congo": '259', 'Peru': '133',
                   'Philippines': '134', 'Poland': '135', 'Portugal': '136', 'Puerto Rico': '228', 'Qatar': '137',
                   'Réunion': '249', 'Romania': '140', 'Russia': '141', 'Rwanda': '139', 'Saarland': '263',
                   'Saint-Martin': '267',
                   'Samoa': '143', 'San Marino': '144', 'Sao Tome and Principe': '145', 'Saudi Arabia': '146',
                   'Scotland': '190',
                   'Senegal': '149', 'Serbia': '215', 'Serbia and Montenegro': '150', 'Seychelles': '151',
                   'Sierra Leone': '152',
                   'Singapore': '153', 'Sint Maarten': '265', 'Slovakia': '154', 'Slovenia': '155',
                   'Solomon Islands': '69',
                   'Somalia': '156', 'South Africa': '159', 'Southern Sudan': '262', 'Spain': '157', 'Sri Lanka': '158',
                   'St. Kitts & Nevis': '225', 'St. Lucia': '230', 'St. Vincent & Grenadinen': '224', 'Sudan': '160',
                   'Suriname': '161', 'Swaziland': '273', 'Sweden': '147', 'Switzerland': '148', 'Syria': '163',
                   'Tahiti': '237',
                   'Tajikistan': '165', 'Tanzania': '166', 'Thailand': '167', 'The Gambia': '52', 'Tibet': '245',
                   'Timor-Leste': '242', 'Togo': '168', 'Tonga': '169', 'Trinidad and Tobago': '170', 'Tunisia': '173',
                   'Türkiye': '174', 'Turkmenistan': '175', 'Turks- and Caicosinseln': '226', 'Tuvalu': '247',
                   'UdSSR': '221',
                   'Uganda': '176', 'Ukraine': '177', 'United Arab Emirates': '183', 'United Kingdom': '264',
                   'United States': '184', 'Uruguay': '179', 'Uzbekistan': '180', 'Vanuatu': '181', 'Vatican': '256',
                   'Venezuela': '182', 'Vietnam': '185', 'Wales': '191', 'Western Sahara': '275', 'Yemen': '186',
                   'Yugoslavia (Republic)': '258', 'Zaire': '254', 'Zambia': '142', 'Zanzibar': '253',
                   'Zimbabwe': '187'}
        return country_with_code.get(country, '')


    def get_formdata(self, country_id):
        data = {
            'DetailsucheSaved[vorname]': '',
            'DetailsucheSaved[name]': '',
            'DetailsucheSaved[name_anzeige]': '',
            'DetailsucheSaved[passname]': '',
            'DetailsucheSaved[genaue_suche]': '0',
            'DetailsucheSaved[geb_ort]': '',
            'DetailsucheSaved[genaue_suche_geburtsort]': '0',
            'DetailsucheSaved[land_id]': country_id,
            'DetailsucheSaved[zweites_land_id]': '',
            'DetailsucheSaved[geb_land_id]': '',
            'DetailsucheSaved[kontinent_id]': '',
            'DetailsucheSaved[geburtstag]': "doesn't matter",
            'DetailsucheSaved[geburtsmonat]': "doesn't matter",
            'DetailsucheSaved[geburtsjahr]': '',
            'alter': '17 - 28',
            'DetailsucheSaved[age]': '17;28',
            'DetailsucheSaved[minAlter]': '17',
            'DetailsucheSaved[maxAlter]': '28',
            'jahrgang': '1850 - 2015',
            'DetailsucheSaved[jahrgang]': '1850;2015',
            'DetailsucheSaved[minJahrgang]': '1850',
            'DetailsucheSaved[maxJahrgang]': '2015',
            'groesse': '0 - 220',
            'DetailsucheSaved[groesse]': '0;220',
            'DetailsucheSaved[minGroesse]': '0',
            'DetailsucheSaved[maxGroesse]': '220',
            'speichern': 'Submit search',
            'DetailsucheSaved[hauptposition_id]': '',
            'DetailsucheSaved[nebenposition_id_1]': '',
            'DetailsucheSaved[nebenposition_id_2]': '',
            'DetailsucheSaved[minMarktwert]': '0',
            'DetailsucheSaved[maxMarktwert]': '20.000',
            'DetailsucheSaved[fuss_id]': [
                '',
                '',
            ],
            'DetailsucheSaved[captain]': [
                '',
                '',
            ],
            'DetailsucheSaved[rn]': '0',
            'DetailsucheSaved[wettbewerb_id]': '',
            'DetailsucheSaved[w_land_id]': '',
            'nm_spiele': '0 - 300',
            'DetailsucheSaved[nm_spiele]': '0;300',
            'DetailsucheSaved[minNmSpiele]': '0',
            'DetailsucheSaved[maxNmSpiele]': '300',
            'DetailsucheSaved[trans_id]': '0',
            'DetailsucheSaved[aktiv]': [
                '0',
                '1',
            ],
            'DetailsucheSaved[vereinslos]': '0',
            'DetailsucheSaved[leihen]': '0',
        }
        return data


    def remove_numbers_and_hash(self, string):
        cleaned_string = re.sub(r'[0-9#]', '', string)        # Use re.sub() to replace numbers and the # character with an empty string
        cleaned_string = cleaned_string.strip()
        return cleaned_string


    def close(spider, reason):
        d=1


    def initialize_supabase_client(self):
        supabase_url = self.supabase_url
        supabase_key = self.supabase_key
        try:        # Initializing the client
            supabase = create_client(supabase_url, supabase_key)
            print("Supabase client initialized successfully.")
            return supabase
        except Exception as e:
            print(f"Error initializing Supabase client: {e}")
            raise
