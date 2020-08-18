# Indeed.com Crawler

## Table of content
* Background
* Install
  - Python 3.7.4
  - Scrapy 2.3.0
  - MongoDB 4.4.0
* Usage

## Back ground
This project aim to seek the current skill demand trending, so that poeple can specify what skills to develop. The program will
 collect the job ads from indeed.com and store the data into MongoDB. Then the generate the keywords from the ads into a tag cloud
 and a excel chart. The program is developed on Windows 10, which is the default environment for all the content. 

## Install
To run the scrapy crawler we need to prepare few things below.
### Python 3.7.4

  You can use version check commands to check if Python is installed.You can use `python --version` to check if python is installed
  If not to https://www.python.org/downloads/ to download for the python. 

### Scrapy 2.3.0
  If you are using Anaconda or Miniconda, to install Scrapy using conda, run
  >conda install -c conda-forge scrapy
  
  Alternatively after python is installed you can install scrapy as a Python packages with
  >pip install Scrapy
  
  And you can check if the installation is successful by checking the version with `scrapy -version`.

### MongoDB 4.4.0
  You can go to https://docs.mongodb.com/manual/administration/install-community/ to download the MongoDB with the msi package.During the installation make sure
  to install MongoDB as a service.The detaill instruction is given on the site. After the MongoDB is installed.

### Word cloud
You can use the command below to install the package.
>pip install wordcloud

  
## Usage
  First to extract the zip file. Then run the gui.py with `python gui.py` in cmd, the gui should prompt should come out in few seconds. There are 5 field in the inerface.
  * 'Input start url'
  
    Search the job in the main site, after redirecting to the search result, copy the address from result site and input to this field, make sure the 
    qurey does not contain 'start='. 
  * 'Input total job numbers to be crawled'
  
    Find the total job number in the result site and input to this field. Make sure the input is integer or the program will crash.
  * 'Input User-Agent'
  
    Input the user-agent you are going to apply to send requests. The default user-agent is `Mozilla/5.0 (X11; Linux x86_64)`
  * 'Obey Robot.txt'
  
    Select yes or not to decide wether the spider will obey the scraping rule set by the site
  * 'Out put'
  
    This filed will display the crawling process.
