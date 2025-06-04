
import csv
import re
import time
import json
import scrapy
import datetime
from datetime import datetime
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Amstat_Market_Scrapy(scrapy.Spider):
    name = 'Amstat_Market_Scrapy'
    Current_Market_url = ("https://premier.amstatcorp.com/market/my-market-details?ignoreUserEdits=false&typesToLoad=current-market-snapshot"
           "%2Cphysical-performance-spec%2Coperation-cost-dtls%2Cmodel-fleet-summary%2Cmodel-images&marketGuid={}")
    Market_History_url = ("https://premier.amstatcorp.com/market/my-market-details?_dc=1708347667412&ignoreUserEdits=false&typesToLoad=transaction-history"
           "%2Cmarket-chart-data%2Crecent-market-changes&marketGuid={}")
    Market_headers = {
        'authority': 'premier.amstatcorp.com',
        'accept': 'application/json,application/xml',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,nl;q=0.7',
        'cookie': 'ScreenWidthInfo=1366; __hstc=265555408.e698e92a9b5bbbe43071861fe1fc853a.1705933371385.1705933371385.1705933371385.1; hubspotutk=e698e92a9b5bbbe43071861fe1fc853a; __hs_cookie_cat_pref=1:true,2:true,3:true; _ga=GA1.2.1388444742.1705933403; _ga_TYWTSL6DXK=GS1.2.1705933403.1.0.1705933403.60.0.0; ARRAffinity=18311a48ed0b1109ca871590f7012f044d70c16a16fb4686d86db54e58e999e6; PremierSession=sfpwur020ezqflmm3mftwihw; .AspNet.Cookies=dMlka6LjmLN4YfeSc6BPdsUmc5blfLntN2Kjs9m-WuZzWZsuVWInuuwUMOuFnKNFfLE2sFC3puDLJiWqjfvPcE2xjpEvTvGr4ymxFBVhCBQVPRJHzp302UwWjIxOzs1REYNqEoU8SU_thOgc_lpZoE_eY07Fo-MFGF5bxzOnQJp_hXw0MdxxLH49T2WkNh8umSvYq0LXl0Hv81CO15zAf-Ai3RCuyMS3eMnl7N669AziPe4veGXXDhUpi9Unn9g90tDf37XK0KqUrSVj1u4Qn_37S7EWJAhnGete0njcbUdiRJcoXe3IozpCT-afsJvfEn-GEz6jv4eVD0TM3Vjp7tZcRprn92n80IOQpRJPQauDCtfbCfn0pmts1sPYGdE93PHdnCaUIju3L87A64n91TJfkQc9oU79XFu_DWRUnFdtQILzqgK_9O1rwUsBhOMWg2Wsz8FeGtywQiNlC02tO0DliT7e1pCdDOHiLnouVy2h6kRCxi7hvIKJ0527WBu6cUEcu9osjKw7ZBRObXh5UcyNPLRLxyy5AoHkv7DgCjtX80QfZYxCR-ENNwwwVSWbktwMSAKQ2O6fbREKDuzSaR9-OAmHLsnoeflPXvX9YyouWIWSs04qkUex12-PmvIuE1HadsfSs85LM9Ekhv1HJFAEStunbZfbJNyMqUnsgkwkUcIa_voel0lQQFuDpd1QcMbMKdP_04c4U94BrnG3a_y2tSxlR_EwKEIv89t7_zMYUoX6kMdDVo8I6khYimKREjwEyuVi-8i9AYS3e8os6GccqqrHaD_b6iEBgYlnK14hZSVuRuQOtUXrwsU-VJErEnVmN9MuiXT__ASfNJm07K0VCgf27YzXqTSMKTTfN-zSeQA2372tJRn98yH94nPWL7bE7MIGeEzRK-EGhNDieACawXfC56o3Tn2euYrZIWu8W-lCT7WaDq0hS0ZR3tY6giWL_e0IwrdMMmohC9lGo4Saol2NVcwdnrg6wtItU626wlZVICXlRQZ6qEMOLkRCb84FAHyiWE0e8Jnb68N31p4CW0EMB4df78gYqiHx_Abx1sjv-wLQk0_wHA8ZjD4fbkjpVX45nqB09Ge3Vi2YT5hfJls; PremierSubscriber=NxMOqa1WS5TXutosYnfe+TkINUrOSt6W; ScreenWidthInfo=1366',
        'csrftoken': '6-UxLxGulPbapETYpeNPIxjo8cHl-IgsprUsTfe_BsCLdcMN7xIanei1azuyomfPt2zeX_0rrja8uPe4gJt2rf_Kvlk1:-ckncQvz7ZWSFIbbWR8zKqwt6kq4gTcT_3HSCCGtBck86ZiNChpqELlPWZk_WHyVDfEwvtnsbAT8Q6IfJu5LEUj2jGASsyx9DObC9wDzp0KLac9Aga_tbywqPCu30vmvb15zPA2',
        # 'referer': 'https://premier.amstatcorp.com/market/c1b2f81c-d753-4963-a5ed-655f953fa2f1',
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

    custom_settings = {'FEED_URI': f'output/Amstat_Market {datetime.now().strftime("%d-%m-%Y")}.csv',
                       'FEED_FORMAT': 'csv',
                       'FEED_EXPORT_ENCODING': 'utf-8-sig', }

    def start_requests(self):
        csv_file_path = 'input/Amstat_Market_Record.csv'
        with open(csv_file_path, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            URLs = [row['Make & Model URL'] for row in csv_reader]

        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.get('https://premier.amstatcorp.com/dashboard')
        # driver.maximize_window()

        # Find the email and password input fields and enter credentials
        email_field = driver.find_element('id', 'email')
        password_field = driver.find_element('id', 'password')
        email_field.send_keys('wsoh@jet8.com')
        password_field.send_keys('931557Jetislife!')
        login_button = driver.find_element('id', 'login-button')
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
        time.sleep(5)

        driver.get('https://premier.amstatcorp.com/market/37fac389-483e-4f7d-bdee-d74867700979')
        time.sleep(7)

        headers = self.Market_headers
        cookiesss = ''
        for cookie in driver.get_cookies():
            cookiesss += f"{cookie.get('name')}={cookie.get('value')}; "
        headers['cookie'] = cookiesss
        self.Market_headers['cookie'] = cookiesss

        headers['csrftoken'] = csrf_token
        self.Market_headers['csrftoken'] = csrf_token

        for mm_url in URLs:
            time.sleep(1)
            uuid_pattern = re.compile(r'/market/([a-f0-9-]+)')
            matches = uuid_pattern.findall(mm_url)
            if matches:
                Guid = matches[0]
                yield scrapy.Request(url=self.Current_Market_url.format(Guid), headers=self.Market_headers, callback=self.parse,
                                     meta={'mm_url': mm_url, 'Guid':Guid})
            else:
                print("Guid of the URL is not Correct or Not Found")

    def parse(self, response):
        data = json.loads(response.body)
        item = dict()
        item['Date Ingested'] = datetime.now().strftime("%d/%m/%Y")
        make_model_mix = data.get('data').get('model-fleet-summary')[1]
        make_model = make_model_mix.split(' - ', 1)
        item['Make'] = make_model[0]
        item['Model'] = make_model[1] if len(make_model) > 1 else ''
        item['Aircraft Group/Segment'] = data.get('data').get('model-fleet-summary')[21]
        item['Production Status'] = data.get('data').get('model-fleet-summary')[13]
        item['Total Products'] = data.get('data').get('model-fleet-summary')[12]
        item['Year Range'] = str(data.get('data').get('model-fleet-summary')[7]) +'-'+ str(data.get('data').get('model-fleet-summary')[8])

        if data.get('data').get('model-fleet-summary')[9]:
            TTAF_Min = '{:,}'.format(int(data.get('data').get('model-fleet-summary')[9]))
        else:
            TTAF_Min = " "
        if data.get('data').get('model-fleet-summary')[10]:
            TTAF_Max = '{:,}'.format(int(data.get('data').get('model-fleet-summary')[10]))
        else:
            TTAF_Max = " "

        item['TTAF Range'] = str(TTAF_Min) +' - '+ str(TTAF_Max)
        item['Active Fleet'] = data.get('data').get('current-market-snapshot')[0]
        item['For Sale'] = data.get('data').get('current-market-snapshot')[1]
        item['For Sale - Unverified'] = data.get('data').get('current-market-snapshot')[2]
        item['For Lease'] = data.get('data').get('current-market-snapshot')[3]
        item['Total For Sale/Lease'] = data.get('data').get('current-market-snapshot')[4]
        item['% For Sale/Lease'] = round((data.get('data').get('current-market-snapshot')[5]),2)
        item['Absorption Rate (months)'] = round((data.get('data').get('current-market-snapshot')[6]),2)

        Guid = response.meta.get('Guid')
        yield scrapy.Request(url=self.Market_History_url.format(Guid), headers=self.Market_headers, callback=self.detail_parse,
                             meta={'item':item, 'mm_url':response.meta.get('mm_url')})

    def detail_parse(self, response):
        data = json.loads(response.body)
        item = response.meta.get('item')

        item['Resale_Retail (YTD)'] = data.get('data').get('transaction-history')[7]
        item['Resale_Retail (2023)'] = data.get('data').get('transaction-history')[18]
        item['Resale_Retail (2022)'] = data.get('data').get('transaction-history')[29]

        item['Retail_to_Retail (YTD)'] = data.get('data').get('transaction-history')[0]
        item['Retail_to_Retail (2023)'] = data.get('data').get('transaction-history')[11]
        item['Retail_to_Retail (2022)'] = data.get('data').get('transaction-history')[22]

        item['Dealer_to_Retail (YTD)'] = data.get('data').get('transaction-history')[5]
        item['Dealer_to_Retail (2023)'] = data.get('data').get('transaction-history')[16]
        item['Dealer_to_Retail (2022)'] = data.get('data').get('transaction-history')[27]

        item['Other_to_Retail (YTD)'] = data.get('data').get('transaction-history')[8]
        item['Other_to_Retail (2023)'] = data.get('data').get('transaction-history')[19]
        item['Other_to_Retail (2022)'] = data.get('data').get('transaction-history')[30]

        item['Net_Dealer_Inv (YTD)'] = data.get('data').get('transaction-history')[6]
        item['Net_Dealer_Inv (2023)'] = data.get('data').get('transaction-history')[17]
        item['Net_Dealer_Inv (2022)'] = data.get('data').get('transaction-history')[28]

        item['DOM - Sold (Average) (YTD)'] = data.get('data').get('transaction-history')[9]
        item['DOM - Sold (Average) (2023)'] = data.get('data').get('transaction-history')[20]
        item['DOM - Sold (Average) (2022)'] = data.get('data').get('transaction-history')[31]

        item['DOM - Sold (Median) (YTD)'] = data.get('data').get('transaction-history')[10]
        item['DOM - Sold (Median) (2023)'] = data.get('data').get('transaction-history')[21]
        item['DOM - Sold (Median) (2022)'] = data.get('data').get('transaction-history')[32]

        item['Make & Model URL'] = response.meta.get('mm_url')
        yield item