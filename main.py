import json
import argparse
from selenium import webdriver
from src import scraper

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
    # get years and download button for ui claims
    url = 'http://www.dlt.ri.gov/lmi/uiadmin.htm'
    button_options = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[1]/td[2]/table/tbody/tr[7]/td/p/font/select'
    years = scraper.scrape_years(browser, url, button_options, update)
    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[1]/td/p[1]/b/font/a[1]'

    # scrape ui claims
    scraper.download_ui(browser, download, years)

def scrape_supply_demand():
    # get quarter-year for supply & demand
    url = 'http://www.dlt.ri.gov/lmi/publications/supply&demand.htm'
    button_options = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td/blockquote/table/tbody/tr[2]/td[3]/select/option'
    years = scraper.scrape_years(browser, url, button_options, update)

    # scrape supply & demand
    scraper.download_sd(browser, years)

def scrape_projections():
    if update == True:
        return

    # download major industry 
    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/b/font[2]/font/a[1]'
    scraper.download_industry_proj(browser, download, 'major')

    # download 3 digit naics industry
    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/b/font[3]/font/a[1]'
    scraper.download_industry_proj(browser, download, 'naics3')

    # download specific occupations (uses same download xpath as above)
    scraper.download_occupation_proj(browser, download, 'occupations')

    # download major occupation groups (uses same download xpath as above)
    scraper.download_occupation_proj(browser, download, 'major_occ_group')

def scrape_geographic():
    # download new england unemployment
    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/b/font[2]/font[2]/a[1]'
    scraper.download_new_england(browser, download, 'non_adjusted')
    scraper.download_new_england(browser, download, 'seasonal_adjusted')

    # get employment by city/town
    url = 'http://www.dlt.ri.gov/lmi/laus/town/town.htm'
    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr/td/p/b/span/font/a' 
    button_options = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/form/table/tbody/tr[4]/td[2]/select/option'
    scraper.download_citytown(browser, url, button_options, download)

def scrape_wages():
    if update == True:
        return

    # download wage information
    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/b/font[2]/font[2]/a'
    scraper.download_wages(browser, download, 'total_wages')
    scraper.download_wages(browser, download, 'occupation_wages')
    scraper.download_wages(browser, download, 'new_england_wages')
    
def run_scrapers():
    scrape_current_employment()
    scrape_ui_claims()
    scrape_supply_demand()
    scrape_projections()
    scrape_geographic()
    scrape_wages()

if __name__ == '__main__':
    # load config options
    with open('config.json', 'r') as f:
        config = json.load(f)
        save_path = config['save_path']
        chromedriver = config['chromedriver']

    # start chrome browser
    options = chrome_options(save_path)
    browser = webdriver.Chrome(chromedriver, options=options)

    # check if update
    update = arg_parse()

    # scrape all information
    run_scrapers()
