#this source is to get simple ex01.tml
from bs4 import BeautifulSoup
import requests

#read file from network, zerobizcoin@nate.com
baseurl = 'http://13.125.232.188/quizbot/ex01'

html = requests.get(baseurl).text
soup = BeautifulSoup(html, 'lxml')

#bring text from p tag
exclass_div = soup.find("div", {'class':'ex_class'})
message_p = exclass_div.find("p")
print(message_p.get_text())

#bring text from p tags
exclass_div = soup.find("div", {"class":"ex_class"})
message_ps  = exclass_div.find_all('p')
print(message_ps[0].get_text())


"""
<!DOCTYPE html>
<html>
	<head>
		<title>Crawling Example 01</title>
	</head>
	<body>
    	<div>
            <p>0 aaaaaa</p>
            <p>1 bbbbbb</p>
            <p>2 cccccc</p>
        </div>
        <div class="ex_class">
            <p>3 dddddd</p>
            <p>4 eeeeee</p>
            <p>5 ffffff</p>
        </div>
        <div id="ex_id">
            <p>6 gggggg</p>
            <p>7 hhhhhh</p>
            <p>8 iiiiii</p>
        </div>
		<h1 class="h1_handling">It's headline-h1</h1>
        <h2 class="h2_handling">
            <a href="http://zerobizcamus.com">It's headline-h2</a>
        </h2>
		<p>9 It's 1st paragraph-p.</p>
		<p>10 It's 2nd paragraph-p.</p>
	</body>
</html>
"""

