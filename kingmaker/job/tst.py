
from bs4 import BeautifulSoup
import requests

URL = "http://comic.naver.com/webtoon/list.nhn?titleId=20853&weekday=tue&page=1"

def get_html(url):
    f = open('a.html')
    return f
    _html = ""
    resp = requests.get(url)
    if resp.status_code == 200:
        _html = resp.text
    #print resp.json()
    return _html

html = get_html(URL)

soup = BeautifulSoup(html, 'html.parser')

webtoon_area = soup.find("table",
        {"class": "wikitable mw-collapsible"}
        )

finfos = {}

for tmp in webtoon_area.find_all('tr'):
    name = tmp.find('th').text
    tmp = tmp.find('td')
    if not tmp:
        print 'skip'
        continue

    finfos['name'] = name.strip()
    finfos['prereq'] = tmp.text.strip()

    print '{} '.format(finfos)
    break
