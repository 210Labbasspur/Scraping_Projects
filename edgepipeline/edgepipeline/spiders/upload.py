import os
import scrapy
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime


class upload(scrapy.Spider):
    name = 'upload'
    start_urls = ['https://www.example.com']

    def parse(self, response):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.get('https://pearlsolutions.ftptoday.com/')
        time.sleep(5)
        email_field = driver.find_element('id', 'u')
        email_field.send_keys('MarathonMotorsCOData')
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        time.sleep(5)

        password_field = driver.find_element('id', 'p')
        password_field.send_keys('J2gPzBSrDhnv')
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        time.sleep(10)

        upload_button = driver.find_element('id', 'files-upload')
        upload_button.click()
        time.sleep(2)

        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')  # Adjust the XPath as needed
        relative_file_path = f'output/edgepipeline_watch_list_all - ({datetime.now().strftime("%d-%m-%Y")}).csv'
        absolute_file_path = os.path.abspath(relative_file_path)

        # Send the file path to the file input element
        file_input.send_keys(absolute_file_path)

        time.sleep(10)

        # Deleting file after uploading on the site
        relative_file_path = f'output/edgepipeline_watch_list_all - ({datetime.now().strftime("%d-%m-%Y")}).csv'
        file_path = os.path.abspath(relative_file_path)
        try:
            os.remove(file_path)
            print(f"{file_path} has been deleted successfully.")
        except FileNotFoundError:
            print(f"The file {file_path} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(5)
        driver.quit()

