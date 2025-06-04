##      Amstat_Aircraft

import csv
import os
import re
import time
import json
import scrapy
import datetime
from datetime import datetime
from scrapy.http.cookies import CookieJar
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, TimeoutException
from selenium.common.exceptions import NoSuchElementException

class Amstat_Aircraft(scrapy.Spider):
    name = 'Amstat_Aircraft'
    custom_settings = {'FEED_URI': f'output/Amstat_Aircraft {datetime.now().strftime("%d-%m-%Y")} Test.csv',
                       'FEED_FORMAT': 'csv',
                       'FEED_EXPORT_ENCODING': 'utf-8-sig', }
    url = ("https://premier.amstatcorp.com/search/aircraft/33311198-31fd-45f3-ad4d-69dfa141e420?_dc=1708115302248&"
           "considerUserEdits=true&considerAsSearchRun=false&masterSearchId=&layoutId=0&criteria=&page={}&start={}&limit={}")
    headers = {
        'authority': 'premier.amstatcorp.com',
        'accept': 'application/json,application/xml',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'ScreenWidthInfo=1366; ARRAffinity=efc65b9db919d3d2bce9b71210569c1ed26cdefa1212a61f0c989a888afd6493; PremierSession=dcmim52g5a4ibcnatn1ctgvw; .AspNet.Cookies=DaZ7tdB5la2pd_6vCtqRJ4GXjABc3qmDpvmAvyB8CxtfLus50tbeWXpakIwKrVWAsUrsUDGaRqSJDHy3E3svzHbMgUcT4KMQmCBAMSCBVrAhJdLr7SW2ax7YaHVb0nDVGMppp0acz3cRwNVu3Rr5MK6u-oezkXKwp5FfDB4xMfljM3XUtDuxD6N1azwf0pAFz6bw577MOQW_ssIJKZBdAnneiIG9xOh4XieJbSkdRSIUc4tU1TRpPaYfaTPOT1ckiHd5lqN1rd01r50CNYC-n5gqjSMSD6GpQOlhWw0Sjgjg7V3Y5vxOTjVQesPhq8Zt-sOfdr69v-easccs-E7aR_XNhjy7rgFfQD9nUg1pDmG5PV8Q5XB2KC5zLuERTh8NEvWHLmL1huW48_kQu-M7w60ASZtc8qiTyqc29XIvxKQTKz5qfJjX9qvuh6PhM5H31F56Bcz_n7OcaVPvUtiSLVYl1HRQCXPTMlNeSV5Gj0PeeGqrkSz4Dl57r_llaGKnxnPhVhot9ZdOgTbx5PprR_UGGsCy7Kd80n0eba0a8OwKEqETfHxfRTQ5V4KfKq0oyAlQCOvF-wmAIxn6vJxyo6Hxn_oIWna8T_7Y3YFq_7v694p4sWCcAVdKVJof-1E-GeQdXnMEn0soQ1tKViB9vOMABsboRXNfyoyBNAuPBAFw9-riSbNSQs7mnGUUIHCCYnOscdS5idGa18NVRFytk9txlg9YhRO9umpih1SGfvnf-uUQILmrZebX4--SLayBTmi0WCX0inckLpZlO_eXnrlT_pWKNOHBzX1iZU32dk0FJgNq0jw3oM3CKqXG4JKorogj5V6cRDWnwMCEfWT--blOt0n3Jvrrw0svCnj5JqOYZdu5EDOZMk_4VoK6ln6qGPw4mouyIgWsUyvg26ZirK4iCzFQJR84NgGV5PIcknbBr91OOn4VpI_NWIYXOHbOlP0DptL25M7nHgUYHX_4L257cIoUg6DfrUtXuPDBT1YWeeXeWndBJ8HE0Frzq9mz4pv6B_OA-ga1WffrsTYH7CHQAT1S26FNsD0MjsGLQg2f0FdNPdTDozqfn0vthOyslDf0zsvIjP38Ht32yDh6BQv4V8g; PremierSubscriber=NxMOqa1WS5S5XMS4LjRKGSCWCV0CxKbg; ScreenWidthInfo=1366',
        # 'csrftoken': 'SDxiaAeFQDlMRNReK8eb6j7Q6B1M0YZgCbnbPm5CjxWqkpJMOhrh3rG1CBJOrHW_wyiexT9AclyyZ68FnN0_Y0mNZQI1:lSQZA_TaHnAXJSgpl-eBaYjOLrdevzIhvrv9-uqt4x-_JWfbDgJUEsSnfqc84vqN8DrnfD8sJzhP4FYkU4c_NfxaAHg1lA8aA6DSQzR3HUQxxcsO2F4LGk0mXf43AGmoyizn3Q2',
        # 'referer': 'https://premier.amstatcorp.com/aircraft-advanced-search/33311198-31fd-45f3-ad4d-69dfa141e420?masterSearchId=&sortProperty=DaysOnMarket&sortDirection=ASC&selectedEntityId=252473&selectedEntityType=aircraft&restoreEntityId=252473&openStatus=true',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'user-time-zone-offset': '-300',
        'x-requested-with': 'XMLHttpRequest'
    }
    aircraft_api_url = "https://premier.amstatcorp.com/aircraft/{}/aircraft-sections"

    def start_requests(self):
        #   Using Selenium to Login and extract desired cookies and csrftoken
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(options=options)
        driver.get('https://premier.amstatcorp.com/dashboard')
        driver.maximize_window()

        email_field = driver.find_element('id', 'email')  # Use the correct identifier for your email input field
        password_field = driver.find_element('id','password')  # Use the correct identifier for your password input field
        email_field.send_keys('wsoh@jet8.com')
        password_field.send_keys('931557Jetislife!')
        login_button = driver.find_element('id', 'login-button')  # Use the correct identifier for your login button
        login_button.click()
        time.sleep(10)

        primary_mach_button_locator = (By.ID, 'button-1029-btnWrap')
        wait = WebDriverWait(driver, 10)
        time.sleep(5)
        primary_mach_button = wait.until(EC.element_to_be_clickable(primary_mach_button_locator))
        primary_mach_button.click()
        time.sleep(10)

        agree_button_locator = (By.ID, 'button-1037-btnIconEl')
        wait = WebDriverWait(driver, 10)
        agree_button = wait.until(EC.element_to_be_clickable(agree_button_locator))
        agree_button.click()
        time.sleep(5)

        page_source = driver.page_source
        response = Selector(text=page_source)
        csrf_token = response.css('script:contains("CSRFToken")::text').re_first(r'CSRFToken":"(.*?)"')

        time.sleep(2)
        driver.get('https://premier.amstatcorp.com/aircraft-advanced-search/33311198-31fd-45f3-ad4d-69dfa141e420?masterSearchId'
                   '=&sortProperty=DaysOnMarket&sortDirection=ASC&selectedEntityId=252473&selectedEntityType=aircraft'
                   '&restoreEntityId=252473&openStatus=true')

        time.sleep(5)

        headers = self.headers
        cookiesss = ''
        for cookie in driver.get_cookies():
            cookiesss += f"{cookie.get('name')}={cookie.get('value')}; "
        headers['cookie'] = cookiesss
        self.headers['cookie'] = cookiesss

        headers['csrftoken'] = csrf_token
        self.headers['csrftoken'] = csrf_token

        # driver.quit()
        yield scrapy.Request(url=self.url.format(1,0,60), headers=self.headers, callback=self.parse,
                             meta={'headers':headers,'page_no':1, 'present_count':0})

    def parse(self, response):
        updated_headers = response.meta.get('headers')
        json_string = (response.body).decode('utf-8')
        data = json.loads(json_string)

        for aircraft in data['result']['rows']:
            yield scrapy.Request(url=self.aircraft_api_url.format(aircraft[1]), headers=self.headers, callback=self.detail)

        ########### PAGINATION
        Total_count = data['result']['totalCount']
        Present_count = response.meta.get('present_count') + data['result']['count']
        page_no = response.meta.get('page_no')
        if Present_count < Total_count:
            yield scrapy.Request(url=self.url.format(page_no+1,Present_count,60), headers=updated_headers, callback=self.parse,
                                 meta={'headers':updated_headers,'page_no':page_no+1, 'present_count':Present_count})

    def detail(self, response):
        json_string = (response.body).decode('utf-8')
        data = json.loads(json_string)
        if data:
            item = dict()
            item['Date Ingested'] = datetime.now().strftime("%d/%m/%Y")
            item['Make'] = None
            item['Model'] = None
            item['Serial #'] = None
            item['Registration Number'] = None
            item['Year'] = None
            item['Asking Price $'] = None
            item['Asking Price Note'] = ''
            for aircraft_section in data['AircraftSections']:
                if isinstance(aircraft_section, dict):
                    if aircraft_section['Name'] == 'Aircraft General':
                        for properties in aircraft_section['Properties']:
                            if properties.get('PropertyName') == 'MakeName':
                                item['Make'] = properties.get('AmstatValue')
                            if properties.get('PropertyName') == 'ModelName':
                                item['Model'] = properties.get('AmstatValue')
                            if properties.get('PropertyName') == 'SerialNumber':
                                item['Serial #'] = properties.get('AmstatValue')
                            if properties.get('PropertyName') == 'RegistrationNumber':
                                item['Registration Number'] = properties.get('AmstatValue')
                            if properties.get('PropertyName') == 'YOM':
                                item['Year'] = properties.get('AmstatValue')
                            if properties.get('PropertyName') == 'TTAFN':
                                if properties.get('AmstatValue'):
                                    item['TTAF'] = '{:,}'.format(int(properties.get('AmstatValue')))
                            if properties.get('PropertyName') == 'ForSaleStatus':
                                item['Status'] = properties.get('AmstatValue')
                            if properties.get('PropertyName') == 'DaysOnMarket':
                                item['Days On Market (FS)'] = properties.get('AmstatValue')
                            if properties.get('PropertyName') == 'AskingPrice':
                                asking_price = properties.get('AmstatValue')
                                if asking_price == 'Inquire' or asking_price == 'Make Offer':
                                    item['Asking Price Note'] = properties.get('AmstatValue')
                                else:
                                    if properties.get('AmstatValue'):
                                        item['Asking Price $'] = '{:,}'.format((int(properties.get('AmstatValue'))))
                            if properties.get('PropertyName') == 'State':
                                item['State'] = properties.get('AmstatValue')
                            if properties.get('PropertyName') == 'OpDefOwner':
                                item['Owner'] = properties.get('AmstatValue')
                            if properties.get('PropertyName') == 'OpDefOwner':
                                item['Broker/Dealer'] = properties.get('AmstatValue')
                            if properties.get('PropertyName') == 'LastModified':
                                input_string = properties.get('AmstatValue')
                                try:
                                    datetime_object = datetime.strptime(input_string, '%Y-%m-%dT%H:%M:%S.%f')
                                except ValueError:
                                    datetime_object = datetime.strptime(input_string, '%Y-%m-%dT%H:%M:%S')
                                # Extract only the date part
                                date_only = datetime_object.date()
                                # Convert date to string
                                item['Date Entered'] = date_only.strftime('%d/%m/%Y')

                        for sections in aircraft_section['Sections']:
                            for section_properties in sections['Properties']:
                                if section_properties.get('PropertyName') == 'ACCountry':
                                    item['Aircraft Country'] = section_properties.get('AmstatValue')
                                if section_properties.get('PropertyName') == 'City':
                                    item['City'] = section_properties.get('AmstatValue')
                                if section_properties.get('PropertyName') == 'GlobalRegion':
                                    item['Aircraft Region'] = section_properties.get('AmstatValue')
                                if section_properties.get('PropertyName') == 'ACGroup':
                                    item['Aircraft Group'] = section_properties.get('AmstatValue')
                                if section_properties.get('PropertyName') == 'ACSegment':
                                    item['Aircraft Segment'] = section_properties.get('AmstatValue')

                        yield item
