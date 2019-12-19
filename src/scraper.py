import os
import time
import shutil

# scrape years and only most recent with --update
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
    
    while not os.listdir(temp_path):
        time.sleep(3)

    temp_file = temp_path + os.listdir(temp_path)[0]
    stem_file = temp_file.split('.')[-1]
    
    # check if file finished downloading
    while stem_file == 'tmp':
        time.sleep(3)
        print('[status] waiting on file to download...')
        temp_file = temp_path + os.listdir(temp_path)[0]
        stem_file = temp_file.split('.')[-1]

    new_file = f'./data/raw/{file_path}/{year}.{stem_file}'
    shutil.move(temp_file, new_file)

def download_file(browser, xpath, file_path, year):
        button = browser.find_element_by_xpath(xpath)
        button.click()
        time.sleep(2)
        move_file(year, file_path)

############################ Generalized Scrapers ############################
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

# download supply & demand
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

# download industry projections
def download_industry_proj(browser, xpath, report_type):
    url = f'http://www.dlt.ri.gov/lmi/proj/{report_type}indproj.htm'
    file_path = 'projections/industry'

    # request page
    browser.get(url)

    # download excel file
    download_file(browser, xpath, file_path, report_type)

# download occupation projections
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

# download new_england employment
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

# download city/town employment
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

# download statewide employment
def download_statewide(browser, xpath, report_type):
    url = 'http://www.dlt.ri.gov/lmi/laus/state'
    file_path = 'geographic/state'

    if report_type == 'seasonal_adjusted':
        url = f'{url}/seas.htm'
    else:
        url = f'{url}/unadj.htm'

    # request url
    browser.get(url)

    # download excel file
    download_file(browser, xpath, file_path, report_type)

# download wage data
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

############################ Start of Scrapers ############################
def scrape_current_employment(browser, update):
    # get years and download button for ces stats
    url = 'http://www.dlt.ri.gov/lmi/ces.htm'
    button_options = '//*[@id="form"]/font/select/option'
    years = scrape_years(browser, url, button_options, update)
    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/b'

    # scrape sesoanlly adjusted ces stats
    adjusted_download = f'{download}/span/font/a[1]'
    download_ces(browser, 'seasonal', adjusted_download, years)

    # scrape non-adjusted ces stats
    non_adj_download = f'{download}/font[2]/font[2]/strong/a[1]'
    download_ces(browser, 'state', non_adj_download, years)

def scrape_ui_claims(browser, update):
    # get years and download button for ui claims
    url = 'http://www.dlt.ri.gov/lmi/uiadmin.htm'
    button_options = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[1]/td[2]/table/tbody/tr[7]/td/p/font/select/option'
    years = scrape_years(browser, url, button_options, update)
    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[1]/td/p[1]/b/font/a[1]'

    # scrape ui claims
    download_ui(browser, download, years)

def scrape_supply_demand(browser, update):
    # get quarter-year for supply & demand
    url = 'http://www.dlt.ri.gov/lmi/publications/supply&demand.htm'
    button_options = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td/blockquote/table/tbody/tr[2]/td[3]/select/option'
    years = scrape_years(browser, url, button_options, update)

    # scrape supply & demand
    download_sd(browser, years)

def scrape_projections(browser, update):
    if update == True:
        return

    # download major industry 
    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/b/font[2]/font/a[1]'
    download_industry_proj(browser, download, 'major')

    # download 3 digit naics industry
    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/b/font[3]/font/a[1]'
    download_industry_proj(browser, download, 'naics3')

    # download specific occupations (uses same download xpath as above)
    download_occupation_proj(browser, download, 'occupations')

    # download major occupation groups (uses same download xpath as above)
    download_occupation_proj(browser, download, 'major_occ_group')

def scrape_geographic(browser):
    # download statewide unemployment
    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/b/font[2]/a[1]'
    download_statewide(browser, download, 'non_adjusted')
    download_statewide(browser, download, 'seasonal_adjusted')

    # download new england unemployment
    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/b/font[2]/font[2]/a[1]'
    download_new_england(browser, download, 'non_adjusted')
    download_new_england(browser, download, 'seasonal_adjusted')

    # get employment by city/town
    url = 'http://www.dlt.ri.gov/lmi/laus/town/town.htm'
    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr/td/p/b/span/font/a' 
    button_options = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/form/table/tbody/tr[4]/td[2]/select/option'
    download_citytown(browser, url, button_options, download)

def scrape_wages(browser, update):
    if update == True:
        return

    # download wage information
    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/b/font[2]/font/a'
    download_wages(browser, download, 'total_wages')

    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/b/font[2]/font[2]/a'
    download_wages(browser, download, 'occupation_wages')

    download = '/html/body/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[1]/td/b/font[3]/font/a'
    download_wages(browser, download, 'new_england_wages')