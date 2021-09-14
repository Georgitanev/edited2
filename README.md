# edited2
 scraper

# scraper

Downloading info from Mango .com

Scraper goes to the page in mango and downloads data for - item name, price, color, sizes and saves in .json format.
```sh
python scraper.py
```
To run it by scrapy use:
```sh
cd scraper_edit
scrapy crawl scraper_edit -O shop_data.json
```

Scraper have a validator who checks variable types and if they are correct saves the data in json file and prints a message.

```sh
"Given JSON data is Valid and saved in shop_data.json"
```

Installations:

You can check your chrome version from Crome browser by clicking -> menu -> help -> About Google Chrome
Download chrome driver that fits your chrome version from https://sites.google.com/chromium.org/driver/downloads

extract the file in folder

```sh
'chromedriver_win32\chromedriver.exe'
```
for scrapy put in folder

```sh
scraper_edit\scraper_edit\spiders\chromedriver_win32\chromedriver.exe
```
Install requirements file with packages and python v 3.8
```sh
pip install -r requirements.txt
```