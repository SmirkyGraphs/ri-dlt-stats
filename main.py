import json
import argparse
from selenium import webdriver
from src import scraper
from src import cleaner

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

def renamer_dict():
    # loading dictionary to rename columns and add level
    file = './data/files/data_dict.json'
    with open(file) as f:
        data = json.load(f)

    # get order of ces cols
    order_ces = data['current_employment']['order_cols']
    order_state = data['statewide_employment']['order_cols']

    # get rename columns
    rename_ces_cols = data['current_employment']['non_adjusted']['rename_cols']

    # get rename dict
    rename_act = data['current_employment']['non_adjusted']['rename_industry']
    rename_adj = data['current_employment']['seasonally_adjusted']['rename_industry']

    # get level dict
    level_act = data['current_employment']['non_adjusted']['map_level']
    level_adj = data['current_employment']['seasonally_adjusted']['map_level']
    
    renamer = {
        'rename_ces_cols': rename_ces_cols,
        'rename_act': rename_act,
        'rename_adj': rename_adj,
        'level_act': level_act,
        'level_adj': level_adj,
        'order_ces': order_ces,
        'order_state': order_state
    }
    
    return renamer
    
def run_scrapers():
    scraper.scrape_current_employment(browser, update)
    scraper.scrape_ui_claims(browser, update)
    scraper.scrape_supply_demand(browser, update)
    scraper.scrape_projections(browser, update)
    scraper.scrape_geographic(browser)
    scraper.scrape_wages(browser, update)

def run_cleaners():
    cleaner.clean_ces(rename_dict)
    cleaner.clean_statewide(rename_dict)

if __name__ == '__main__':
    # load config options
    with open('config.json', 'r') as f:
        config = json.load(f)
        save_path = config['save_path']
        chromedriver = config['chromedriver']

    # start chrome browser
    #options = chrome_options(save_path)
    #browser = webdriver.Chrome(chromedriver, options=options)

    # check if update
    update = arg_parse()

    # scrape all information
    #run_scrapers()
    #browser.close()

    # merge files and clean data
    rename_dict = renamer_dict()
    run_cleaners()
