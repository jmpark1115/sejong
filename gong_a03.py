# to print one notice and content on board
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

# read content
html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')

content_div = soup.find('div',{'class':'board-content col-12'})
content_ps = content_div.find_all('p')

message = []
for content_p in content_ps:
    message += content_p.get_text().replace('\n','')
message = ''.join(message)
print(message)




