import requests
import csv
import time
import cateid_util
import random
import math
import json
from get_token import encode_token
import proxy_util
import webbrowser

count = 0

def get_header(cate_id):
    header = {
            'Host': 'my.meituan.com',
            'Connection': 'close',
            'Accept': 'application/json',
            'Sec-Fetch-Dest': 'empty',
            # 'User-Agent': proxy_util.get_user_agent(),
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
            'DNT': '1',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://my.meituan.com/meishi/{}/'.format(str(cate_id)),
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
        }
    return header

def get_content(cate_id, uuid, token, page):
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    params = {
        'cityName': '绵阳',
        'cateId': str(cate_id)[1:],
        'areaId': 0,
        'sort': '',
        'dinnerCountAttrId': '',
        'page': page,
        'userId': '',
        'uuid': uuid,
        'platform': 1,
        'partner': 126,
        'originUrl': 'https://my.meituan.com/meishi/{}/'.format(str(cate_id)),
        'riskLevel': 1,
        'optimusCode': 10,
        '_token': token
    }
    proxy = {
        "https": "221.206.100.133:34073"
    }
    response = requests.get("https://my.meituan.com/meishi/api/poi/getPoiList", params=params, headers=get_header(cate_id)).text
    if ('您的网络好像不太给力，请稍后再试' in response):
        data = json.loads(response)
        webbrowser.open_new(data['customData']['verifyPageUrl'])
        capter = input("Please input capter: ")
        response = requests.get("https://my.meituan.com/meishi/api/poi/getPoiList", params=params, headers=get_header(cate_id)).text
    print(response)
    return json.loads(response)

def get_page_count(cate_id, uuid, token):
    content = get_content(cate_id, uuid, token, 1)
    return math.ceil(content['data']['totalCounts'] / 15)

def get_page_content(cate_id, uuid, page, token):
    global count
    content = get_content(cate_id, uuid, token, page)
    content = content['data']['poiInfos']
    page_content = []
    for item in content:
        page_content.append([count, item['poiId'], str(cate_id), item['frontImg'], item['title'], item['avgScore'], item['allCommentNum'], item['address'], item['avgPrice']])
        count += 1
    return page_content

if __name__ == "__main__":
    cate_ids = cateid_util.get_cate_ids()
    with open("data/shop_info.csv", "a", encoding="utf-8") as fw:
        writer = csv.writer(fw)
        writer.writerow(['id', 'poiId', 'cate_id', 'frontImg', 'title', 'avgScore', 'allCommentNum', 'address', 'avgPrice'])
        for cate_id in cate_ids[20:27]:
            # cate_id = 'c54'
            uuid = "77bfc8{}14f44b05f.1583498542.1.0.0".format(random.randint(10000,99999))
            token = encode_token(cate_id, 1, uuid)
            page_num = get_page_count(cate_id, uuid, token)
            print("**************现在开始获取：{} 类别, 共 {} 页**************".format(cateid_util.get_cate_name_by_id(cate_id), page_num))
            for idx in range(page_num):
                page_idx = idx + 1
                if (page_idx > 60):
                    break
                print("------------------------------现在开始获取：{} 类别的 {} 页------------------------------".format(cateid_util.get_cate_name_by_id(cate_id), str(page_idx)))
                page_content = get_page_content(cate_id, uuid, page_idx, token)
                # print(cate_id, page_num, page_content)
                writer.writerows(page_content)
                time.sleep(random.randint(0, 5))