# -*- coding: utf-8 -*-

import json
import requests

from config import ip

# 测试GeoIP2
def domain_parse_location_test(param):
    url = 'http://{0}:{1}/geoIp/getDomainOrIpLocation'.format(ip, "5005")
    # 传输的数据格式
    data = {'param': param}
    # post传递数据
    r = requests.post(url, data=json.dumps(data))
    print(r.text)


if __name__ == '__main__':
    domain_parse_location_test('www.baidu.com')
    domain_parse_location_test('104.193.88.123')
