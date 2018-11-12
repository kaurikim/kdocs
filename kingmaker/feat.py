# -*- coding: utf-8 -*-

import json
import requests
import copy
from bs4 import BeautifulSoup

fdb = dict()
rinfos = dict()

class FInfo:
    def __init__(self, finfo):
        self.name = finfo.get('name')
        self.descp = finfo.get('desc')
        self.reqs = copy.deepcopy(finfo.get('prereq'))
        self.plist = list()
        self.is_root = False
        if len(self.reqs) == 0:
            self.is_root = True

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

html = get_html('tst')

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
    if len(reqs) > 0:
        finfo['prereq'] = [req.strip() for req in reqs.split(',')]
    else:
        finfo['prereq'] = list()

    print finfo['prereq']

    tmp = tmp.find_next_sibling()
    finfo['desc'] = replace_non_ascii_unicode(tmp.text.strip(), '')
    name = finfo['name']
    infos[name] = finfo
    tmp = FInfo(finfo)
    fdb[name] = tmp
    '''
    if tmp.is_root:
        rinfos[name] = tmp
    '''
    rinfos[name] = tmp


#dd = json.dumps(infos, indent=4)
#print dd

for name, info in rinfos.items():
    msg = '{} >> {} :'.format(name, info.reqs)
    for req in info.reqs:
        dst = fdb.get(req, None)
        if dst:
            msg = msg + ' {}'.format(dst.name)
        else:
            print '{} is not exist.'.format(req)

    print msg




#for key, data in infos.items():
#    print '{} >> {}'.format(key, data.get('prereq'))
