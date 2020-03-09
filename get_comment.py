import requests
import csv
import json
import random
import math

def get_shop_poiId_and_comment_count():
    poi_ids = []
    comment_counts = []
    with open("data/shopinfo_nodup.csv", "r", encoding="utf-8") as fr:
        reader = csv.reader(fr)
        next(reader)
        for item in reader:
            poi_ids.append(item[1])
            comment_counts.append(item[6])
    return poi_ids, comment_counts

def get_data(poiId, uuid):
    headers = {
        'Host': 'www.meituan.com',
        'Accept': 'application/json',
        'Sec-Fetch-Dest': 'empty',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'DNT': '1',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://www.meituan.com/meishi/{}/'.format(str(poiId)),
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    }
    params = {
        'uuid': uuid,
        'platform': '1',
        'partner': '126',
        'originUrl': 'https://www.meituan.com/meishi/{}/'.format(str(poiId)),
        'riskLevel': '1',
        'optimusCode': '10',
        'id': poiId,
        'userId': '',
        'offset': '0',
        'pageSize': '10',
        'sortType': '1'
    }
    response = requests.get("https://www.meituan.com/meishi/api/poi/getMerchantComment", params=params, headers=headers).text
    print(response)
    return json.loads(response)

def get_tag(response):
    keywords = {}
    tags = response['data']['tags']
    for item in tags:
        keywords[item['tag']] = item['count']
    return keywords

if __name__ == "__main__":
    poiIds, comment_counts = get_shop_poiId_and_comment_count()
    with open("data/comment.csv", "a", encoding="utf-8") as fw:
        writer = csv.writer(fw)
        writer.writerow(['userName', 'avgPrice' 'comment', 'picUrls', 'commentTime', 'zanCnt', 'userLevel', 'userId', 'star', 'anonymous'])
        for idx, poiId in enumerate(poiIds):
            uuid = "77bfc8{}14f44b05f.1583498542.1.0.0".format(random.randint(10000,99999))
            response = get_data(poiId, uuid)
            pageNum = math.ceil(comment_counts[idx] / 50)
            for i in range(pageNum):
                pageIdx = i + 1
                