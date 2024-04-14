# Developed by @sanuja : https://github.com/sanuja-gayantha

import requests
import concurrent.futures
import os
import time
import random

from rotatingProxy.rotatingProxy import *
from api.google_sheet import google_sheet_api
from api.google_drive import google_drive_api
from .constants import IP_CHECKING_URL, CONNECTIONS, RESPONSE_ITERATIONS_PROXY, PROXY_TIMEOUT



class Pdf_Downloader():

    def __init__(self, pdf_url, pdf_title):
        self.proxies_list=self.read_json_file(os.path.join(os.getcwd(), './rotatingProxy/proxy_list.json'))
        self.pdf_download_url=pdf_url
        self.pdf_title=pdf_title
        self.proxy_timeout = PROXY_TIMEOUT
        self.headers = self.read_json_file(os.path.join(os.getcwd(), 'headers.json'))
        self.temp_pdfs_dir_path= os.path.join(os.getcwd(), './spyder/temp_pdfs')


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


    def download_response(self, proxy):
        try:
            response = requests.get(self.pdf_download_url, 
                                        headers=self.headers,
                                        stream = True,
                                        verify=False,
                                        proxies={"http": proxy, "https": proxy})
                                        
            if response.status_code==200:
                content = next(response.iter_content(10))
            else:
                return

            return response
        except Exception as e:
            return ""
            pass


    #  Run for every link
    def get_valid_proxy_download_response(self):
        result = ""

        random.shuffle(self.proxies_list) 
        random_proxies_list = self.N_of_List(self.proxies_list, N=7)
        # print(random_proxies_list)

        # Sends 10 requests at once to same domain url
        for count, random_proxies_list_element in enumerate(random_proxies_list):
            with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
                results = executor.map(self.download_response, random_proxies_list[count])
                
            get_out=False
            for result in results:
                if result != "":
                    # print(result.status_code, result.json())
                    get_out=True
                    break

            if get_out:
                break

        return result


    def download_pdf(self):
        result =""
        for _ in range(RESPONSE_ITERATIONS_PROXY):
            response = self.get_valid_proxy_download_response()
            if response!="":
                result="valid"
                break

        if result=="valid":
            print(f"[*] Downloading {self.pdf_download_url} ...")
            with open(f"{self.temp_pdfs_dir_path}/{self.pdf_title}.pdf", "wb") as fd:
                fd.write(response.content)

            file_size = 0
            while file_size == 0:
                file_size = os.path.getsize(f"{self.temp_pdfs_dir_path}/{self.pdf_title}.pdf")
                # print(file_size)
                time.sleep(1)

        return result

        
def pdf_downloader_main(pdf_url, pdf_title):
    pdfInstance = Pdf_Downloader(pdf_url, pdf_title)
    result = pdfInstance.download_pdf()
    return result








