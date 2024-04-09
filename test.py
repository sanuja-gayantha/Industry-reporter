# import requests
# r = requests.get('https://jsonplaceholder.typicode.com/todos/1')
# r = requests.get('https://ipinfo.io/json')
# print(r.text)

import requests
from bs4 import BeautifulSoup as soup
from itertools import cycle


url = 'https://www.socks-proxy.net/'
response = requests.get(url)
bsobj = soup(response.content, features="lxml")


proxies= set()
for ip in bsobj.findAll('table')[0].findAll('tbody')[0].findAll('tr'):
  cols = ip.findChildren(recursive = False)
  cols = [element.text.strip() for element in cols]
  #print(cols)
  proxy = ':'.join([cols[0],cols[1]])
  proxy = 'socks4://'+proxy
  proxies.add(proxy)
  print(proxy)



proxy_pool = cycle(proxies)

url = 'https://ipinfo.io/json'
# url = 'https://httpbin.org/ip'
for i in range(1,10):
  #Get a proxy from the pool
  proxy = next(proxy_pool)
  print("Request #%d"%i)
  try:
    response = requests.get(url,proxies={"http": proxy, "https": proxy})
    print(response.json())
  except:
    pass