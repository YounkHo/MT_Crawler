import requests
import random
import urllib
from urllib import parse

def get_ip_list():
    ip_list = []
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    url = "http://api3.xiguadaili.com/ip/?tid=556933875278591&num=201&protocol=https&delay=1"
    data = requests.get(url, header)
    for ip in data.text.split('\r\n'):
        ip_list.append(ip)
    return ip_list

def get_user_agent():
    user_agents = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/13.0.782.215)",
        "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/5.0 Opera 11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20130514 Firefox/21.0",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    ]
    user_agent = random.choice(user_agents)
    return user_agent

def get_proxy_from_pool():
    ip_pool = []
    with open("data/Http_Agent.txt", "r", encoding="utf-8") as fr:
        lines = fr.readlines()
        for line in lines:
            ip_pool.append(line.strip())
    return random.choice(ip_pool)

def test_proxy(ip_port, choice):
    proxies = None
    tar_url = "https://icanhazip.com/"
    user_agent = get_user_agent()
    headers = {'User-Agent': user_agent}
    if choice == 'http':
        proxies = {
            "http": "http://"+ip_port,
        }

    elif choice == 'https':
        proxies = {
            "https": "https://" + ip_port,
        }
    try:
        thisIP = "".join(ip_port.split(":")[0:1])
        res = requests.get(tar_url, proxies=proxies, headers=headers, timeout=8)
        print(thisIP, res.text)
        proxyIP = res.text.strip()
        if proxyIP == thisIP:
            return proxyIP
        else:
            return False
    except:
        return False

def store_txt(choice):
    """
    将测试通过的ip_port保存为txt文件
    :param choice:
    :return:
    """
    ip_list = get_ip_list()
    print(ip_list)
    with open("data/Http_Agent.txt", 'a', encoding='utf-8') as file:
        for ip_port in ip_list:
            ip_alive = test_proxy(ip_port, choice=choice)
            if ip_alive:
                file.write(ip_port+"\n")

if __name__ == "__main__":
    store_txt('https')