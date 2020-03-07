import base64
import zlib
import time
import datetime
import urllib

def decode_token(token):
    # base64解码
    token_decode = base64.b64decode(token.encode())
    print(token_decode)
    # 二进制解压
    token_string = zlib.decompress(token_decode)
    return token_string

def encode_sign(cate_id, page_idx, uuid):
    sign_params = '"areaId=0&cateId={}&cityName={}&dinnerCountAttrId=&optimusCode=10&originUrl=https://my.meituan.com/meishi/{}/&page={}&partner=126&platform=1&riskLevel=1&sort=&userId=&uuid={}"'.format(str(cate_id)[1:], str('绵阳'), str(cate_id), str(page_idx), str(uuid))
    # 二进制编码
    encode = str(sign_params).encode()
    # 二进制压缩
    compress = zlib.compress(encode)
    # base64编码
    b_encode = base64.b64encode(compress)
    # 转为字符串
    token = str(b_encode, encoding='utf-8')
    return token

# 生成token
def encode_token(cate_id, page_idx, uuid):
    ts = int(datetime.datetime.now().timestamp() * 1000)
    token_dict = {
        'rId': 100900,
        'ver': '1.0.6',
        'ts': ts,
        'cts': ts + 100 * 1000,
        'brVD': [875, 946],
        'brR': [[1920, 1080], [1920, 1057], 24, 24],
        'bI': ['https://nanchong.meituan.com/meishi/{}/'.format(str(cate_id)), ''],
        'mT': [],
        'kT': [],
        'aT': [],
        'tT': [],
        'aM': '',
        'sign': encode_sign(cate_id, page_idx, uuid)
    }
    # 二进制编码
    encode = str(token_dict).encode()
    # 二进制压缩
    compress = zlib.compress(encode)
    # base64编码
    b_encode = base64.b64encode(compress)
    # 转为字符串
    token = str(b_encode, encoding='utf-8')
    return urllib.parse.quote(token)

# token = "eJwdjU1OwzAQhe/ShZf+aZwmRfICdYWE2HEAxxm3FrEdjcdIvQn3QKw4EOIWjFi9T0/v5+AR/NPqtAiegGE4DyIkur/4DO7n++v341OsqRTAS+2FHomQU6LulHJvl7qCM1pUTNdUXnFzN6K9PSiV7zJDou6LDDUr5nZLKvC8Eru/cosFiXedOZ7EvnmKFTPbmNrbM7zDxtwqkhO9wf9p72l107TEMC/RnyZjo7WLHqM04zzY8zzaozRSS334A4DLSfc="

# if __name__ == "__main__":
#     print(encode_token())