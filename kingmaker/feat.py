# -*- coding: utf-8 -*-

import json
import requests
from bs4 import BeautifulSoup
from unicode_string_utils import open_file_read_unicode

URL = "http://comic.naver.com/webtoon/list.nhn?titleId=20853&weekday=tue&page=1"

class FInfo:
    def __init__(self, name, descp, reqs):
        self.name = name
        self.descp = descp
        self.descp = reqs

def crt_finfo(name, reqstr, desc):
    req = reqstr, d


def get_html(url):
    with open('a.html') as f:
        data = f.read()
    return data
    _html = ""
    resp = requests.get(url)
    if resp.status_code == 200:
        _html = resp.text
    #print resp.json()
    return _html


def get_json():
    with open('../enGB.json') as f:
        data = json.load(f)
    return data

html = get_html(URL)

soup = BeautifulSoup(html, 'html.parser')

webtoon_area = soup.find("table",
        {"class": "wikitable mw-collapsible"}
        )


def replace_non_ascii_unicode(s, replacement='?'):
  return "".join([(c if (ord(c) < 128) else replacement) for c in s])


infos = dict()
for tmp in webtoon_area.find_all('tr'):
    name = tmp.find('th').text
    tmp = tmp.find('td')
    if not tmp:
        print 'skip'
        continue

    finfo = dict()

    tst = name.strip()
    finfo['name'] = replace_non_ascii_unicode(tst, '')
    reqs = replace_non_ascii_unicode(tmp.text.strip(), '')
    reqs = reqs.replace(' ', '')
    finfo['prereq'] = [req.strip() for req in reqs.split(',')]

    tmp = tmp.find_next_sibling()
    finfo['desc'] = replace_non_ascii_unicode(tmp.text.strip(), '')
    name = finfo['name']
    infos[name] = finfo


dd = json.dumps(infos, indent=4)
print dd


#for key, data in infos.items():
#    print '{} >> {}'.format(key, data.get('prereq'))
