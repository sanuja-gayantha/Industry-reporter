# # import requests
# # from bs4 import BeautifulSoup

# # headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'}
# # url="https://www.bain.com/insights/topics/energy-and-natural-resources-report/"

# # response = requests.get(url, headers=headers)
# # soup = BeautifulSoup(response.text, 'html.parser')

# # for link in soup.find_all('a'):
# #     print(link.get('href'))

# # # Bain, BCG, Elevation Capital, Kalaari capital 

# # from selenium import webdriver
# # from selenium.webdriver.chrome.service import Service as ChromeService
# # from webdriver_manager.chrome import ChromeDriverManager

# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from bs4 import BeautifulSoup

# # options = webdriver.ChromeOptions()
# # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# # driver.get("https://view.ceros.com/bain/chapters1-4-3-1/p/1?heightOverride=1100&mobileHeightOverride=2000")
# # driver.implicitly_wait(10)
# # page_source = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='pdf']")))

# # soup = BeautifulSoup(page_source, 'html.parser')
# # for link in soup.find_all('a'):
# #     print(link.get('href'))

# # driver.quit()


# import json
# import re

# import requests
# from bs4 import BeautifulSoup


# def find_pdfs(data):
#     if isinstance(data, dict):
#         for k, v in data.items():
#             if k == "url" and ".pdf" in v:
#                 yield v
#             else:
#                 yield from find_pdfs(v)
#     elif isinstance(data, list):
#         for v in data:
#             yield from find_pdfs(v)


# url = "https://www.bain.com/insights/topics/energy-and-natural-resources-report/"

# soup = BeautifulSoup(requests.get(url).content, "html.parser")
# iframe_src = soup.iframe["src"]
# iframe_text = requests.get(iframe_src).text
# print(iframe_text)

# # 1. check if now iframe  have a href links that have .pdf extenction
# # 2. Check for form action or a javascript ajax/fetch call

# # section = iframe_text.find_all('href')
# # iframe_text = requests.get(iframe_src).content
# # iframes=soup.find_all('iframe')
# # for iframe in iframes:
# #     src=iframe['src']
# #     response = requests.get(src)
# #     if response.status_code == 200 :
# #         soup_src= BeautifulSoup(response.text,'html.parser')
# #         print(soup_src)


# # print(iframe_src)

# # doc = re.search(r"docVersion: (.*}),", iframe_text).group(1)
# # doc = json.loads(doc)

# # data = requests.get(doc["committedJsonUrl"]).text
# # data = re.search(r"(\{.*\})\);", data).group(1)
# # data = json.loads(data)

# # # print(json.dumps(data, indent=4))
# # pdfs = set(find_pdfs(data))
# # print(*pdfs, sep="\n")


# # https://www.bain.com/globalassets/noindex/2023/bain_report_engineering_and_r_and_d_report_2023.pdf
# # https://www.bain.com/globalassets/noindex/2022/bain_report_global-private-equity-report-2022.pdf
# # https://www.bain.com/globalassets/noindex/2023/bain_report_energy_and_natural_resources_2023.pdf








# import json
# import re

# import requests
# from bs4 import BeautifulSoup


# def find_pdfs(data):
#     if isinstance(data, dict):
#         for k, v in data.items():
#             if k == "url" and ".pdf" in v:
#                 yield v
#             else:
#                 yield from find_pdfs(v)
#     elif isinstance(data, list):
#         for v in data:
#             yield from find_pdfs(v)


# # url = "https://www.bain.com/insights/topics/energy-and-natural-resources-report/"

# # soup = BeautifulSoup(requests.get(url).content, "html.parser")
# # iframe_src = soup.iframe["src"]
# # iframe_text = requests.get(iframe_src).text

# # doc = re.search(r"docVersion: (.*}),", iframe_text).group(1)
# # doc = json.loads(doc)

# # data = requests.get(doc["committedJsonUrl"]).text
# # data = re.search(r"(\{.*\})\);", data).group(1)
# # data = json.loads(data)

# # # print(json.dumps(data, indent=4))
# # pdfs = set(find_pdfs(data))
# # print(*pdfs, sep="\n")


a = ["1","2","3","5"]
b = "4"
filtered = filter(lambda x: x == b, a)
if list(filtered):
    print("exists in the list")
else:
    print("does not exist in the list")
