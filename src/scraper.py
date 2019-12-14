import os
import shutil
import time

def scrape_years(browser, url, xpath, update):
    # get years from dropdown options
    browser.get(url)
    options = browser.find_elements_by_xpath(xpath)
    years = [x.text.strip() for x in options[1:]]

    if update == True:
        years = years[:1]
    
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

# download ui claims
def download_ui(browser, xpath, years):
    url = f'http://www.dlt.ri.gov/lmi/uiadmin/'
    file_path = 'unemployment_insurance'

    for year in years:
        report_url = f'{url}/{year}.htm'

        # request url
        browser.get(report_url)

        # download excel file
        download_file(browser, xpath, file_path, year)

def download_sd(browser, years):
    url = 'http://www.dlt.ri.gov/lmi/excel'
    file_path = 'supply_demand'
    for year in years:
        # get quarter and year
        q = year[:1]
        year = year[-2:]
        fname = f'{q}-{year}'

        report_url = f'{url}/s&d{q}{year}.xlsx'
        browser.get(report_url)

        # move downloaded file
        move_file(fname, file_path)

def download_industry_proj(browser, xpath, report_type):
    url = f'http://www.dlt.ri.gov/lmi/proj/{report_type}indproj.htm'
    file_path = 'projections/industry'

    # request page
    browser.get(url)

    # download excel file
    download_file(browser, xpath, file_path, report_type)

def download_occupation_proj(browser, xpath, report_type):
    url = 'http://www.dlt.ri.gov/lmi/proj'
    file_path = 'projections/occupation'

    if report_type == 'major_occ_group':
        url = f'{url}/majoroccproj.htm'
    else:
        url = f'{url}/occprojocc.htm'

    # request page
    browser.get(url)

    # download excel file
    download_file(browser, xpath, file_path, report_type)

def download_new_england(browser, xpath, report_type):
    url = 'http://www.dlt.ri.gov/lmi/laus/us'
    file_path = 'geographic/new_england'

    if report_type == 'seasonal_adjusted':
        url = f'{url}/neadj.htm'
    else:
        url = f'{url}/neunadj.htm'

    # request url
    browser.get(url)

    # download excel file
    download_file(browser, xpath, file_path, report_type)

def download_citytown(browser, url, xpath, download):
    # get every city/town
    browser.get(url)
    options = browser.find_elements_by_xpath(xpath)
    cities = [x.get_attribute("value") for x in options[1:]]

    # get file_name
    fname = [x.text for x in options[1:]]
    fname = [" ".join(x.split()) for x in fname]
    fname = [x.lower().replace(' ', '_') for x in fname]

    # download file for each city
    count = 0
    for city in cities:
        file_path = 'geographic/cities_towns'
        browser.get(city)
        download_file(browser, download, file_path, fname[count])
        
        count += 1
        time.sleep(3)

def download_wages(browser, xpath, report_type):
    file_path = 'wages'

    if report_type == 'occupation_wages':
        url = 'http://www.dlt.ri.gov/lmi/oes/stateocc.htm'
    elif report_type == 'total_wages':
        url = 'http://www.dlt.ri.gov/lmi/es202/4digit/2018.htm'
    else:
        url = 'http://www.dlt.ri.gov/lmi/oes/nemedian.html'

    # request url
    browser.get(url)

    # download excel file
    download_file(browser, xpath, file_path, report_type)