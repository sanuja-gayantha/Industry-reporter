# Developed by @sanuja : https://www.fiverr.com/sanuja_kumara

import os
import json
import random
import time
import shutil


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def download_pdf_to_custom_path(download_url):
    currect_dir=os.getcwd()
    result =""
    try:
        options = webdriver.ChromeOptions()

        options.add_experimental_option("prefs",  {
            "download.default_directory": currect_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
            }
        )
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(download_url)
        time.sleep(5)
        
        driver.get("chrome://downloads")
        download_items_script = "return document.querySelector('downloads-manager').shadowRoot.getElementById('downloadsList').items;"
        items = driver.execute_script(download_items_script)

        while items[0]["state"] == 0:
            time.sleep(1)
            items = driver.execute_script(download_items_script)

        if items[0]["state"] == 2:
            # print(items[0])
            time.sleep(2)
        else:
            # The download did not complete successfully.
            print(f"Something went wrong. {items[0]['state']}")

        time.sleep(1)
        driver.quit()

        if os.path.exists(f"{currect_dir}/{items[0]['fileName']}"):
            source = f"{currect_dir}/{items[0]['fileName']}"
            destination = f"{os.path.join(os.getcwd(), './spyder/temp_pdfs')}"
            shutil.move(source, destination)

            old_name = f"{os.path.join(os.getcwd(), './spyder/temp_pdfs/', items[0]['fileName'])}"
            new_name = f"{os.path.join(os.getcwd(), './spyder/temp_pdfs', download_url.split('/')[-1])}"
            os.rename(old_name, new_name)

            result="valid"
            return result


        # # if .pdf's exists in root move thenm in to temp_pdfs folder
        # files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.pdf')]
        # if len(files)>0:
        #     for file in files:
        #         source = f"{os.getcwd()}/{file}"
        #         destination = f"{os.path.join(os.getcwd(), './spyder/temp_pdfs')}"
        #         shutil.move(source, destination)
                
        #     result="valid"
        #     return result


    except Exception as e:
        print(e)
    
    return result


def selenium_pdf_downloader_main(pdf_url):
    result = download_pdf_to_custom_path(pdf_url) 
    return result





