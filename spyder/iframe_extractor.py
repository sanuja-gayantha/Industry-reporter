# Developed by @sanuja : https://www.fiverr.com/sanuja_kumara

import requests
from bs4 import BeautifulSoup
import os
import concurrent.futures
import json
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from rotatingProxy.rotatingProxy import *
from .constants import CONNECTIONS, RESPONSE_ITERATIONS_PROXY, PROXY_TIMEOUT


class Iframe_Extractor(webdriver.Chrome):

    def __init__(self):

        self.headers = self.read_json_file(os.path.join(os.getcwd(), 'headers.json'))
        self.proxies_list=self.read_json_file(os.path.join(os.getcwd(), './rotatingProxy/proxy_list.json'))
        self.proxy_timeout = PROXY_TIMEOUT
        self.iframe_src:any

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        super(Iframe_Extractor, self).__init__(service=ChromeService(ChromeDriverManager().install()), options=options)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.quit()

    def read_json_file(self, path):
        with open(path) as json_file:
            result = json.load(json_file)
            return result

    def N_of_List(self, receved_list, N):
        temp_list=[]
        i=0
        while i<len(receved_list):
            temp_list.append(receved_list[i:i+N])
            i+=N
        return temp_list

    def domain_response(self, proxy):
        try:
            response = requests.get(self.iframe_src, 
                                        headers=self.headers,
                                        proxies={"http": proxy, "https": proxy}, timeout=self.proxy_timeout)
            return response

        except Exception as e:
            return ""
            pass

    #  Run for every link
    def get_valid_proxy_domain_response(self):
        result = ""

        random.shuffle(self.proxies_list) 
        random_proxies_list = self.N_of_List(self.proxies_list, N=7)
        # print(random_proxies_list)

        # Sends 10 requests at once to same domain url
        for count, random_proxies_list_element in enumerate(random_proxies_list):
            with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
                results = executor.map(self.domain_response, random_proxies_list[count])
                
            get_out=False
            for result in results:
                if result != "":
                    # print(result.status_code, result.json())
                    get_out=True
                    break

            if get_out:
                break

        return result

    def get_iframe_pdf_urls(self, soup):

        pdf_links=[]
        try:
            iframe_src = soup.iframe["src"]
            self.iframe_src=iframe_src

            for _ in range(RESPONSE_ITERATIONS_PROXY):
                iframe_text = self.get_valid_proxy_domain_response()
                if iframe_text!="":
                    break

            if iframe_text!="":
                print(iframe_text.url)

                self.get(iframe_text.url)
                WebDriverWait(self, 15).until(EC.presence_of_element_located((By.XPATH, '//a [@href]')))
                raw_links = self.find_elements(By.XPATH, '//a [@href]')

                for link in raw_links:
                    l = link.get_attribute("href")
                    l_split=l.split("/")[-1].split(".")
                    if len(l_split)>1 and l_split[-1]=="pdf":
                        # print(l_split, "raw_link:{}".format(l))
                        pdf_links.append(l)

                return pdf_links
            return ""
            
        except Exception as e:
            return ""


def get_iframe_pdf_urls_main(soup):
    with Iframe_Extractor() as ie:
        return ie.get_iframe_pdf_urls(soup) 









