# Developed by @sanuja : https://github.com/sanuja-gayantha

import requests
from bs4 import BeautifulSoup as soup
import concurrent.futures
import json
import os

from .constants import PROXIEX_LOCATED_URL, IP_CHECKING_URL, CONNECTIONS


class RotatingProxy():
    
    def __init__(self, proxies_located_url, ip_checking_url):

        self.proxies_located_url = proxies_located_url
        self.ip_checking_url = ip_checking_url
        self.proxies = []
        self.headers = self.read_json_file(os.path.join(os.getcwd(), 'headers.json'))


    def read_json_file(self, path):
        with open(path) as json_file:
            result = json.load(json_file)
            return result


    # Find proxies IP's from web & Scrape them
    def get_proxies_from_web(self):

        response = requests.get(self.proxies_located_url)
        bsObj = soup(response.content, features="lxml")

        for ip in bsObj.findAll('table')[0].findAll('tbody')[0].findAll('tr'):    
            # put table rows to a list
            cols = ip.findChildren(recursive = False)
            cols = [element.text.strip() for element in cols]
            
            # proxy address
            proxy = 'socks4://'+ ':'.join([cols[0],cols[1]])
            self.proxies.append(proxy)
            # print(proxy)


    # Find working/valid IP's
    def extract_valid_proxy(self, proxy):
        try:
            response = requests.get(self.ip_checking_url, 
                                        headers=self.headers,
                                        proxies={"http": proxy, "https": proxy}, timeout=5)
            return proxy

        except Exception as e:
            return ""
            pass

        
    # Store them in .json file for futher use
    def generate_json(self, results):

        temp_results=[]
        for result in results:
            if result != "":
                print(result)
                temp_results.append(result)

        with open('proxyList.json', 'w') as file:
            json.dump(temp_results, file, indent=4)

        if len(temp_results)<25:
            self.rotating_proxy_main()



def rotating_proxy_main():
    print("[*] Searching new proxies...")
    
    ins = RotatingProxy(PROXIEX_LOCATED_URL, IP_CHECKING_URL)
    ins.get_proxies_from_web()

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        results = executor.map(ins.extract_valid_proxy, ins.proxies)

    ins.generate_json(results)


    