#######     AFIP
import os
import time
import openpyxl
from datetime import datetime, timedelta
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def read_excel_to_list(file_path, encoding='latin-1'):
    data = []
    workbook = openpyxl.load_workbook(file_path, read_only=True)
    sheet = workbook.active
    headers = [cell.value.strip() for cell in sheet[1]]
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = dict(zip(headers, row))
        for header, value in zip(headers, row):
            if isinstance(value, datetime):
                value = value.strftime("%d/%m/%Y")  # Convert date to string
            row_data[header] = value
        data.append(row_data)
    return data
######   Reading Input Excell file to collect required data
file_path = "input/AFIP_input.xlsx"
data = read_excel_to_list(file_path)


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get('https://auth.afip.gob.ar/')
# driver.maximize_window()
time.sleep(20)


for entry in data:
    print(entry)
    email_field = driver.find_element('id', 'F1:username')  # Use the correct identifier for your email input field
    email_field.clear()
    time.sleep(5)
    email_id = entry.get('ID')
    email_field.send_keys(email_id)
    login_button = driver.find_element('id', 'F1:btnSiguiente')  # Use the correct identifier for your login button
    login_button.click()
    time.sleep(10)
    password_field = driver.find_element('id', 'F1:password')  # Use the correct identifier for your password input field
    password_field.clear()
    password = entry.get('pwd')
    password_field.send_keys(password)
    login_button = driver.find_element('id', 'F1:btnIngresar')  # Use the correct identifier for your login button
    login_button.click()
    time.sleep(10)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "buscadorInput"))
    )
    page_source = driver.page_source
    response = Selector(text=page_source)
    search_box = response.css('#buscadorInput').get('')

    search_field = driver.find_element('id', 'buscadorInput')  # Use the correct identifier for your password input field
    search_field.clear()
    search_field.send_keys('MIS COMPROBANTES')
    time.sleep(5)
    link_element = driver.find_element(By.XPATH,"//a[contains(@class, 'dropdown-item')]")
    link_element.click()

    print(driver.title)
    time.sleep(25)
    print('Lets move to other Tab ')
    # WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    # WebDriverWait(driver, 10).until(EC.number_of_windows_to_be_greater_than(1))
    # WebDriverWait(driver, 10).until(EC.new_window_is_opened(driver.window_handles))
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(10)
    print(driver.title)
    time.sleep(15)

    # if entry.get('Agent') == 'Y':
    if entry.get('Agent', '').lower() == 'y':
        SRL_button = driver.find_element(By.XPATH,"//*[contains(text(),'DIAGNOSTICO TESLA SRL')]/parent::div[1]/parent::div[1]/parent::a[contains(@class,'panel panel-default hoverazul')]")
        SRL_button.click()
        time.sleep(10)
    # else:
    #     pass


    categories = ['Emitidos', 'Recibidos']
    for category in categories:
        print('Lets enter the loop')
        time.sleep(10)
        cat_btn = None
        if category == 'Emitidos':
            cat_btn = driver.find_element('id', 'btnEmitidos')  # Use the correct identifier for your password input field
            time.sleep(5)
        elif category == 'Recibidos':
            cat_btn = driver.find_element('id', 'btnRecibidos')  # Use the correct identifier for your password input field
            time.sleep(5)

        cat_btn.click()

        time.sleep(10)
        print(driver.title)

        search_field = driver.find_element('id', 'fechaEmision')  # Use the correct identifier for your password input field
        search_field.clear()

        today = datetime.today()
        first_day_of_current_month = datetime(today.year, today.month, 1)

        start_date_str = entry.get('Initial_date')
        end_date_str = entry.get('Ending_date')

        date_range = f"{start_date_str} - {end_date_str}"
        print('Dates are :', date_range)
        search_field.send_keys(date_range)

        time.sleep(10)
        search_button = driver.find_element('id', 'buscarComprobantes')  # Use the correct identifier for your login button
        search_button.click()


        time.sleep(20)

        ######## Set the download directory and file name
        chrome_options = Options()
        download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        output_dir = os.path.join(download_dir, 'OUTPUT')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        prefs = {"download.default_directory": download_dir}
        chrome_options.add_experimental_option("prefs", prefs)
        time.sleep(10)

        time.sleep(10)
        print('Lets download the available csv or excell file, and its button is : ')
        print(driver.find_element(By.XPATH,"//*[contains(@class,'dt-buttons btn-group')]/button[contains(@class,'btn btn-default')][1]"))
        download_button = driver.find_element(By.XPATH,"//*[contains(@class,'dt-buttons btn-group')]/button[contains(@class,'btn btn-default')][1]")
        download_button.click()

        time.sleep(20)

        #### Calculate the date string to be appended to the file name
        today = datetime.today()
        first_day_of_last_month = datetime(today.year, today.month - 1, 1)
        date_suffix = " - " + end_date_str[2:].replace('/', '')

        time.sleep(10)
        #### Wait for the file to be downloaded
        timeout = 10  # Maximum time to wait for the file to be downloaded (in seconds)
        start_time = time.time()
        while True:
            files = [f for f in os.listdir(download_dir) if os.path.isfile(os.path.join(download_dir, f))]
            files = [f for f in files if f.endswith('.xlsx') or f.endswith('.zip')]
            if files:
                try:
                    latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(download_dir, x)))
                    break
                except FileNotFoundError:
                    pass
            elif time.time() - start_time > timeout:
                print("Timeout: File download took too long.")
                break
            time.sleep(5)

        time.sleep(10)
        if files:
            if latest_file.endswith('.xlsx'):
                new_file_name = latest_file.split(".")[0] + date_suffix + ".xlsx"
            elif latest_file.endswith('.zip'):
                new_file_name = latest_file.split(".")[0] + date_suffix + ".zip"
            else:
                print("Unsupported file format.")
                new_file_name = None
            if new_file_name:
                os.rename(os.path.join(download_dir, latest_file), os.path.join(download_dir, new_file_name))
                os.replace(os.path.join(download_dir, new_file_name), os.path.join(output_dir, new_file_name))
                # Confirmation message
                print(f"The file has been saved successfully as '{new_file_name}' in the 'OUTPUT' folder.")
        else:
            print("No files were found in the download directory.")


        time.sleep(10)
        Menu_button = driver.find_element(By.XPATH,"//a[contains(text(),'Menú Principal')]")
        Menu_button.click()
        time.sleep(10)

    driver.get('https://auth.afip.gob.ar/')
    time.sleep(15)


print('Code completed')
driver.quit()
