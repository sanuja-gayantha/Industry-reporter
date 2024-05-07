# # # # Developed by @sanuja : https://www.fiverr.com/sanuja_kumara

# from spyder import spyder

# if __name__ == "__main__":
#     spyder.spyder_main()


# # from spyder import selenium_scraper

# # current_domain_url="https://www.npci.org.in/"
# # seleniumLinkList = selenium_scraper.get_valid_urls_main(current_domain_url)

# # from spyder import selenium_pdf_downloader


# # import requests

# # pdf_url = "https://www.npci.org.in/PDF/nach/circular/2015-16/Circular_No_126.pdf"
# # pdf_title=pdf_url.split('/')[-1]

# # headers = {
# #     "Cookie": "TS6917...",  # Cookie, I get it from my browser developer tools, you can replace it with yours.
# #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
# # }

# # response = requests.get(url, headers=headers)
# # if response.status_code == 200:
# #     with open("file.pdf", "wb") as f:
# #         f.write(response.content)
# #     print("Download complete!")
# # else:
# #     print("Failed to download the file. Status code:", response.status_code)

# # selenium_pdf_downloader.selenium_pdf_downloader_main(pdf_url, pdf_title)

# # url="https://www.npci.org.in/PDF/nach/circular/2015-16/Circular-No.135.pdf"
# # s=url.split("/")
# # print(s)






# import time
# import os
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait



# download_url = "https://www.npci.org.in/PDF/nach/circular/2015-16/Circular-No.135.pdf"
# download_dir = os.path.join(os.getcwd())
# options = webdriver.ChromeOptions()

# options.add_experimental_option('prefs',  {         
#     "download.default_directory": download_dir,
#     "download.prompt_for_download": False,         
#     "plugins.always_open_pdf_externally": True         
#     })

# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# driver.get(download_url)
# WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#icon')))
# driver.find_element(By.ID, '#icon').click()

# time.sleep(5)
# driver.quit()

# url="https://web-assets.bcg.com/04/0a/60f1dc524b858490ba660dbc7632/bcg-gamma-lighthouse-full-length.mp3"

# ext =[
#     "mp4",
#     "mp3"
# ]
# ext_url_identifier=url.split("/")[-1].split(".")[-1]
# if not set(ext_url_identifier).isdisjoint(set(ext)):
#     # print("Duplicates found.")
#     return ["invalid", 0]

# print(ext_url_identifier)


# import requests

# url = 'https://www.npci.org.in/PDF/nach/circular/2015-16/Circular-No.135.pdf'
# path = 'sample.pdf'

# response = requests.get(url)

# with open(path, 'wb') as file:
#     file.write(response.content)





# import time
# import os
# from pathlib import Path
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait

# def download_pdf_to_custom_path(download_url, download_folder):
#     options = webdriver.ChromeOptions()

#     options.add_experimental_option("prefs",  {
#         "download.default_directory": download_folder,
#         "download.prompt_for_download": False,
#         "download.directory_upgrade": True,
#         "plugins.always_open_pdf_externally": True
#         }
#     )
#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
#     driver.get(download_url)
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "form")))
    
#     driver.get("chrome://downloads")
#     download_items_script = "return document.querySelector('downloads-manager').shadowRoot.getElementById('downloadsList').items;"
#     items = driver.execute_script(download_items_script)
#     while items[0]["state"] == 0:
#         time.sleep(1)
#         items = driver.execute_script(download_items_script)

#     if items[0]["state"] == 2:
#         time.sleep(2)
#     else:
#         print(f"Something went wrong. {items[0]['state']}")

#     driver.quit()


# if __name__ == "__main__":
#     download_url = "https://www.npci.org.in/PDF/nach/circular/2015-16/Circular-No.135.pdf"
#     folder = os.path.join(os.getcwd())
#     download_pdf_to_custom_path(download_url, folder)




# from spyder import selenium_pdf_downloader

# pdf_url = "https://web-assets.bcg.com/a4/fe/08791d2b4abf9b62e4e7eabc6a49/time-to-run-finland-bcg.pdf"
# print(selenium_pdf_downloader.selenium_pdf_downloader_main(pdf_url))



import sqlite3
import os


old_list=[]
connection = sqlite3.connect(os.path.join(os.getcwd(), 'r2database.db'))
cur = connection.cursor()


pd =  cur.execute("SELECT * FROM TEMP_URLS").fetchall()
for p in pd:
    old_list.append([p[1], p[2], p[3]])

connection.close()

# print(old_list)


connection = sqlite3.connect(os.path.join(os.getcwd(), 'database.db'))
cur = connection.cursor()
cur.execute("DROP TABLE TEMP_URLS") 
cur.execute('''CREATE TABLE IF NOT EXISTS TEMP_URLS(ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                    VALID_URL_DOMAIN VARCHAR,
                                                                    VALID_URL VARCHAR,
                                                                    STATUS VARCHAR);''')


for o in old_list:
    cur.execute('''INSERT INTO TEMP_URLS (VALID_URL_DOMAIN, VALID_URL, STATUS) VALUES (?, ?, ?)''', (o[0], o[1], o[2],))
    
connection.commit()
connection.close()
