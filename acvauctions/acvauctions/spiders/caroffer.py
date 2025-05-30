import os
import csv
import time
import scrapy
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
##  Auto-Installer in Selenium to avoid any issue


class caroffer(scrapy.Spider):
    name = 'caroffer'
    start_urls = ['https://www.example.com']


    def parse(self, response):
        file_path = f'output/Uploaded on Caroffer - {datetime.now().strftime("%d-%m-%Y")}.csv'
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f'{file_path} has been deleted.')

        csv_file_path = f'output/acvauctions - {datetime.now().strftime("%d-%m-%Y")}.csv'
        data_list = []
        if os.path.exists(csv_file_path):
            with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    row_dict = {
                        'VIN': row['VIN'],
                        'Mileage': row['Mileage'],
                        'Zip': row['Zip'],
                        'Color': row['Color'],
                        'Leather': row['Leather'],
                        'Sunroof': row['Sunroof'],
                        'Navigation': row['Navigation']
                    }
                    if 10000 <= abs(int(row['Zip'])) <= 99999:
                        data_list.append(row_dict)

            for vehicle in data_list:
                print(vehicle)


            options = webdriver.ChromeOptions()
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(options=options)
            driver.get('https://dealer.caroffer.com/#/sell/fresh-trades-dash')
            time.sleep(5)

            email_field = driver.find_element('id', 'userName')
            password_field = driver.find_element('id', 'password')
            email_field.send_keys('muhammet.citiroglu@gmail.com')
            password_field.send_keys('Reapers11779!')
            time.sleep(1)
            login_button = driver.find_element(By.XPATH, "//*[@type='submit']")
            login_button.click()
            time.sleep(5)

            for vehicle in data_list[30:40]:
                print(vehicle)
                dollor = driver.find_element(By.XPATH, "//*[@data-icon='dollar']")
                dollor.click()
                time.sleep(2)

                try:
                    try:
                        add_vehicle = driver.find_element(By.XPATH, "//*[contains(text(), 'Add Vehicle')]")
                        add_vehicle.click()
                        other_vehicle = driver.find_element(By.XPATH,"//*[contains(text(),'Other Vehicle')]/parent::button[1]")
                        other_vehicle.click()
                        time.sleep(5)
                    except:
                        pass

                    vin_field = driver.find_element(By.XPATH, "//*[contains(@name,'userInput')]")
                    ActionChains(driver).double_click(vin_field).send_keys(Keys.DELETE).perform()
                    vin_field.send_keys(vehicle.get('VIN'))
                    time.sleep(2)
                    go_button = driver.find_element(By.XPATH,"//*[@class='ant-btn ant-btn-primary ant-btn-lg goButton___tvpzN']")
                    driver.execute_script("arguments[0].click();", go_button)
                    time.sleep(5)

                    time.sleep(2)
                    try:
                        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'hubspot-conversations-iframe')))
                        close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='initial-message-close-button']")))
                        close_button.click()
                        driver.switch_to.default_content()
                        print("Chat widget closed successfully.")
                    except Exception as e:
                        print(f"An error occurred while closing the chat widget")
                        driver.switch_to.default_content()
                        print("Switched back to default content.")
                    time.sleep(2)

                    mileage = driver.find_element(By.XPATH, "//*[contains(@id,'tradeGradeMileage')]")
                    ActionChains(driver).double_click(mileage).send_keys(Keys.DELETE).perform()
                    mileage.send_keys(vehicle.get('Mileage'))
                    time.sleep(1)

                    dropdown = driver.find_element(By.XPATH,"//*[contains(text(),'Exterior Color')]/preceding-sibling::span[1]/parent::div[1]")
                    dropdown.click()
                    list_container = driver.find_element(By.XPATH, "//*[@class='rc-virtual-list-holder']")
                    for _ in range(5):  # Adjust the number of iterations as needed
                        try:
                            option = driver.find_element(By.XPATH,f"//div[contains(@class, 'ant-select-item-option') and @title='{vehicle.get('Color')}']")
                            option.click()
                            break
                        except:
                            driver.execute_script("arguments[0].scrollBy(0, 100);", list_container)
                            WebDriverWait(driver, 1).until(lambda d: list_container.is_displayed())

                    time.sleep(2)

                    zipcode = driver.find_element(By.XPATH, "//*[contains(@id,'tradeGradeVehicleZipCode')]")
                    ActionChains(driver).double_click(zipcode).send_keys(Keys.DELETE).perform()
                    zipcode.send_keys(vehicle.get('Zip'))
                    time.sleep(1)

                    time.sleep(5)
                    get_vehicle_button = driver.find_element(By.XPATH,"//*[contains(text(),'Get Vehicle Options')]/parent::button[1]")
                    driver.execute_script("arguments[0].click();", get_vehicle_button)
                    time.sleep(10)

                    actions = ActionChains(driver)
                    actions.send_keys(Keys.PAGE_DOWN).perform()
                    try:
                        required_element = driver.find_element(By.XPATH, "//b[contains(text(), '(REQUIRED)')]")
                        while (required_element):
                            print('***   Required_element Found   *** ')
                            time.sleep(2)
                            dropdown = driver.find_element(By.XPATH,"//*[contains(text(),'(REQUIRED)')]/parent::span[1]/following-sibling::div[1]"
                                                           "/div[1]/div[1][contains(@class,'ant-select-selector')]")
                            time.sleep(1)
                            driver.execute_script("arguments[0].scrollIntoView();", dropdown)
                            dropdown.click()
                            first_option = WebDriverWait(driver, 10).until(
                                EC.presence_of_all_elements_located((By.XPATH,"//div[contains(@class, 'ant-select-item ant-select-item-option ant-select-item-option-active')]/div[contains(@class, 'ant-select-item-option')][1]"))
                            )

                            driver.execute_script("arguments[0].scrollIntoView(true);", first_option[-1])
                            driver.execute_script("arguments[0].click();", first_option[-1])
                            time.sleep(2)

                            actions = ActionChains(driver)
                            actions.send_keys(Keys.PAGE_DOWN).perform()

                    except (NoSuchElementException, TimeoutException):
                        print("No more element with '(REQUIRED)' found. Proceeding without selection.",
                              NoSuchElementException)

                    actions = ActionChains(driver)
                    actions.send_keys(Keys.PAGE_DOWN).perform()
                    time.sleep(5)

                    if int(vehicle.get('Leather')) == 1:
                        leather_button = driver.find_element(By.XPATH,"//*[contains(text(),'Has Leather?')]/following-sibling::div[1]/button[1]")
                        leather_button.click()
                    else:
                        leather_button = driver.find_element(By.XPATH,"//*[contains(text(),'Has Leather?')]/following-sibling::div[1]/button[2]")
                        leather_button.click()
                    time.sleep(2)

                    if int(vehicle.get('Sunroof')) == 1:
                        sunroof_button = driver.find_element(By.XPATH,"//*[contains(text(),'Has Sunroof/Moonroof?')]/following-sibling::div[1]/button[1]")
                        sunroof_button.click()
                    else:
                        sunroof_button = driver.find_element(By.XPATH,"//*[contains(text(),'Has Sunroof/Moonroof?')]/following-sibling::div[1]/button[2]")
                        sunroof_button.click()
                    time.sleep(2)

                    if int(vehicle.get('Navigation')) == 1:
                        navigation_button = driver.find_element(By.XPATH,"//*[contains(text(),'Has Navigation?')]/following-sibling::div[1]/button[1]")
                        navigation_button.click()
                    else:
                        navigation_button = driver.find_element(By.XPATH,"//*[contains(text(),'Has Navigation?')]/following-sibling::div[1]/button[2]")
                        navigation_button.click()
                    time.sleep(5)

                    next_button = driver.find_element(By.XPATH, "//*[contains(text(),'Next')]/parent::button[1]")
                    next_button.click()
                    time.sleep(7)

                    preowned_button = driver.find_element(By.XPATH,"//*[contains(text(),'Is the vehicle Certified Pre-Owned')]/following-sibling::div[1]/button[2]")
                    preowned_button.click()
                    time.sleep(2)
                    updatevehicle_button = driver.find_element(By.XPATH, "//*[contains(text(),'Update Vehicle')]/parent::button[1]")
                    updatevehicle_button.click()

                    time.sleep(2)
                    try:
                        close_button = driver.find_element(By.XPATH,"//*[@class='ant-btn ant-btn-text ant-btn-icon-only closeBtn___ypkf4']")
                        close_button.click()
                        time.sleep(2)
                    except:
                        pass
                    time.sleep(15)

                    refresh_button = driver.find_element(By.XPATH,"//*[@class='anticon anticon-reload reloadIcon___4TEhq']")
                    refresh_button.click()

                    time.sleep(15)
                    page_source = driver.page_source
                    sel = Selector(text=page_source)
                    latest_vehicle = sel.css(".ant-collapse-item-active:nth-child(1) .vehicleCardsWrap___S4Yoo div:nth-child(1) .goldMarker___11hMp")
                    if vehicle.get('VIN') == latest_vehicle.css('.vehicleMetric___2VBnU ::text').get('').strip():
                        item = dict()
                        item['VIN'] = latest_vehicle.css('.vehicleMetric___2VBnU ::text').get('').strip()
                        item['24Hr Approvals'] = latest_vehicle.xpath(".//div[contains(text(),'24Hr Approvals')]/following-sibling::div[1]/text()").get('').strip().replace('$', '').replace(',', '')
                        item['Sell Today'] = latest_vehicle.xpath(".//div[contains(text(),'Sell Today')]/following-sibling::div[1]/text()").get('').strip().replace('$', '').replace(',', '')
                        sell_today = latest_vehicle.xpath(".//div[contains(text(),'Sell Today')]/following-sibling::div[1]/text()").get('').strip().replace('$', '').replace(',', '')
                        item['93% of Sell Today'] = None
                        if sell_today != 'N/A' and sell_today != '':
                            item['93% of Sell Today'] = round((float(sell_today) * (0.93)), 2)
                        item['45-Day Guarantee'] = latest_vehicle.xpath(".//div[contains(text(),'45-Day Guarantee')]/following-sibling::div[1]/text()").get('').strip().replace('$', '').replace(',', '')

                        with open(f'output/Uploaded on Caroffer - {datetime.now().strftime("%d-%m-%Y")}.csv', 'a', newline='',
                                  encoding='utf-8') as csvfile:
                            fieldnames = ['VIN', '24Hr Approvals', 'Sell Today', '93% of Sell Today', '45-Day Guarantee']
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            if csvfile.tell() == 0:
                                writer.writeheader()
                            writer.writerow(item)
                            print('Data entered : ', item)

                        time.sleep(2)
                    else:
                        print('VIN # ', vehicle.get("VIN"), ' Vehicle could not be uploaded successfully')

                except (NoSuchElementException, TimeoutException):
                    print("Provided VIN is not valid")
                    close_button = driver.find_element(By.XPATH,"//*[@class='ant-btn ant-btn-text ant-btn-icon-only closeBtn___ypkf4']")
                    close_button.click()
                    time.sleep(2)

            driver.quit()
            #   Deleting file at the end of the script
            file_path = f'output/acvauctions - {datetime.now().strftime("%d-%m-%Y")}.csv'
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f'{file_path} has been deleted.')
        else:
            print(f'{csv_file_path} File doesnt exists')
