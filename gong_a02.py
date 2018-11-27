# to print all notices with url on board
import requests
from bs4 import BeautifulSoup

html = requests.get("https://www.bithumb.com").text
soup = BeautifulSoup(html, 'lxml')

global_div = soup.find('div', {"class":"global_width ct"})
dd_tags = soup.find_all('dd')

for dd_tag in dd_tags:
    message = dd_tag.get_text()
    print(message)

    a_tag = dd_tag.find('a')
    onclick_url = a_tag['onclick']
    pos = onclick_url.find('http')
    url = onclick_url[pos:-2]
    print(url)



