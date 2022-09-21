# -*- coding: utf-8 -*-

import base64
import requests
import json
from config import ip


def image_feature_vector_test():
    # 测试请求
    url = 'http://{0}:{1}/imageFeatureVector/calFeatureVector'.format(ip, "5004")
    f = open('./img/ocr_test.png', 'rb')
    # base64编码
    base64_data = base64.b64encode(f.read())
    f.close()
    base64_data = base64_data.decode()
    # 传输的数据格式
    data = {'img': base64_data}
    # post传递数据
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(r.text)


if __name__ == '__main__':
    image_feature_vector_test()

