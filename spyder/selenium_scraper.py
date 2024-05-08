# Developed by @sanuja : https://www.fiverr.com/sanuja_kumara

import os
import json
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class Selenium_Scraper(webdriver.Chrome):

    def __init__(self):
 
        self.iframe_src:any

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        super(Selenium_Scraper, self).__init__(service=ChromeService(ChromeDriverManager().install()), options=options)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.quit()

    def read_json_file(self, path):
        with open(path) as json_file:
            result = json.load(json_file)
            return result

    def get_valid_urls(self, link):

        pdf_links=[]
        try:
            self.get(link)
            WebDriverWait(self, 15).until(EC.presence_of_element_located((By.XPATH, '//a [@href]')))
            raw_links = self.find_elements(By.XPATH, '//a [@href]')

            for link in raw_links:
                l = link.get_attribute("href")
                pdf_links.append(l)
            print(pdf_links)
            return pdf_links

        except Exception as e:
            return ""


def get_valid_urls_main(link):
    with Selenium_Scraper() as se:
        return se.get_valid_urls(link) 









