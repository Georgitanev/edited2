import json
import os
from time import sleep

import jsonschema
import scrapy
from bs4 import BeautifulSoup as bs
from jsonschema import validate
from selenium import webdriver

from ..items import ScraperEditItem

path = os.path.dirname(os.path.abspath(__file__))
chrome_driver_path = os.path.join(path, "chromedriver_win32",
                                  "chromedriver.exe")
# schema path
mango_shop_schema_path = os.path.join(path, "json_schema.json")


def open_json(schema_path):
    with open(schema_path, encoding="utf-8-sig") as fh:
        return json.load(fh)


class QuotesSpider(scrapy.Spider):
    name = "scraper_edit"
    start_urls = [
        "https://shop.mango.com/bg-en/women/skirts-midi/midi-satin-skirt_17042020.html?c=99"]

    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        chrome_driver_path = os.path.join(path, "chromedriver_win32",
                                          "chromedriver.exe")
        self.driver = webdriver.Chrome(chrome_driver_path)

    def validateJson(self, items, mango_shop_schema):
        self.items = items
        try:
            validate(instance=self.items, schema=mango_shop_schema)
        except jsonschema.exceptions.ValidationError as err:
            return False
        return True

    def parse(self, response):
        items = ScraperEditItem()
        self.driver.get(response.url)
        source = bs(self.driver.page_source, 'html.parser')
        self.driver.implicitly_wait(90)  # wait page to load
        self.driver.set_window_size(1400, 1047)
        self.driver.get(response.url)
        # click button to accept cookies
        # // TODO to put click for cookies on first page only.
        # // And may be checker.
        # // TODO after that they are accepted. Wait too much time for except
        try:
            self.driver.find_element_by_id("onetrust-accept-btn-handler").click()
        except Exception as ex:
            print(ex)
        # click menu with sizes
        self.driver.find_element_by_xpath(
            "//div[@id='sizeSelector']/span").click()
        name = self.driver.find_element_by_xpath(
            "//div[@id='app']/main/div/div[3]/div/div/h1").text
        price_str = self.driver.find_element_by_xpath(
            "//div[@id='app']/main/div/div[3]/div/div[2]/span[2]").text
        price = float(price_str.split('лв.')[1])
        # color detector
        sleep(5)
        label_text = source.find('div', {
            'class': 'color-container color-container--selected'}).img[
            'alt']
        color = label_text.split(' ')[0].lower()
        # sizes list
        sizes_html = self.driver.find_element_by_xpath(
            "//*[@id='sizeSelector']/div").text
        all_sizes_list = sizes_html.split("\n")
        items["name"] = name
        items["price"] = price
        items["color"] = color
        items["size"] = all_sizes_list

        validate_validate = {
            "name": name,
            "price": price,
            "color": color,
            "size": all_sizes_list
        }
        x = self.validateJson(validate_validate, mango_shop_schema)
        if x:
            yield {
                    "name": name,
                    "price": price,
                    "color": color,
                    "size": all_sizes_list}
