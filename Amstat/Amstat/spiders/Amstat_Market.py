#######         Amstat_Market

import csv
import datetime
import os
import time
import json
import scrapy
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, TimeoutException
from selenium.common.exceptions import NoSuchElementException

class Amstat_Market(scrapy.Spider):
    name = 'Amstat_Market'
    url = "https://premier.amstatcorp.com/aircraft-advanced-search/75d58bf6-a548-4a49-bb05-f92a5876c440?considerUserEdits=true&considerAsSearchRun=false&masterSearchId=&layoutId=0&searchId=&entity=&page=1&start=0&limit=600"
    headers = {
        'authority': 'premier.amstatcorp.com',
        'accept': 'application/json,application/xml',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cookie': '__hstc=265555408.e698e92a9b5bbbe43071861fe1fc853a.1705933371385.1705933371385.1705933371385.1; hubspotutk=e698e92a9b5bbbe43071861fe1fc853a; __hs_cookie_cat_pref=1:true,2:true,3:true; _ga=GA1.2.1388444742.1705933403; _ga_TYWTSL6DXK=GS1.2.1705933403.1.0.1705933403.60.0.0; ScreenWidthInfo=1366; ARRAffinity=18311a48ed0b1109ca871590f7012f044d70c16a16fb4686d86db54e58e999e6; PremierSession=4yymn5bzi5nwoh1xudtkudnm; .AspNet.Cookies=mkfuVtDzf93yH8_MoKHxyNnLUAG0bw0n2NFXnU7jvHqNdhrYIQWtU1zfY8keRorJA0VFFFd6htmm5qsPbW-xCJ4y2PnqJBxGNl9R2lJ228T7-yJZxelBo9y8Xpqrz7j0SvnBtjzr3_X7MFEBtmDnC6Q1pvcuyiDrwXx4jPMTOCAu5mtM7U0y1RWVkC6K7F-N_tE1JX2XFETdDTKEneRc322ngT-PqaE9wWPXzOduPPmJ1HJP1DEqw3KvTste3aBXZPo2LYE4jNfCZcUnwNl9fwzOm9wsZEZ5ozHcMAAn72O_iFx2RBRZANLMgjaGe9uQe5q-djkzxrcirFLRZ2WYAOkPcVuY8mW-kdQAd28IZSqZnn-O-TRb9NLBhDXMCbKcuivD1WTUil6U7TEOZxztZZQVX-O7QjV-amjFAFLE5RY5g72o0VlDd18GN_CtHXNA7BnonMQMbJggCpp3jttOztWEQZqgcrXgsr5FUfNU83cY2ZrmyQKRCVSnlbey2eBCPv0sAWy4nRFPBy9HHdWCVHbjGdQiM9IvF4p8SEqQ2BvlV_BA5koEiScY1qKYPJ4gS5Qxf9MRdDzoIA_Mef-TV37DieFFTUQIFzAdMg17R_-2D5HMt1DLyAjBh_k1TO52ztII_cthMF6e1lnam8SCUiuzWjElDJw5RCg0y8wL8GGVagS_CoAgMfGBDfINVF_fMOlNqH8zsg2qV1G_6OxvFUIzfDqcMOXWVJgiD9mAOrMgQX5VpqcPKKQGyKQj5wxMMxwYg_K0P3cHxVrxzruWawyfk8DBDhM1ixx9m8UUBhH6e2j7_Je7vcKnprReI14aoyDEOp9amCP4kc6gTMWvQo5DLDMxfHnojru-R59ft5Vbjc13T2-Bf1cjX9Iz2D5sXPydDkiovDxQgvQFCcza3aZSl6dXL7DI6kdGUx1vVt_Su1aYTrFDJl3cCYWpl5KOSqPe9HOZ1phuj2wi_S9DjT1ea_3t6McnrOd4a9FdajcsZ_va7_ToEBCSddfAk3WbsjLV5PpnjVgA5HUC18ibQJ7ODH8UiyKgihCwyENjPIT3Obojg6baW_YN8TX4NxbsF-bzTNeNzaIuXuMHl8o3evmBv4Q; PremierSubscriber=NxMOqa1WS5QO22WknFe1lqs37O/JWv5U',
        'csrftoken': 'diSpxxc5HErTfp648pg4xMD5UOODO690zpecpfD_XEmn233OOQBPvtnYGaDNL8JjfwJrKDuQ4qAj568MC9buLnq7lxI1:rXWGP9QdH2sjTRDIwLJIEDf42CIEJqlLaFeL6enhHJ6sOEeBANe1U0TZLhtbx0KE-qPdV0Fm34taDF4UGvau1TGFnytsKb79ng-jIqc64h2gvrBDKDr-BVJwW3UPSxeh4EjDPA2',
        'referer': 'https://premier.amstatcorp.com/aircraft-advanced-search/75d58bf6-a548-4a49-bb05-f92a5876c440?masterSearchId=',
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

    def start_requests(self):
        '''''''         MARKET PART COMPLETED       '''
        with open('input/makes_and_models.json', 'r') as file:
            data = json.load(file)

        csv_filename = f'output/Amstat_Market {datetime.datetime.now().strftime("%d-%m-%Y")}.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Date Ingested','Make','Model','Aircraft Group/Segment','Production Status','Total Products','Year Range','Active Fleet',
            'For Sale','For Sale - Unverified','For Lease','Total For Sale/Lease','% For Sale/Lease','Absorption Rate (months)',
            'Resale_Retail (YTD)','Resale_Retail (2023)', 'Resale_Retail (2022)','Retail_to_Retail (YTD)',
             'Retail_to_Retail (2023)','Retail_to_Retail (2022)','Dealer_to_Retail (YTD)', 'Dealer_to_Retail (2023)',
             'Dealer_to_Retail (2022)','Other_to_Retail (YTD)', 'Other_to_Retail (2023)', 'Other_to_Retail (2022)',
             'Net_Dealer_Inv (YTD)','Net_Dealer_Inv (2023)','Net_Dealer_Inv (2022)', 'DOM - Sold (Average) (YTD)',
             'DOM - Sold (Average) (2023)', 'DOM - Sold (Average) (2022)', 'DOM - Sold (Median) (YTD)',
             'DOM - Sold (Median) (2023)', 'DOM - Sold (Median) (2022)','Make & Model URL']

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            options = webdriver.ChromeOptions()
            options.add_experimental_option("detach", True)

            driver = webdriver.Chrome(options=options)
            driver.get('https://premier.amstatcorp.com/dashboard')
            driver.maximize_window()

            # Find the email and password input fields and enter credentials
            email_field = driver.find_element('id', 'email')  # Use the correct identifier for your email input field
            password_field = driver.find_element('id', 'password')  # Use the correct identifier for your password input field
            email_field.send_keys('wsoh@jet8.com')
            password_field.send_keys('931557Jetislife!')
            login_button = driver.find_element('id', 'login-button')  # Use the correct identifier for your login button
            login_button.click()
            time.sleep(10)

            button_locator = (By.ID, 'button-1029-btnWrap')
            wait = WebDriverWait(driver, 10)
            time.sleep(5)
            primary_mach_button = wait.until(EC.element_to_be_clickable(button_locator))
            # Click the button
            primary_mach_button.click()

            time.sleep(12)
            button_locator = (By.ID, 'button-1037-btnIconEl')
            wait = WebDriverWait(driver, 10)
            agree_button = wait.until(EC.element_to_be_clickable(button_locator))
            agree_button.click()
            time.sleep(5)
            driver.get('https://premier.amstatcorp.com/market')
            time.sleep(2)
            for Make_ID, models in data.items():
                for Model_ID in models:
                    # time.sleep(5)

                    time.sleep(3)
                    make_input = wait.until(EC.presence_of_element_located((By.NAME, 'MakeID')))
                    make_input.clear()
                    make_input.send_keys(Make_ID)
                    time.sleep(1)
                    make_input.send_keys(Keys.RETURN)
                    time.sleep(2)
                    # Wait for the model input to be ready
                    model_input = wait.until(EC.presence_of_element_located((By.NAME, 'ModelID')))
                    model_input.clear()
                    model_input.send_keys(Model_ID)
                    time.sleep(1)
                    model_input.send_keys(Keys.RETURN)

                    time.sleep(5)
                    go_button = driver.find_element(By.XPATH, '//span[contains(text(),"Go")]/following-sibling::span')
                    go_button.click()

                    time.sleep(10)

                    try:
                        error_element = driver.find_element(By.XPATH,'//*[contains(text(),"Please select make and model to proceed")]')
                        print("Error element found. Please select make and model to proceed.")
                        disclaimer_ok_button = driver.find_element(By.XPATH, '//span[contains(text(),"OK")]/following-sibling::span')
                        disclaimer_ok_button.click()
                        time.sleep(3)
                        driver.get('https://premier.amstatcorp.com/market')
                        pass
                    except NoSuchElementException:
                        pass

                    page_source = driver.page_source
                    response = Selector(text=page_source)

                    item = dict()
                    item['Date Ingested'] = datetime.datetime.now().strftime("%d/%m/%Y")
                    make_model_mix = response.css('div.fleet-summary-header span::text').extract_first('')
                    make_model = make_model_mix.split(' - ', 1)
                    item['Make'] = make_model[0]
                    item['Model'] = make_model[1] if len(make_model) > 1 else ''

                    item['Aircraft Group/Segment'] = response.xpath("//*[contains(text(),'Aircraft Group / Segment:')]/following-sibling::span/text()").get('')
                    item['Production Status'] = response.xpath('//div[@class="fleet-summary-content-header" and span[@class="header-lbl" and text()="Production Status:"]]/text()').get('')
                    item['Total Products'] = response.xpath('//div[@class="small-gray-text range-header" and contains(text(), "Total Prod.")]/div[@class="medium-black-bold-text"]/a/text()').get('')
                    item['Year Range'] = response.xpath('//div[contains(text(), "Year Range")]/div[@class="medium-black-bold-text"]/text()').get('')
                    item['Active Fleet'] = response.xpath('//span[text()="Active Fleet:"]/following-sibling::a/text()').get('')
                    item['For Sale'] = response.xpath('//span[text()="For Sale:"]/following-sibling::a/text()').get('')
                    item['For Sale - Unverified'] = response.xpath('//span[text()="For Sale - Unverified:"]/following-sibling::a/text()').get('')
                    item['For Lease'] = response.xpath('//span[text()="For Lease:"]/following-sibling::a/text()').get('')
                    item['Total For Sale/Lease'] = response.xpath('//div[contains(@class, "range-header") and contains(text(), "Total For Sale/Lease")]/div[@class="medium-black-bold-text"]/a/text()').get('')
                    item['% For Sale/Lease'] = response.xpath('//div[contains(@class, "range-header") and contains(text(), "% For Sale/Lease")]/div[@class="medium-black-bold-text"]/text()').get('')
                    item['Absorption Rate (months)'] = response.xpath('//div[contains(@class, "range-header") and contains(text(), "Absorption Rate (months)")]/div[@class="medium-black-bold-text"]/text()').get('')

                    item['Resale_Retail (YTD)'] = response.xpath("//td[contains(text(), 'Resale Retail')]/following-sibling::td[1]/a/text()").get('')
                    item['Resale_Retail (2023)'] = response.xpath("//td[contains(text(), 'Resale Retail')]/following-sibling::td[2]/a/text()").get('')
                    item['Resale_Retail (2022)'] = response.xpath("//td[contains(text(), 'Resale Retail')]/following-sibling::td[3]/a/text()").get('')

                    item['Retail_to_Retail (YTD)'] = response.xpath("//td[contains(text(), 'Retail to Retail')]/following-sibling::td[1]/a/text()").get('')
                    item['Retail_to_Retail (2023)'] = response.xpath("//td[contains(text(), 'Retail to Retail')]/following-sibling::td[2]/a/text()").get('')
                    item['Retail_to_Retail (2022)'] = response.xpath("//td[contains(text(), 'Retail to Retail')]/following-sibling::td[3]/a/text()").get('')

                    item['Dealer_to_Retail (YTD)'] = response.xpath("//td[contains(text(), 'Dealer to Retail')]/following-sibling::td[1]/a/text()").get('')
                    item['Dealer_to_Retail (2023)'] = response.xpath("//td[contains(text(), 'Dealer to Retail')]/following-sibling::td[2]/a/text()").get('')
                    item['Dealer_to_Retail (2022)'] = response.xpath("//td[contains(text(), 'Dealer to Retail')]/following-sibling::td[3]/a/text()").get('')

                    item['Other_to_Retail (YTD)'] = response.xpath("//td[contains(text(), 'Other to Retail')]/following-sibling::td[1]/a/text()").get('')
                    item['Other_to_Retail (2023)'] = response.xpath("//td[contains(text(), 'Other to Retail')]/following-sibling::td[2]/a/text()").get('')
                    item['Other_to_Retail (2022)'] = response.xpath("//td[contains(text(), 'Other to Retail')]/following-sibling::td[3]/a/text()").get('')

                    item['Net_Dealer_Inv (YTD)'] = response.xpath("//td[contains(text(), 'Net Dealer Inv.')]/following-sibling::td[1]/text()").get('')
                    item['Net_Dealer_Inv (2023)'] = response.xpath("//td[contains(text(), 'Net Dealer Inv.')]/following-sibling::td[2]/text()").get('')
                    item['Net_Dealer_Inv (2022)'] = response.xpath("//td[contains(text(), 'Net Dealer Inv.')]/following-sibling::td[3]/text()").get('')

                    DOM = response.css('.row-line::text').getall()
                    item['DOM - Sold (Average) (YTD)'] = DOM[-6].replace('YTD:','')
                    item['DOM - Sold (Average) (2023)'] = DOM[-4].replace('2023:','')
                    item['DOM - Sold (Average) (2022)'] = DOM[-2].replace('2022:','')
                    item['DOM - Sold (Median) (YTD)'] = DOM[-5].replace('YTD:','')
                    item['DOM - Sold (Median) (2023)'] = DOM[-3].replace('2023:','')
                    item['DOM - Sold (Median) (2022)'] = DOM[-1].replace('2022:','')

                    item['Make & Model URL'] = driver.current_url

                    print(f'Required data is : {item}')
                    writer.writerow(item)

                    time.sleep(5)
                    try:
                        close_button = driver.find_element(By.XPATH, '//span[contains(@class,"x-tab-close-btn")]')
                        close_button.click()
                        time.sleep(3)
                    except NoSuchElementException:
                        print('Unable to locate (x-tab-close-btn) element ')

            driver.close()

    def parse(self, response):
        pass


