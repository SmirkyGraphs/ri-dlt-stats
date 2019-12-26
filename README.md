# Rhode Island Dept. Labor & Training Statistics
 
This project uses selenium to automate downloading excel files on employment, wages, supply & demand and other labor related stats from Rhode Island's [Department of Labor and Training](http://www.dlt.ri.gov/lmi/data.htm). The data is then cleaned using pandas and shaped to better work with Tableau to create dashboards tracking changes over time.

## Prerequisites

You must have Python 3 installed.  You can download it
[here](https://www.python.org/downloads/).  
To use selenium you will need the [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) version matching your chrome browser.  
The `config.json` needs to be edited with your chromedriver path and the path for your `/data/temp` folder location.

## Data Collection

Currently these are the data sources that are collected from `scraper.py`.

- [current employment stats](http://www.dlt.ri.gov/lmi/ces.htm)
- [monthly ui claims](http://www.dlt.ri.gov/lmi/uiadmin.htm)
- [supply & demand](http://www.dlt.ri.gov/lmi/publications/supply&demand.htm)
- [industry/occupation projections](http://www.dlt.ri.gov/lmi/proj.htm)
- [statewide labor force](http://www.dlt.ri.gov/lmi/laus/state/state.htm)
- [cities/towns labor force](http://www.dlt.ri.gov/lmi/laus/town/town.htm)
- [new england unemployment](http://www.dlt.ri.gov/lmi/laus/us/us.htm)
- [occupation wages](http://www.dlt.ri.gov/lmi/oes/stateocc.htm)
- [total wages by industry](http://www.dlt.ri.gov/lmi/es202/4digit/2018.htm)
- [new england wages by occupation](http://www.dlt.ri.gov/lmi/oes/nemedian.html)

## Data Cleaning

Currently these are the data sources that are cleaned from `cleaner.py`.

- [current employment stats](http://www.dlt.ri.gov/lmi/ces.htm)
- [monthly ui claims](http://www.dlt.ri.gov/lmi/uiadmin.htm)
- [statewide labor force](http://www.dlt.ri.gov/lmi/laus/state/state.htm)