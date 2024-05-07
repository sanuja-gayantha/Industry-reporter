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
            time.sleep(2)
        else:
            # The download did not complete successfully.
            print(f"Something went wrong. {items[0]['state']}")

        time.sleep(1)
        driver.quit()

        if os.path.exists(f"{currect_dir}/{download_url.split('/')[-1]}"):
            source = f"{currect_dir}/{download_url.split('/')[-1]}"
            destination = f"{os.path.join(os.getcwd(), './spyder/temp_pdfs')}"
            shutil.move(source, destination)

            result="valid"

    except Exception as e:
        print(e)
        pass
    
    return result


def selenium_pdf_downloader_main(pdf_url):
    return download_pdf_to_custom_path(pdf_url) 





