# to print one notice with url on the top of board
import requests
from bs4 import BeautifulSoup

html = requests.get("https://www.bithumb.com").text
soup = BeautifulSoup(html, 'lxml')

global_div = soup.find('div', {"class":"global_width ct"})
dd_tags = soup.find_all('dd')
message = dd_tags[0].get_text()
print(message)

a_tag = dd_tags[0].find('a')
onclick_url = a_tag['onclick']
pos = onclick_url.find('http')
url = onclick_url[pos:-2]
print(url)


