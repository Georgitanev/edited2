import json
import os

import jsonschema
from bs4 import BeautifulSoup as bs
from jsonschema import validate
from selenium import webdriver

path = os.path.dirname(os.path.abspath(__file__))
chrome_driver_path = os.path.join(path, "chromedriver_win32", "chromedriver.exe")

filename = "shop_data.json"
mango_shop_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "price": {"type": "number"},
        "color": {"type": "string"},
        "size": {"type": "array"},
    },
    "required": ["name", "price", "color", "size"]
}
# //TODO put schema as external file


def validateJson(jsonData):
    try:
        validate(instance=jsonData, schema=mango_shop_schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True


def validate_and_save(items, filename):
    if validateJson(items):
        print(items)
        with open(filename, "w") as writeJSON:
            json.dump(items, writeJSON, ensure_ascii=False)
        print("Given JSON data is Valid and saved in " + filename)
    else:
        print(items)
        print("Given JSON data is InValid")


driver = webdriver.Chrome(chrome_driver_path)
caps = webdriver.DesiredCapabilities.CHROME.copy()
driver.implicitly_wait(90)  # wait page to load
driver.set_window_size(1400, 1047)
# open the URL
driver.get(
    "https://shop.mango.com/bg-en/women/skirts-midi/midi-satin-skirt_17042020.html?c=99")
# click button to accept cookies
driver.find_element_by_id("onetrust-accept-btn-handler").click()
# click menu with sizes
driver.find_element_by_xpath("//div[@id='sizeSelector']/span").click()


def extract_data(driver):
    source = bs(driver.page_source, 'html.parser')
    name = driver.find_element_by_xpath(
        "//div[@id='app']/main/div/div[3]/div/div/h1").text
    price_str = driver.find_element_by_xpath(
        "//div[@id='app']/main/div/div[3]/div/div[2]/span[2]").text
    price = float(price_str.split('лв.')[1])
    # color detector
    label_text = source.find('div', {
        'class': 'color-container color-container--selected'}).img['alt']
    color = label_text.split(' ')[0].lower()
    # sizes list
    sizes_html = driver.find_element_by_xpath(
        "//*[@id='sizeSelector']/div").text
    all_sizes_list = sizes_html.split("\n")
    return name, price, color, all_sizes_list


name, price, color, all_sizes_list = extract_data(driver)
items = {
    "name": name,
    "price": price,
    "color": color,
    "size": all_sizes_list
}

validate_and_save(items, filename)
driver.quit()

