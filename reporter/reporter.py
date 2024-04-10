# Developed by @sanuja : https://github.com/sanuja-gayantha

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import time
import json
import os

from .constants import BASE_URL


class Reporter(webdriver.Chrome):

    def __init__(self, tear_down=False):
        # options = webdriver.ChromeOptions()
        # super(Reporter, self).__init__(service=ChromeService(ChromeDriverManager().install()), options=options)

        self.tear_down = tear_down
        self.domains = []
        
    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.tear_down:
            self.quit()

    
    def get_domains(self):
        # Call Api for to get domains <-- write Api !!

        # Then bsed on Question do following
            # 1. If yes delete Links.json & Pdfs.json & rewrite Domains.json <-- This will start the process from the beginning
            # 2. If not call the last domain, continue <-- If something went wrong, this willl help

        # domain_list will be replaced in future!!!
        domain_list =[{"name" : "https://www.bain.com/", "status" : True, },{"name" : "https://kalaari.com/", "rollno" : True, }]      
        
        # with open('Domains.json', 'w') as file:
        #     json.dump(domain_list, file, sindent=4)

        # Read filtered domains
        with open(os.path.join('', Domains.json)) as json_file:
            self.domains = json.load(json_file)

        return

    def scrape_website_urls(self):
        # Question : Is this a brand new scraping?
        # Call Api for to get domains <-- write Api !!
        # Then bsed on Question do following
            # 1. If yes delete Links.json & Pdfs.json & rewrite Domains.json, this will start the process from the beginning
            # 2. If not call the last domain, continue <-- If something went wrong, this willl help
        # Navigate to home page (use proxy IP's)
        # Check if there is sitemap or not
            # 1. Navigate to sitemap & collect all href links
            # 2. Nf not pass & collect all href links
            # 3. Store then in a list
        # Navigate to each link 
            # 1. Find href links
            # 2. Add href links to the list(save links to .json file) if they does not exists already
                # If there is .pdf link, download it, upload to google drive <-- write Api !!
                    # <-- For now only do .pdf link filtering..
            # 3. Repeat navigation process until count of new links existance equal to zero


        print(self.domains)
        






def reporter_main():
    with Reporter(tear_down=False) as manager:
        manager.scrape_website_urls()
        # print('Exiting...')








