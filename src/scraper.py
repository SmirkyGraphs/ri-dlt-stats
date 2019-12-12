import os
import shutil
import time

from selenium import webdriver
from datetime import datetime
from pytz import timezone


def chrome_options(download_dir):
    options = webdriver.ChromeOptions() 
    download_dir = download_dir.replace('/', '\\')

    prefs = {
        'download.prompt_for_download' : False,
        'download.default_directory' : f'{download_dir}',
    }

    #options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('prefs', prefs)

    return options

def scrape_years(browser, url, xpath, update):
    if update == True:
        years = [str(datetime.now(timezone('EST')).year)]
        
    else:
        # get years from dropdown options
        browser.get(url)
        button_options = '//*[@id="form"]/font/select/option'
        options = browser.find_elements_by_xpath(button_options)
        years = [x.text.strip() for x in options[1:]]
    
    return years

# create function to move file after downloading
def move_file(year, file_path):
    temp_path = './data/temp/'
    temp_file = temp_path + os.listdir(temp_path)[0]
    stem_file = temp_file.split('.')[-1]
    new_file = f'./data/raw/{file_path}/{year}.{stem_file}'
    shutil.move(temp_file, new_file)

def download_file(browser, xpath, file_path, year):
        button = browser.find_element_by_xpath(xpath)
        button.click()
        time.sleep(2)
        move_file(year, file_path)

# download ces stats
def download_ces(browser, report_type, xpath, years):
    url = f'http://www.dlt.ri.gov/lmi/ces/{report_type}'

    # set file_name type
    if report_type == 'seasonal':
        file_path = 'current_employment/seasonal_adjusted'
    else:
        file_path = 'current_employment/non_adjusted'

    for year in years:
        report_url = f'{url}/{year}.htm'

        # request url
        browser.get(report_url)

        # download excel file
        download_file(browser, xpath, file_path, year)