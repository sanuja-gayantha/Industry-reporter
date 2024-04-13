# Developed by @sanuja : https://github.com/sanuja-gayantha

import requests
from bs4 import BeautifulSoup as soup
import concurrent.futures
import json
import os
import random

from .constants import PROXIEX_LOCATED_URL, IP_CHECKING_URL, CONNECTIONS


class RotatingProxy():
    
    def __init__(self, proxies_located_url, ip_checking_url):

        self.proxies_located_url = proxies_located_url
        self.ip_checking_url = ip_checking_url
        self.proxies = []
        self.headers = self.read_json_file(os.path.join(os.getcwd(), 'headers.json'))
        self.proxies_path = os.path.join(os.getcwd(), './rotatingProxy/proxyList.json')


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
            response = requests.get(self.proxies_located_url, 
                                        headers=self.headers,
                                        proxies={"http": proxy, "https": proxy}, timeout=5)
            return response

        except Exception as e:
            return ""
            pass       

    # Find proxies IP's from web & Scrape them
    def get_proxies_from_web(self):

        current_proxies_list = self.read_json_file(self.proxies_path)

        random.shuffle(current_proxies_list) 
        random_proxies_list = self.N_of_List(current_proxies_list, N=5)

        # Sends 5 requests at once to same domain url
        for count, random_proxies_list_element in enumerate(random_proxies_list):
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                results = executor.map(self.domain_response, random_proxies_list[count])
                
            get_out=False
            for response in results:
                if response != "":
                    # print(result.status_code, result.json())
                    get_out=True
                    break

            if get_out:
                break
          
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

        with open('./rotatingProxy/proxyList.json', 'w') as file:
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


    