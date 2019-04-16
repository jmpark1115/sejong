from bs4 import BeautifulSoup
import requests
import time

#jmpark start
from selenium import webdriver
location = 'C:\ChromeDriver\chromedriver.exe'

driver = webdriver.Chrome(location)
driver.implicitly_wait(3)

baseurl = 'https://www.bithumb.com'

resp = requests.get(baseurl)
html = resp.text
soup = BeautifulSoup(html, 'lxml')

div = soup.find('div', {'class': 'global_width ct'})
# print(div)

dd = div.find('dd')
# print(dd)

print(dd.get_text())

a_tag = dd.find('a')
href = a_tag['onclick']
index = href.find('https')
url = href[13:-2]
print(url)

driver.get(url)
time.sleep(1)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

div = soup.find('div', {'class':'board-content col-12'})
ptags = div.find_all('p')

msg = []
for ptag in ptags:
    msg += ptag.get_text()

msg = ''.join(msg)
print(msg)





