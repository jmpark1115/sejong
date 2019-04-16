from bs4 import BeautifulSoup
import requests

baseurl = 'https://www.bithumb.com'

resp = requests.get(baseurl)
html = resp.text
soup = BeautifulSoup(html, 'lxml')

div = soup.find('div', {'class': 'global_width ct'})
# print(div)

dd = div.find('dd')
# print(dd)

# 공지사항 메시지를 출력한다
print(dd.get_text())

# 해당 공지사항 url 을 출력한다
a_tag = dd.find('a')
href = a_tag['onclick']
index = href.find('https')
url = href[13:-2]
print(url)





