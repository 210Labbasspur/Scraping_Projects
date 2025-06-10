'''
https://www.handelsbanken.com/en/investor-relations/reports-and-presentations
https://www.nordea.com/en/investors/swedish-subsidiary-reports
https://sebgroup.com/investor-relations/reports-and-presentations/financial-reports
https://www.swedbank.com/sv/investor-relations/rapporter-och-presentationer/delarsrapporter.html
https://investors.avanza.se/en/ir/reports/annual-and-interim-reports/
https://nordnetab.com/sv/investerare/finansiell-information/
https://www.norionbank.se/en-SE/investors/financial-information/reports-and-presentations
https://group.tfbank.se/en/financial-reports/
https://www.resursbank.se/om-oss/bolagsinformation/finansiell-information
https://www.catella.com/en/investor-relations/reports-and-presentations
https://www.samtrygg.com/finanansiell-rapportering
https://realheart.se/investors-realheart/financial-reports/
https://blickglobalgroup.com/reports
https://episurf.com/investors/reports/
https://spermosens.com/investors/financial-reports/?lang=sv
https://ir.chargepanel.se/
https://www.vibrosense.com/investors
https://goobit.se/investor-relations/arsredovisningar-och-rapporter
https://investor.plexian.se/
https://oncozenge.se/investors/
https://www.bioarctic.se/en/investors/
https://diagonalbio.com/investors-diagonal/financial-reports/
????________???? Investerare (streamify.io) ######################################################################
https://www.streamify.io/investors/
https://carbiotix.com/financiel-reports
https://www.fomtechnologies.com/investor/announcements-and-reports
https://aquabiotechnology.com/downloads/
'''


import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
# driver.get('https://www.handelsbanken.com/en/investor-relations/reports-and-presentations')
driver.get('https://www.handelsbanken.com/en/investor-relations/reports-and-presentations')
driver.maximize_window()
# element = driver.find_element(By.CSS_SELECTOR, ".views-field-name").get_attribute('href')
# element = driver.find_element(By.XPATH, "//*[contains(text(), 'Accept all')]/parent::button")
# element.click()

cookie_button = driver.find_element(By.XPATH, "//button[@class='shb-button-primary' and @data-test-id='CookieConsent__acceptButton']")
cookie_button.click()

prefix = 'https://vp292.alertir.com'
# element = driver.find_element(By.XPATH, "//a[contains(text(), '(PDF)')]/@href")
# (prefix + element).click()
elements = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
print(elements)
# Get href values and print them
pdf_hrefs = [element.get_attribute("href") for element in elements]
for href in pdf_hrefs:
    print("href:", prefix+href)



# print(element.)
time.sleep(2)
driver.quit()





