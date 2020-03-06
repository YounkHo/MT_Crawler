import requests
import csv
import time
from bs4 import BeautifulSoup
import re

HEADER = {
    'Host': 'my.meituan.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'Sec-Fetch-Dest': 'document',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cookie': 'uuid=bb55f64c93584506bf82.1583465518.1.0.0; _lxsdk_cuid=170ade65acbc8-0b76fefcea06f5-39687407-1fa400-170ade65acbc8; ci=306; rvct=306; __mta=188513559.1583465529614.1583465540995.1583465564920.3; client-id=5ddd113d-24a2-41b3-b085-cf9745f137f7; _lxsdk_s=170ade65acd-6d5-b88-3c%7C%7C14'
}

response = requests.get(url='https://my.meituan.com/meishi/', headers=HEADER).text
html_data = BeautifulSoup(response, 'lxml')
category_all = html_data.select('ul[data-reactid="20"]')[0]
category = category_all.select('li')
with open('data/cate_id.csv', "w", encoding="utf-8") as fo:
    writer = csv.writer(fo)
    writer.writerow(['id', 'cate_id', 'cate_name'])
    for index, cate_item in enumerate(category):
        writer.writerow([index, cate_item.a['href'].split('/')[-2], cate_item.a.string])