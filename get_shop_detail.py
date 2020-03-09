import requests
import re
import json
import csv
import time
import random

def get_shop_poiId():
    poi_ids = []
    with open("data/shopinfo_nodup.csv", "r", encoding="utf-8") as fr:
        reader = csv.reader(fr)
        next(reader)
        for item in reader:
            poi_ids.append(item[1])
    return poi_ids
            
def get_data(poiId):
    header = {
        'Host': 'www.meituan.com',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        'Sec-Fetch-Dest': 'document',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Referer': 'https://my.meituan.com/meishi/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    }
    url = "https://www.meituan.com/meishi/{}/".format(str(poiId))
    response = requests.get(url, headers=header).text
    return response

def get_detail(response):
    script = re.findall(r'window._appState =*[\s\S]*?<\/script>', response)
    shop_details = json.loads(script[0][18:-10])
    detail = shop_details['detailInfo']
    return [detail['poiId'], detail['name'], detail['avgScore'], detail['address'], detail['phone'], detail['openTime'], detail['extraInfos'], detail['hasFoodSafeInfo'], detail['longitude'], detail['latitude'], detail['avgPrice'], detail['brandId'], detail['brandName'], detail['showStatus']]

if __name__ == "__main__":
    with open("data/shop_details.csv", "a", encoding="utf-8") as fw:
        writer = csv.writer(fw)
        poiIds = get_shop_poiId()

        writer.writerow(['poiId', 'name', 'avgScore', 'address', 'phone', 'openTime', 'extraInfos', 'hasFoodSafeInfo', 'longitude', 'latitude', 'avgPrice', 'brandId', 'brandName', 'showStatus'])
        for poiId in poiIds[1647:1746]:
            print("************* 现在开始爬取:{} *************".format(poiId))
            res = get_data(poiId)
            data = get_detail(res)
            print(data)
            writer.writerow(data)
            time.sleep(random.randint(0, 3))