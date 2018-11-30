from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import time
import requests

# https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EC%84%9C%EC%B4%88%EB%8F%99%EB%82%A0%EC%94%A8

def weather_info(**nalssi):

    print("weather_info %s" %nalssi)

    msg = u'지역을 찾지 못했습니다'

    try:
        area = nalssi['area']
        # area = nalssi
        area = area + ' 날씨'
        search = urllib.parse.quote(area)
    
        url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%s' % (search)

        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')

        # 오늘 날씨
        t1 = soup.find('p', {'class': 'info_temperature'}).get_text().strip()
    
        liList = soup.find('ul', {'class': 'info_list'}).find_all('li')
        t2 = liList[0].get_text().strip()
        t3 = liList[1].get_text().strip()
        t4 = liList[2].get_text().strip()
    
        dtList = soup.find('dl', {'class': 'indicator'}).find_all('dt')
        ddList = soup.find('dl', {'class': 'indicator'}).find_all('dd')
    
        t5 = dtList[0].get_text().strip() + ddList[0].get_text().strip()
        t6 = dtList[1].get_text().strip() + ddList[1].get_text().strip()
        t7 = dtList[2].get_text().strip() + ddList[2].get_text().strip()
    
        # 내일 날씨
        tomorrow = soup.find('div', {'class': 'tomorrow_area'})
    
        tm1 = tomorrow.find('p', {'class': 'info_temperature'}).get_text().strip()
    
        liList = tomorrow.find('ul', {'class': 'info_list'}).find_all('li')
        tm2 = liList[0].get_text().strip()
        tm3 = liList[1].get_text().strip()
    
        # 메세지 발송
        sendTiem = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
    
        # msg = "< {} {} 날씨 > \n" .format(sido.decode('utf-8'), gu.decode('utf-8'))
        msg = ""
        msg = "[" + sendTiem + "]" + "\n" + t1 + "\n" + t2 + "\n" + t3 + "\n" + t4 + "\n" + t5 + "\n" + t6 + "\n" + t7
        msg += "\n\n" + "[내일날씨]" + "\n" + tm1 + "\n" + tm2 + "\n" + tm3
    except:
        msg = u'지역을 찾지 못했습니다'
        
    return msg



if __name__ == '__main__' :
    
    params = {'area': '서초동'}
    msg = weather_info(**params)
    
    # msg = weather_info(area = '서초동')

    print(msg)