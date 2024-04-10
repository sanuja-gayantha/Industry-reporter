# Developed by @sanuja : https://github.com/sanuja-gayantha

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import time

from constants import BASE_URL


class Reporter(webdriver.Chrome):

    def __init__(self, tear_down=False):
        options = webdriver.ChromeOptions()
        super(Reporter, self).__init__(service=ChromeService(ChromeDriverManager().install()), options=options)

        self.tear_down = tear_down
        # self.base_url = base_url
        
    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.tear_down:
            self.quit()


    def scrape_website_urls(self):
        # Navigate to home page (use proxy IP's)
        # Check if there is sitemap or not
            # 1. Navigate to sitemap
            # 2. Nf not pass
        # Collect all href links
            # 1. Store then in a list
        # Navigate to each link 
            # 1. Find href links
            # 2. Add href links to list(save links to .json file) if they does not exists already
                # If there is .pdf link, download it, upload to google drive (Write Api library for this) 
                    # <-- For now only do .pdf link filtering..
            # 3. Continue navigation process until count of new links existance equal to zero

        



with Reporter(tear_down=False) as manager:
    manager.get_main_page()
    print('Exiting...')








