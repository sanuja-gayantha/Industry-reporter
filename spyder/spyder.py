# Developed by @sanuja : https://www.fiverr.com/sanuja_kumara

import requests
from bs4 import BeautifulSoup
import concurrent.futures

import time
import json
import os
import random
import re
from datetime import date
import uuid 

from rotatingProxy import rotatingProxy
from database import *
from api import api
from .pdf_downloader import pdf_downloader_main
from .selenium_pdf_downloader import selenium_pdf_downloader_main
from .iframe_extractor import get_iframe_pdf_urls_main
from .selenium_scraper import get_valid_urls_main
from .constants import IP_CHECKING_URL, CONNECTIONS, RESPONSE_ITERATIONS_PROXY, PROXY_TIMEOUT, GOOGLE_SHEET_SCOPES, GOOGLE_DRIVE_SCOPES


class Spyder():

    def __init__(self, scrape_type):

        self.scrape_type = scrape_type
        self.domains:list
        self.domain:str
        self.proxies_list:list
        self.current_domain_url:str
        self.proxy_timeout = PROXY_TIMEOUT
        self.headers = self.read_json_file(os.path.join(os.getcwd(), 'headers.json'))
        self.proxies_path = os.path.join(os.getcwd(), './rotatingProxy/proxy_list.json')
        self.temp_pdfs_dir_path= os.path.join(os.getcwd(), './spyder/temp_pdfs')

        rotatingProxy.rotating_proxy_main()
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
        self.proxies_list = self.read_json_file(self.proxies_path)


    def validate_url(self, url):

        filter_words=[
            "pt-br",
            "es-ar",
            "es-cl",
            "es-co",
            "fr",
            "de",
            "es",
            "it",
            "es-es",
            "el",
            "ko",
            "ja",
            "our-team",
            "about",
            "contact-us",
            "offices",
            "careers",
            "node"
        ]

        ext =[
            "mp4",
            "mp3"
        ]

        # https://
        if url.split(":")[0]=="https" or url.split(":")[0]=="http":

            # is it a pdf
            is_pdf=self.validate_pdf(url, "https") 
            if is_pdf!="":
                return ["valid_pdf", is_pdf]
                
            # removing social media links and invalid url formats
            url_identifier=url.split(":")[1].split("//")[1].split(".")[1] 
            current_url_identifier=self.current_domain_url.split(":")[1].split("//")[1].split(".")[1]

            if current_url_identifier!=url_identifier:
                return ["invalid", 0]

            countries_url_identifier=url.split("/")
            if not set(countries_url_identifier).isdisjoint(set(filter_words)):
                # print("Duplicates found.")
                return ["invalid", 0]

            ext_url_identifier=url.split("/")[-1].split(".")[-1]
            if not set(ext_url_identifier).isdisjoint(set(ext)):
                # print("Duplicates found.")
                return ["invalid", 0]

            return ["valid_url_https", url]

        # /
        elif url.split("/")[0]=="":

            countries_url_identifier=url.split("/")
            if not set(countries_url_identifier).isdisjoint(set(filter_words)):
                # print("Duplicates found.")
                return ["invalid", 0]           

            is_pdf=self.validate_pdf(url, "/") 
            
            if is_pdf!="":
                return ["valid_pdf", is_pdf]

            return ["valid_url_normal", self.domain+url]
        else:
            return ["invalid", 0]


    def validate_pdf(self, url, symbol):
        #  report links, fetch date, document title, and website domain/company.

        basic_split=url.split("/")[-1].split(".")
        if len(basic_split)>1:
            if basic_split[-1]=="pdf":
                if symbol == "/":
                    report_link=self.domain+url
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
        # Call Api for to get domains
        apiInstance = api.Api(api_scope=GOOGLE_SHEET_SCOPES)
        domains_data=apiInstance.api_read_domains_from_spreadsheet()
        self.domains = domains_data
        # self.domains = ["https://www.npci.org.in/"]
        # print(domains_data)
        # self.domains = self.read_json_file(self.domains_path)

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

        # create db tables if they does not exists
        with database.Database() as db:
            db.create_table_urls()
            db.create_table_pdf_urls()

        # # Connect to api for get pdf links and add write them to tempPdfUrlsList.json
        # apiIns = api.Api(GOOGLE_SHEET_SCOPES)
        # temp_pdf_links = apiIns.api_read_spreadsheet()

        for domain in self.domains:
            self.domain=domain
            condition=True

            if self.scrape_type=="n":
                pass

            elif self.scrape_type=="y":
                table_url=self.domain
                # table_url2=self.domain+"/sitemap"

                # delete temp_urls table & append above url_list value 
                with database.Database() as db:
                    db.drop_table_urls()
                    db.create_table_urls()
                    db.append_to_table_urls(self.domain, table_url, "unchecked")
                    # db.append_to_table_urls(self.domain, table_url2, "unchecked")
    

            print("[*] Searching pdf files in "+self.domain)
            idx=0
            while condition:
                selenium_type=False

                # creating new proxies after every 500 urls
                if idx >= 500:
                    idx = 0
                    rotatingProxy.rotating_proxy_main()
                    self.Initialize_proxy_ist()

                # find url that match self.domain & status=unchecked from temp_urls table 
                with database.Database() as db:
                    domain_and_status_uncheckeds=db.check_table_url_domain_and_status_uncheckeds(self.domain)

                if domain_and_status_uncheckeds !=  []:

                    self.current_domain_url=domain_and_status_uncheckeds[0][0]
                    print(self.current_domain_url)

                    response=""
                    # if selenium_type!=True:
                    for _ in range(RESPONSE_ITERATIONS_PROXY):
                        response = self.get_valid_proxy_domain_response()
                        if response!="":
                            break


                    if response!="" or response=="":
                        # Extract urls
                        temp_links=[]

                        # if website allows requests library
                        if response!="":
                            selenium_type=False
                            # 1.Normal page
                            soup = BeautifulSoup(response.text, 'html.parser')
                            for link in soup.find_all('a'):
                                unfiltered_href_link=link.get('href')
                                temp_links.append(unfiltered_href_link)
                            
                            # 2. If page have frams or iframes...
                            iframe_pdf_urls=get_iframe_pdf_urls_main(soup)
                            # print(iframe_pdf_urls)
                            if iframe_pdf_urls!="":
                                for iframe_pdf_url in iframe_pdf_urls:
                                    temp_links.append(iframe_pdf_url)


                        # if website does not allows requests library, so have to use selenium
                        if response=="":
                            selenium_type=True
                            seleniumLinkList = get_valid_urls_main(self.current_domain_url)
                            if len(seleniumLinkList)>0:
                                for seleniumLink in seleniumLinkList:
                                    temp_links.append(seleniumLink)


                        # drop duplicates in temp_links
                        unfiltered_links_list=[]
                        [unfiltered_links_list.append(x) for x in temp_links if x not in unfiltered_links_list]
                            
                        for unfiltered_link in unfiltered_links_list:
                            if unfiltered_link is not None:
                                validate=self.validate_url(unfiltered_link)
                                if validate[0] != "invalid":

                                    if validate[0]=="valid_url_normal":
                                        updated_url=validate[1]
                                        # filter updated_url in TEMP_URLS table, if does not exist, 
                                            # 1. append it to url_list
                                            # 2. add it to TEMP_URLS table
    
                                        with database.Database() as db:
                                            url_existence = db.check_table_url_existence(updated_url)
                                            if url_existence is None:
                                                # not exists
                                                db.append_to_table_urls(self.domain, updated_url, "unchecked") 



                                    elif validate[0]=="valid_url_https":
                                        updated_url=validate[1]
                                        # filter updated_url in TEMP_URLS table, if does not exist, 
                                            # 1. append it to url_list
                                            # 2. add it to TEMP_URLS table

                                        with database.Database() as db:
                                            url_existence = db.check_table_url_existence(updated_url)
                                            if url_existence is None:
                                                # not exists
                                                db.append_to_table_urls(self.domain, updated_url, "unchecked") 

                                                
                                    # return pdf data 
                                    elif validate[0]=="valid_pdf":

                                        # do pdf links existence filter function with temp_pdf_urls table in db                                          
                                        pdf_table_url=validate[1][2]
                                        with database.Database() as db:
                                            pdf_url_existence = db.check_table_pdf_urls_existence(pdf_table_url)

                                        if pdf_url_existence is None:
                                            # not exists
                                            with database.Database() as db:
                                                db.append_to_table_pdf_urls(self.domain, pdf_table_url) 

                                            print("Checking...", validate[1])

                                            # Call Api to download, upload, save data to google drive & google sheet
                            
                                            # Download pdf/only update sheet and if there is pdf
                                            pdf_id=""
                                            pdf_date=validate[1][0]
                                            pdf_domain=validate[1][1]
                                            pdf_title=validate[1][3]
                                            pdf_url=validate[1][2]

                                            # download using requests library
                                            if selenium_type!=True:
                                                pdf_result = pdf_downloader_main(pdf_url, pdf_title)

                                            # download using selenium 
                                            if selenium_type==True:
                                                pdf_result = selenium_pdf_downloader_main(pdf_url)

                                            if pdf_result=="valid":
 
                                                # Upload to google drive and return drive link/url
                                                print("Uploading...")      
                                                apiDriveInstance = api.Api(api_scope=GOOGLE_DRIVE_SCOPES)
                                                drive_response = apiDriveInstance.api_upload_to_drive(pdf_file_path = f"{self.temp_pdfs_dir_path}/{pdf_title}.pdf", pdf_file_title=f"{pdf_title}")
                                                pdf_id=drive_response[1]

                                                # create api instance
                                                apiInstance = api.Api(api_scope=GOOGLE_SHEET_SCOPES)

                                                # save data to google drive & google sheet
                                                data = [pdf_id, pdf_date, pdf_domain, pdf_title, pdf_url, drive_response[0], "New"]
                                                # print(data)
                                                apiInstance.api_append_spreadsheet(data)

                                                if os.path.exists(f"{self.temp_pdfs_dir_path}/{pdf_title}.pdf"):
                                                    os.remove(f"{self.temp_pdfs_dir_path}/{pdf_title}.pdf")

                                                # mark pdf upload ststus as "uploaded" 
                                                with database.Database() as db:
                                                    db.update_table_pdf_url_ststus(pdf_url)      


                    # mark VALID_URL ststus as "checked" 
                    with database.Database() as db:
                        db.update_table_url_ststus(self.current_domain_url)

                else:
                    condition=False

                idx+=1





def questions():
    print("Do you want to check the sequence of all the websites from the start?\n Type 'y' to yes... \n Type 'n'... to no \n Type 'exit' to quit..")
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
    answer = []
    answer = questions()
    
    while True:
        try:
            if answer[0]:
                ins = Spyder(scrape_type=answer[1])
                ins.scrape_website_urls()

            answer = [True, "y"]
        except Exception as e:
            print(e)
            answer = [True, "n"]

