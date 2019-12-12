import json
import argparse
from selenium import webdriver

from src import scraper

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--update', action='store_true', dest='update')
    args = parser.parse_args()
    update = args.update

    return update

def scrape_current_employment():
    # get years and download button for ces stats
    url = 'http://www.dlt.ri.gov/lmi/ces.htm'
    button_options = '//*[@id="form"]/font/select/option'
    years = scraper.scrape_years(browser, url, button_options, update)
    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/b'

    # scrape sesoanlly adjusted ces stats
    adjusted_download = f'{download}/span/font/a[1]'
    scraper.download_ces(browser, 'seasonal', adjusted_download, years)

    # scrape non-adjusted ces stats
    non_adj_download = f'{download}/font[2]/font[2]/strong/a[1]'
    scraper.download_ces(browser, 'state', non_adj_download, years)

def scrape_ui_claims():
    print('hello')

if __name__ == '__main__':
    # load config options
    with open('config.json', 'r') as f:
        config = json.load(f)
        save_path = config['save_path']
        chromedriver = config['chromedriver']

    # start chrome browser
    options = scraper.chrome_options(save_path)
    browser = webdriver.Chrome(chromedriver, options=options)

    # check if update
    update = arg_parse()

    # scrape all information
    scrape_current_employment()
    scrape_ui_claims()

    # next http://www.dlt.ri.gov/lmi/uiadmin.htm


