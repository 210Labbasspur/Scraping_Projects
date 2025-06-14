import time
import scrapy
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class lakeandwells(scrapy.Spider):
    name = 'lakeandwells'
    custom_settings = {
        'FEED_URI': f'output/Lake & Wells Floorplans - {datetime.datetime.now().strftime("%d-%m-%Y")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }
    start_urls = ['https://www.example.com']


    def parse(self, response):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.get('https://liveatlakeandwells.com/floor-plans')
        time.sleep(2)

        driver.execute_script("window.scrollBy(0, 1300);")  # Scroll down by 1000 pixels

        try:
            accept = driver.find_element(By.XPATH, "//button[contains(text(),'Accept')]")
            accept.click()
        except:
            pass

        time.sleep(2)
        iframe = driver.find_element(By.XPATH, "//*[contains(@aria-label,'Interactive floor plan viewer')]")
        driver.switch_to.frame(iframe)
        time.sleep(1)

        dropdown = driver.find_element(By.XPATH, "//div[@role='button'][@aria-label='Bedrooms']")
        dropdown.click()
        listbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ul[@role='listbox']")))
        options = listbox.find_elements(By.TAG_NAME, "li")
        for option in options:
            option.click()
        time.sleep(2)

        page_source = driver.page_source
        sel = Selector(text=page_source)
        floors = sel.xpath("//li[contains(@class,'-itemStyles')]")
        available_floors = []
        for floor in reversed(floors):
            number = int(floor.css('.css-1gmg8q9-numberStyles ::text').get('').strip())
            if number > 0:
                available_floors.append(floor.css('li ::attr(id)').get('').strip())

        for floor in available_floors:
            id = floor
            select_floor = driver.find_element(By.XPATH, f"//*[contains(@id,'{id}')]")
            select_floor.click()
            time.sleep(2)

            list_items = driver.find_elements(By.XPATH, "//li[contains(@class,'css-y76wec-listItemStyle')]")
            for item in list_items:
                button = item.find_element(By.TAG_NAME, "button")
                button.click()
                time.sleep(2)

                page_source = driver.page_source
                sel = Selector(text=page_source)
                item = dict()
                item['Building Name'] = 'Lake & Wells'
                item['Unit size'] = sel.xpath(
                    "//*[contains(@class,'css-1jskwkp-FloorPlanLabel e1ft7jji4')]/text()").get('').strip()
                item['Unit #'] = sel.xpath(".//*[contains(@id,'unit-number-label')]/text()").get('').strip().replace(
                    'APT', '').replace(' ', '')

                bed_bath = sel.xpath("//*[contains(@aria-label,' Bath')]/text()").get('').strip()
                item['Beds'] = int(
                    next((x.split()[0] for x in bed_bath.split('/') if 'Bed' in x and x.split()[0].isdigit()), 0))
                item['Bath'] = int(
                    next((x.split()[0] for x in bed_bath.split('/') if 'Bath' in x and x.split()[0].isdigit()), 0))

                item['Sq. Ft.'] = sel.xpath("//*[contains(@aria-label,'sq. ft.')]/text()").get('').strip()
                item['Available Date'] = sel.xpath("//*[contains(@aria-label,'Select A Date')]/@value").get('').strip()
                item['12 month Price'] = sel.xpath("//*[contains(@aria-label,'$')]/text()").get('').strip()
                item['Best Value Price and term'] = ''
                time.sleep(2)
                yield item

                back = driver.find_element(By.XPATH, "//*[contains(@class,'css-1aoivz8-CloseButton e2j3bts5')]")
                back.click()
                time.sleep(5)

        driver.quit()
