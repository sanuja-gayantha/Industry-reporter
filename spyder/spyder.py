# Developed by @sanuja : https://github.com/sanuja-gayantha

import requests
from bs4 import BeautifulSoup
import concurrent.futures

import time
import json
import os
import random
import re
from datetime import date

from rotatingProxy.rotatingProxy import *
from api.google_sheet import google_sheet_api
from api.google_drive import google_drive_api
from .pdf_downloader import pdf_downloader_main
from .constants import IP_CHECKING_URL, CONNECTIONS, RESPONSE_ITERATIONS_PROXY, PROXY_TIMEOUT



class Spyder():

    def __init__(self, answer):

        self.answer = answer
        self.domains:list
        self.domain:str
        self.proxies_list:list
        self.current_domain_url:str
        self.proxy_timeout = PROXY_TIMEOUT
        self.headers = self.read_json_file(os.path.join(os.getcwd(), 'headers.json'))

        self.domains_path = os.path.join(os.getcwd(), './spyder/domains.json')
        self.proxies_path = os.path.join(os.getcwd(), './rotatingProxy/proxy_list.json')
        self.urls_list_path = os.path.join(os.getcwd(), './spyder/urls_list.json')
        self.pdf_data_list_path = os.path.join(os.getcwd(), './spyder/pdf_data_list.json')
        self.pdf_urls_list_path = os.path.join(os.getcwd(), './spyder/temp_pdf_urls_list.json')
        self.temp_pdfs_dir_path= os.path.join(os.getcwd(), './spyder/temp_pdfs')

        # temperary
        self.Initialize_proxy_ist()


    def read_json_file(self, path):
        with open(path) as json_file:
            result = json.load(json_file)
            return result


    def write_to_json_file(self, path, payload):
        with open(path, 'w') as file:
            json.dump(payload, file, indent=4, default=str)
        return


    def Initialize_proxy_ist(self):
        # rotating_proxy_main() 
        self.proxies_list = self.read_json_file(self.proxies_path)


    def validate_url(self, url):
        # https://
        
        if url.split(":")[0]=="https" or url.split(":")[0]=="http":

            # removing social media links and invalid url formats
            url_identifier=url.split(":")[1].split("//")[1].split(".")[1]
            current_url_identifier=self.current_domain_url.split(":")[1].split("//")[1].split(".")[1]

            if current_url_identifier!=url_identifier:
                return ["invalid", 0]
            

            # is it a pdf
            is_pdf=self.validate_pdf(url, "https") 
            if is_pdf!="":
                return ["valid_pdf", is_pdf]

            return ["valid_url_https", url]

        # /
        elif url.split("/")[0]=="":
            is_pdf=self.validate_pdf(url, "/") 
            if is_pdf!="":
                return ["valid_pdf", is_pdf]

            return ["valid_url_normal", self.domain["name"]+url]
        else:
            return ["invalid", 0]


    def validate_pdf(self, url, symbol):
        #  report links, fetch date, document title, and website domain/company.

        basic_split=url.split("/")[-1].split(".")
        if len(basic_split)>1:
            if basic_split[-1]=="pdf":
                if symbol == "/":
                    report_link=self.domain["name"]+url
                else:
                    report_link=url
                    
                fetch_date=date.today().strftime("%Y/%m/%d")
                document_title=url.split("/")[-1].split(".")[0]
                website_domain=self.domain

                return [fetch_date, website_domain, report_link, document_title, "New"]
        return ""


    def N_of_List(self, receved_list, N):
        temp_list=[]
        i=0
        while i<len(receved_list):
            temp_list.append(receved_list[i:i+N])
            i+=N
        return temp_list


    def domain_response(self, proxy):
        try:
            response = requests.get(self.current_domain_url, 
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


    def get_domains(self):
        # Call Api for to get domains <-- write Api !!

        # Then bsed on Question do following
            # 1. If yes delete Links.json & Pdfs.json & rewrite Domains.json <-- This will start the process from the beginning
            # 2. If not call the last domain, continue <-- If something went wrong, this willl help

        # domain_list will be replaced in future!!!
        # domain_list =[{"name" : "https://www.bain.com/", "status" : True, },{"name" : "https://kalaari.com/", "status" : True, }]      
        # self.write_to_json_file(self.domains_path, domain_list) 

        # Read filtered domains
        self.domains = self.read_json_file(self.domains_path)
        return

    def list_filter(self, value_v, list_v):
        filtered = filter(lambda x: x == value_v, list_v)
        if list(filtered):
            # print("exists in the list")
            return ""
        else:
            # print("does not exist in the list")
            return value_v
                

    def scrape_website_urls(self):

        # Get valid domains from get_domains function
        self.get_domains()

        # Connect to api for get pdf links and add write them to tempPdfUrlsList.json
        apiIns = google_sheet_api.Sheet_Api()
        temp_pdf_links = apiIns.api_read_spreadsheet()

        read_json_temp_pdf_urls_from_api=[]
        if os.path.exists(self.pdf_urls_list_path):
            read_json_temp_pdf_urls_from_api=self.read_json_file(self.pdf_urls_list_path)

        for temp_link in temp_pdf_links:
            is_temp_link_Exist=self.list_filter(temp_link, read_json_temp_pdf_urls_from_api)
            if is_temp_link_Exist!="":
                read_json_temp_pdf_urls_from_api.append(is_temp_link_Exist)

        if os.path.exists(self.pdf_urls_list_path):
            os.remove(self.pdf_urls_list_path)

        self.write_to_json_file(self.pdf_urls_list_path, read_json_temp_pdf_urls_from_api)


        json_url_list=[]
        json_pdf_urls_list=[]
        json_pdf_data_list=[]
        for domain in self.domains:
            self.domain=domain
            condition=True
            url_list=[]

            # url_list.append(domain["name"]+"/sitemap")
            url_list.append(self.domain["name"])

            # For every new domain call rotating_proxy_main() function to get new proxies list
            # self.Initialize_proxy_ist()

            print("[*] Searching pdf files in "+self.domain["name"])
            while condition:
                idx=0

                for count, url in enumerate(url_list):
                    if count == len(url_list):
                        break

                    self.current_domain_url=url
                    print(count, self.current_domain_url)

                    for _ in range(RESPONSE_ITERATIONS_PROXY):
                        response = self.get_valid_proxy_domain_response()
                        if response!="":
                            break

                    if response=="" and self.current_domain_url==(domain["name"]+"/sitemap"):
                        self.current_domain_url=self.domain["name"]
                        if self.list_filter(domain["name"]+"/sitemap", url_list)=="":
                            url_list.remove(domain["name"]+"/sitemap")
                        continue
                        print("Sitemap not found!!")

                    if response!="":
                        # print(self.current_domain_url)

                        # Add url to urlsList.json
                        json_url_list.append(self.current_domain_url)
                        self.write_to_json_file(self.urls_list_path, json_url_list)

                        # Extract urls
                        # 1.Normal page
                        soup = BeautifulSoup(response.text, 'html.parser')

                        temp_links=[]
                        for link in soup.find_all('a'):
                            unfiltered_href_link=link.get('href')
                            temp_links.append(unfiltered_href_link)

                        # drop duplicates in temp_links
                        unfiltered_links_list=[]
                        [unfiltered_links_list.append(x) for x in temp_links if x not in unfiltered_links_list]
                        
                        for unfiltered_link in unfiltered_links_list:
                            if unfiltered_link is not None:
                                validate=self.validate_url(unfiltered_link)
                                if validate[0] != "invalid":
                                    if validate[0]=="valid_url_normal":
                                        updated_url=validate[1]

                                        value_v=self.list_filter(updated_url, url_list)
                                        if value_v!="":
                                            url_list.append(value_v)
                                            # print(value_v)

                                    elif validate[0]=="valid_url_https":
                                        updated_url=validate[1]
                                        value_v=self.list_filter(updated_url, url_list)
                                        if value_v!="":
                                            url_list.append(value_v)
                                            # print(value_v)
                                            
                                    # return pdf data 
                                    elif validate[0]=="valid_pdf":
                                        # print(validate)

                                        # If pdf url not exist add it to json_pdf_urls_list
                                        if os.path.exists(self.pdf_urls_list_path):
                                            read_json_pdf_urls=self.read_json_file(self.pdf_urls_list_path)
                                        else:
                                            read_json_pdf_urls=[]
                                        
                                        # Check pdf existence from pdfList.json
                                        isExist=self.list_filter(validate[1][2], read_json_pdf_urls)

                                        if isExist!="":
                                            # Save all valid, invalid pdf urls to temp_pdf_urls_list.json
                                            json_pdf_urls_list.append(validate[1][2])
                                            self.write_to_json_file(self.pdf_urls_list_path, json_pdf_urls_list)

                                            # Call Api to download, upload, save data to google drive & google sheet
                                            try:
                                                # Download pdf/only update sheet and if there is pdf
                                                pdf_date=validate[1][0]
                                                pdf_domain=validate[1][1]["name"]
                                                pdf_title=validate[1][3]
                                                pdf_url=validate[1][2]
                                                drive_link=""
                                                    
                                                pdf_result = pdf_downloader_main(pdf_url, pdf_title)
                                                if pdf_result=="valid":
                                                    # Upload to google drive and return drive 
                                                    
                                                    
                                                    # create api instance
                                                    apiInstance = google_sheet_api.Sheet_Api()

                                                    # save data to google drive & google sheet
                                                    data = [pdf_date, pdf_domain, pdf_title, pdf_url, drive_link, "New"]
                                                    print(data)
                                                    apiInstance.api_append_spreadsheet(data)

                                                # if os.path.exists(f"{self.temp_pdfs_dir_path}/{self.pdf_title}.pdf"):
                                                #     os.remove(f"{self.temp_pdfs_dir_path}/{self.pdf_title}.pdf")

                                            except:
                                                pass


                        # 2. If page have frams or iframes...
                        # .................................

                    # print(url_list)
                    idx+=1
                    if idx==1:
                        break

                
                condition=False

            


# Question : Is this a brand new scraping? 
def questions():
    print("Is this a brand new scraping?\n Type 'y' to yes... \n Type 'n'... to no \n Type 'exit' to quit..")
    while True:
        command = input("> ")
        if command == "exit":
            break
        if command == "y":
            return [True, "y"]
        if command == "n":
            return [True, "n"]
        try:
            print(eval(command))
        except Exception as e:
            # print(f"Exception: {str(e)}")
            print("[*] Input is not valid. Try again...")


def spyder_main():
    answer = questions()
    if answer[0]:
        ins = Spyder(answer=answer[1])
        ins.scrape_website_urls()

        # ins=pdf_downloader_main("http://www.nddb.coop/sites/default/files/AB_BV_and_SSCR/BV_and_SSCR_MSN_Mehsana_Buffalo_Dec_2021.pdf", "test")





