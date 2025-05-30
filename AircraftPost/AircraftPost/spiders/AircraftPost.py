############3       AircraftPost

import scrapy
import datetime

class AircraftPost(scrapy.Spider):
    name = 'AircraftPost'
    url = "https://aircraftpost.com/current_markets/summary_on_market"
    headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://aircraftpost.com',
            'priority': 'u=0, i',
            'referer': 'https://aircraftpost.com/sign_in',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            # 'cookie': '_ga=GA1.1.1688421773.1743769159; _acp-web_session=L2U1VnI0Q0lvU3lrczFrVjVFS012RC9kMXpRcXVTM2xIdmhNbHFDWFVmZm5JcnorQTJNeDVFM2Q3dm5lKzF3bXdPejFoYy85b1RiVGtGb0lkYWF5dVNnaG05RUY3K0VJY0FEVmdKNjVncVR0ejJqK0M5WmVEbUdTM1hQUlMrWnJBQSszNFUvTURBdUxKSmExR0JqWUlCY3J1MjBvdXY2Q1ZhTjRVeUVyTmxlMUdzNnpycksyUE53Uy82S3hHeDBLSndTMGpVM3V3aUxxREtlWHNuSGpqZz09LS00dUdyWlhQVnZwVENzY3NjT2FmZGh3PT0%3D--b32463d17576489589be52bd13d96ab6f7766187; _ga_SPG0WKNT79=GS1.1.1744831663.4.0.1744832009.0.0.0',
        }
    # make_model_url = "https://www.aircraftpost.com/current_markets/detail_on_market?make_model={}"
    make_model_url = "https://aircraftpost.com/current_markets/detail_on_market?make_model={}"
    make_model_headers = {
          'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
          'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
          'cache-control': 'max-age=0',
          'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'sec-fetch-dest': 'document',
          'sec-fetch-mode': 'navigate',
          'sec-fetch-site': 'same-origin',
          'sec-fetch-user': '?1',
          'upgrade-insecure-requests': '1',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
          'cookie': '',
    }

    custom_settings = {
        'FEED_URI': f'output/AircraftPost_Market {datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }

    def start_requests(self):
        yield scrapy.Request('https://aircraftpost.com/', headers=self.headers, callback=self.pre_parse)

    def pre_parse(self, response):
        data = {
            'utf8': '✓',
            # 'authenticity_token': 'UgnDEspn/ev133DuJirkADybS5vD10vvSV0hMebym19+LvreU+F+7Il1b7/VP2XQXpXIHrtXFS7s293B5bzvVw==',
            'authenticity_token': response.xpath("//*[@name='csrf-token']/@content").get('').strip(),
            'session[email]': 'djaubert@jet8.com',
            'session[password]': 'Kldj1981!',
            'commit': 'Login',
        }
        yield scrapy.FormRequest('https://aircraftpost.com/session', method='POST', formdata=data, callback=self.post_parse,
                                 dont_filter=True, headers=self.headers)

    def post_parse(self, response):
        yield scrapy.Request("https://www.aircraftpost.com/current_markets/summary_on_market", headers=self.headers, callback=self.parse)


    def parse(self, response):
        count = 0
        for make_model in response.xpath("//select[contains(@name,'make_model')]/option"):
            make_model_ID = make_model.css("::attr(value)").get('').strip()
            make_model_Name = make_model.css("::text").get('').strip()
            if make_model_Name != '':
                print(f'Make/Model is {make_model_Name} and its ID is : {make_model_ID}')
                detail_url = self.make_model_url.format(make_model_ID)
                count += 1
                print(count, '# Detail URL is : ', detail_url)
                yield scrapy.Request(url=self.make_model_url.format(make_model_ID), headers=self.make_model_headers,
                                     callback=self.details, meta={'make_model_Name': make_model_Name})


    def details(self, response):
        item = dict()
        item['Date Ingested'] = datetime.datetime.now().strftime("%d/%m/%Y")
        item['Avg. Market Time (days)'] = response.xpath("//th[contains(text(),'Market Time ')]/following-sibling::td/text()").get('')
        item['Make Model'] = response.meta.get('make_model_Name','')
        no = 1
        for data in response.xpath("//*[contains(@class,'center th-sub-title')]"):
            no += 1
            item['ER'] = 'Yes' if response.css(f'#row_optional_item_type_177 td:nth-child({no}) ::text').get('') == '✔' else ' '
            item['Serial Number'] = data.css('label::text').get('')

            item['Registration'] = response.css(f'#row_registration_number td:nth-child({no}) ::text').get('')
            item['MFR Year'] = response.css(f'#row_year_manufactured td:nth-child({no}) ::text').get('')
            item['EIS Date'] = '01-' + response.css(f'#row_e_is_date td:nth-child({no}) ::text').get('')
            item['Airframe Hours'] = '{:,}'.format(int(response.css(f'#row_air_frame_hours td:nth-child({no}) ::text').get('')))
            item['Country'] = response.css(f'#row_country td:nth-child({no}) span::text').get('').strip()
            item['Time on Market (days)'] = response.css(f'#row_current_days_on_market td:nth-child({no}) ::text').get('').strip()
            item['Ask Price (M)'], item['Ask Price_MO'] = '',''
            if response.css(f'#row_asking_price td:nth-child({no}) b::text').get('').strip() == 'M/O':
                item['Ask Price_MO'] = 'Yes'
            else:
                item['Ask Price (M)'] = ''.join(e.strip().replace('$','').replace('TBD','').replace('Lease','') for e in response.css(f'#row_asking_price td:nth-child({no}) b ::text').getall())
            item['Engine Program Type'] = response.css(f'#row_engine_program_type td:nth-child({no}) a::text').get('').strip()
            item['Passengers'] = response.css(f'#row_passenger_configuration td:nth-child({no}) ::text').get('')
            item['Collins Venue CMS'] = 'Yes' if response.css(f'#row_optional_item_109 td:nth-child({no}) ::text').get('') == '✔' else ' '
            item['Ku-band Internet'] = 'Yes' if response.css(f'#row_optional_item_597 td:nth-child({no}) ::text').get('') == '✔' else ' '
            item['Ka-band internet'] = 'Yes' if response.css(f'#row_optional_item_532 td:nth-child({no}) ::text').get('') == '✔' else ' '
            item['Starlink'] = 'Yes' if response.css(f'#row_optional_item_687 td:nth-child({no}) ::text').get('') == '✔' else ' '
            item['BBML'] = 'Yes' if response.css(f'#row_optional_item_556 td:nth-child({no}) ::text').get('') == '✔' else ' '
            item['GoGo Biz ATG-4000'] = 'Yes' if response.css(f'#row_optional_item_206 td:nth-child({no}) ::text').get('') == '✔' else ' '
            item['GoGo Biz ATG-5000'] = 'Yes' if response.css(f'#row_optional_item_553 td:nth-child({no}) ::text').get('') == '✔' else ' '
            item['Gogo Biz Avance L5'] = 'Yes' if response.css(f'#row_optional_item_573 td:nth-child({no}) ::text').get('') == '✔' else ' '
            item['SwiftBroadband'] = 'Yes' if response.css(f'#row_optional_item_558 td:nth-child({no}) ::text').get('') == '✔' else ' '


            # item['Average Selling Price (M)'] = response.css(f'#row_avg_selling_price td:nth-child({no}) b::text').get('').strip().replace('$','').replace('TBD','').replace('Lease','')
            # item['Base'] = response.css(f'#row_airport td:nth-child({no}) a::text').get('')
            # item['Damage History'] = response.css(f'#row_damage_history td:nth-child({no}) ::text').get('')
            # item['Prior Owners'] = response.css(f'#row_prior_owners td:nth-child({no}) ::text').get('')
            # item['Airframe Hours'] = '{:,}'.format(int(response.css(f'#row_air_frame_hours td:nth-child({no}) ::text').get('')))
            # item['Total Landings'] = '{:,}'.format(int(response.css(f'#row_total_landings td:nth-child({no}) ::text').get('')))
            # item['APU Program'] = 'Yes' if response.css(f'#row_apu_program_msp td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Certification (FAR91)'] = response.css(f'#row_certification td:nth-child({no}) ::text').get('')
            # item['Interior (years)'] = response.css(f'#row_interior_years td:nth-child({no}) ::text').get('')
            # item['Paint (years)'] = response.css(f'#row_paint_years td:nth-child({no}) ::text').get('')
            #
            # item['Engine Hours to Inspection'] = response.css(f'#row_engine_hours_to_inspection td:nth-child({no}) ::text').get('').strip().replace('\n','')
            # item['Galley'] = response.css(f'#row_galley td:nth-child({no}) ::text').get('')
            # item['Lav'] = response.css(f'#row_lav td:nth-child({no}) ::text').get('')
            # item['Engine Inspection Date'] = response.css(f'#row_engine_inspection_due td:nth-child({no}) ::text').get('')
            # item['Airframe Inspection (48 month)'] = response.xpath(f"//*[contains(text(),'Airframe Inspection (48 month)')]/following-sibling::td[{no-1}]/text()").get('')
            # item['Airframe Inspection (60 month)'] = response.xpath(f"//*[contains(text(),'Airframe Inspection (60 month)')]/following-sibling::td[{no-1}]/text()").get('')
            # item['Airframe Inspection (72 month)'] = response.xpath(f"//*[contains(text(),'Airframe Inspection (72 month)')]/following-sibling::td[{no-1}]/text()").get('')
            # item['Airframe Inspection (96 month)'] = response.xpath(f"//*[contains(text(),'Airframe Inspection (96 month)')]/following-sibling::td[{no-1}]/text()").get('')
            # item['Airframe Inspection (120 month)'] = response.xpath(f"//*[contains(text(),'Airframe Inspection (120 month)')]/following-sibling::td[{no-1}]/text()").get('')
            # item['Airframe Inspection (C check / 6 years)'] = response.xpath(f"//*[contains(text(),'Airframe Inspection (C check / 6 years)')]/following-sibling::td[{no-1}]/text()").get('')
            # item['Airframe Inspection (72 or 96 month)'] = response.xpath(f"//*[contains(text(),'Airframe Inspection (72 or 96 month)')]/following-sibling::td[{no-1}]/text()").get('')
            # item['Airframe Inspection (96 or 108 month)'] = response.xpath(f"//*[contains(text(),'Airframe Inspection (96 or 108 month)')]/following-sibling::td[{no-1}]/text()").get('')
            # item['Airframe Inspection (8C / 10 years)'] = response.xpath(f"//*[contains(text(),'Airframe Inspection (8C / 10 years)')]/following-sibling::td[{no-1}]/text()").get('')
            # item['Airframe Inspection (12 year)'] = response.xpath(f"//*[contains(text(),'Airframe Inspection (12 year')]/following-sibling::td[{no-1}]/text()").get('')
            # # # item[''] = response.css(f'#row_engine_hours_to_inspection td:nth-child({no}) ::text').get('')
            #
            #
            # item['Pro Line 21 Advanced'] = 'Yes' if response.css(f'#row_optional_item_263 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Dual HF Comm'] = 'Yes' if response.css(f'#row_optional_item_142 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Dual ADF'] = 'Yes' if response.css(f'#row_optional_item_121 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Dual FMS-V Speed'] = 'Yes' if response.css(f'#row_optional_item_138 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Dual GPS'] = 'Yes' if response.css(f'#row_optional_item_394 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Dual WAAS GPS'] = 'Yes' if response.css(f'#row_optional_item_397 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Flight Data Recorder'] = 'Yes' if response.css(f'#row_optional_item_190 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['TAWS'] = 'Yes' if response.css(f'#row_optional_item_312 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Enhanced Weather Radar'] = 'Yes' if response.css(f'#row_optional_item_176 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['XM Weather'] = 'Yes' if response.css(f'#row_optional_item_361 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Divan'] = 'Yes' if response.css(f'#row_optional_item_118 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Footrest'] = 'Yes' if response.css(f'#row_optional_item_197 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Galley Pocket Door'] = 'Yes' if response.css(f'#row_optional_item_202 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Wood Veneer (Light)'] = 'Yes' if response.css(f'#row_optional_item_356 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Wood Veneer (Medium)'] = 'Yes' if response.css(f'#row_optional_item_357 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Wood Veneer (Dark)'] = 'Yes' if response.css(f'#row_optional_item_355 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['ICG ICS-200'] = 'Yes' if response.css(f'#row_optional_item_563 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['ICG Nxt-Link Iridium Satcom'] = 'Yes' if response.css(f'#row_optional_item_504 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Airshow'] = 'Yes' if response.css(f'#row_optional_item_72 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['GoGo Biz ATG-2000'] = 'Yes' if response.css(f'#row_optional_item_543 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['nice Touch CMS'] = 'Yes' if response.css(f'#row_optional_item_531 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['FANS 1/A'] = 'Yes' if response.css(f'#row_optional_item_398 td:nth-child({no}) ::text').get('') == '✔' else ' '
            #
            # item['2-place Divan'] = 'Yes' if response.css(f'#row_optional_item_39 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Belted Lav'] = 'Yes' if response.css(f'#row_optional_item_88 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Airborne Data Link'] = 'Yes' if response.css(f'#row_optional_item_68 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['GoGo Biz Avance L3'] = 'Yes' if response.css(f'#row_optional_item_520 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['RAAS'] = 'Yes' if response.css(f'#row_optional_item_557 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['4-Zone Cabin'] = 'Yes' if response.css(f'#row_optional_item_508 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Crew Rest Area'] = 'Yes' if response.css(f'#row_optional_item_113 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Dual Aft Divans'] = 'Yes' if response.css(f'#row_optional_item_653 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Mid-Cabin Divider'] = 'Yes' if response.css(f'#row_optional_item_232 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Shower'] = 'Yes' if response.css(f'#row_optional_item_299 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['1-32 in. monitor'] = 'Yes' if response.css(f'#row_optional_item_14 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['3-Cabin Monitors'] = 'Yes' if response.css(f'#row_optional_item_3 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['4-Cabin Monitors'] = 'Yes' if response.css(f'#row_optional_item_20 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['GoGo Biz ATG-4000'] = 'Yes' if response.css(f'#row_optional_item_206 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Auto Braking'] = 'Yes' if response.css(f'#row_optional_item_84 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Auto Throttle'] = 'Yes' if response.css(f'#row_optional_item_85 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['External Camera System'] = 'Yes' if response.css(f'#row_optional_item_184 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Iridium Satcom'] = 'Yes' if response.css(f'#row_optional_item_377 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Third FMS'] = 'Yes' if response.css(f'#row_optional_item_334 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['FMS-6100'] = 'Yes' if response.css(f'#row_optional_item_195 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Avionics Upgrade V3.6.1'] = 'Yes' if response.css(f'#row_optional_item_657 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Synthetic Vision Sys (SVS)'] = 'Yes' if response.css(f'#row_optional_item_309 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['HUD/EVS'] = 'Yes' if response.css(f'#row_optional_item_218 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Dual DME'] = 'Yes' if response.css(f'#row_optional_item_131 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Dual Radio Altimeter'] = 'Yes' if response.css(f'#row_optional_item_151 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Aircell Axxess II'] = 'Yes' if response.css(f'#row_optional_item_69 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Synthetic Vision V2'] = 'Yes' if response.css(f'#row_optional_item_515 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Enhanced Navigation'] = 'Yes' if response.css(f'#row_optional_item_174 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Wireless LAN'] = 'Yes' if response.css(f'#row_optional_item_507 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['State Room'] = 'Yes' if response.css(f'#row_optional_item_555 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['2-24 in. monitors'] = 'Yes' if response.css(f'#row_optional_item_29 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Predictive Windshear'] = 'Yes' if response.css(f'#row_optional_item_538 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['ASC-190'] = 'Yes' if response.css(f'#row_optional_item_82 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['PlaneDeck'] = 'Yes' if response.css(f'#row_optional_item_247 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Head-Up Display (HUD)'] = 'Yes' if response.css(f'#row_optional_item_210 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Enhanced Vision Sys (EVS)'] = 'Yes' if response.css(f'#row_optional_item_175 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['GNS-X'] = 'Yes' if response.css(f'#row_optional_item_205 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Additional Cabin Window'] = 'Yes' if response.css(f'#row_optional_item_62 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Vacuum Lav'] = 'Yes' if response.css(f'#row_optional_item_348 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['TCAS II 7.1'] = 'Yes' if response.css(f'#row_optional_item_322 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['NZ-2000 6.1'] = 'Yes' if response.css(f'#row_optional_item_242 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['ER Mod Year 2009>'] = 'Yes' if response.css(f'#row_optional_item_402 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Batch 3 SB'] = 'Yes' if response.css(f'#row_optional_item_87 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Office In The Sky'] = 'Yes' if response.css(f'#row_optional_item_244 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Collins CMS'] = 'Yes' if response.css(f'#row_optional_item_104 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Inmarsat Swift64 HSD'] = 'Yes' if response.css(f'#row_optional_item_191 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['BEVS'] = 'Yes' if response.css(f'#row_optional_item_89 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Primus Elite'] = 'Yes' if response.css(f'#row_optional_item_258 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Expanded Flight Data Recorder'] = 'Yes' if response.css(f'#row_optional_item_181 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Nuage Chaise Lounge'] = 'Yes' if response.css(f'#row_optional_item_655 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Combined Vision System'] = 'Yes' if response.css(f'#row_optional_item_644 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Refrigerator / Freezer'] = 'Yes' if response.css(f'#row_optional_item_535 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Enhanced Soundproofing'] = 'Yes' if response.css(f'#row_optional_item_533 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Full-Size Bed'] = 'Yes' if response.css(f'#row_optional_item_681 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Queen Bed'] = 'Yes' if response.css(f'#row_optional_item_680 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Vertical Weather'] = 'Yes' if response.css(f'#row_optional_item_539 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Lightning Detection System'] = 'Yes' if response.css(f'#row_optional_item_227 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['2nd Datalink'] = 'Yes' if response.css(f'#row_optional_item_536 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Surface Management System'] = 'Yes' if response.css(f'#row_optional_item_537 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Ovation Select CMS'] = 'Yes' if response.css(f'#row_optional_item_246 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['CDU-830 Display'] = 'Yes' if response.css(f'#row_optional_item_513 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # # item[''] = 'Yes' if response.css(f'#row_optional_item_72 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # # item[''] = 'Yes' if response.css(f'#row_optional_item_72 td:nth-child({no}) ::text').get('') == '✔' else ' '
            #
            #
            # item['CDU-820 Display'] = 'Yes' if response.css(f'#row_optional_item_93 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['NZ-2000'] = 'Yes' if response.css(f'#row_optional_item_239 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['NZ-2000 5.2'] = 'Yes' if response.css(f'#row_optional_item_240 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['NZ-2000 6.0'] = 'Yes' if response.css(f'#row_optional_item_241 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Third Laseref'] = 'Yes' if response.css(f'#row_optional_item_336 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Third Nav'] = 'Yes' if response.css(f'#row_optional_item_337 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['AFIS'] = 'Yes' if response.css(f'#row_optional_item_65 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['SATAFIS'] = 'Yes' if response.css(f'#row_optional_item_295 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Primus 870'] = 'Yes' if response.css(f'#row_optional_item_256 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Primus 880'] = 'Yes' if response.css(f'#row_optional_item_257 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Conference Group'] = 'Yes' if response.css(f'#row_optional_item_110 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['1-Cabin Monitor'] = 'Yes' if response.css(f'#row_optional_item_2 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['2-Cabin Monitors'] = 'Yes' if response.css(f'#row_optional_item_19 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Multi-Channel Satcom'] = 'Yes' if response.css(f'#row_optional_item_383 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Satellite TV'] = 'Yes' if response.css(f'#row_optional_item_296 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['APU 36-150'] = 'Yes' if response.css(f'#row_optional_item_16 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Securaplane'] = 'Yes' if response.css(f'#row_optional_item_298 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Tail Tank'] = 'Yes' if response.css(f'#row_optional_item_311 td:nth-child({no}) ::text').get('') == '✔' else ' '
            # item['Product URL'] = response.url

            yield item
