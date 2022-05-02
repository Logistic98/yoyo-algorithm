# -*- coding: utf-8 -*-

import time
import grequests
import requests
import json

from config import ip


#  将List拆分成若干个指定长度的小List
def list_of_groups(list, length):
    return [list[i:i + length] for i in range(0, len(list), length)]


# 测试GoogleTranslateCrack
def google_translate_crack_test(text, to_lang):
    url = 'http://{0}:{1}/googleTranslate/getTranslateResult'.format(ip, "5002")
    # 传输的数据格式
    data = {'text': text, 'to_lang': to_lang}
    # post传递数据
    r = requests.post(url, data=json.dumps(data))
    print(r.text)


# 测试GoogleTranslateCrack的并发调用
def google_translate_crack_batch_test(text_list, to_lang, concurrency):

    start = time.time()
    url = 'http://{0}:{1}/googleTranslate/getTranslateResult'.format(ip, "5002")

    text_groups_list = list_of_groups(text_list, concurrency)

    result_list = []
    for text_groups in text_groups_list:
        req_list = []
        for text in text_groups:
            data = {'text': text, 'to_lang': to_lang}
            req_list.append(grequests.post(url, data=json.dumps(data)))
        res_list = grequests.map(req_list)
        for res in res_list:
            result_list.append(res.text)

    print(len(result_list))
    print(result_list)
    print(time.time()-start)


if __name__ == '__main__':
    # 测试数据
    text = 'Due to limitations of the web version of google translate, ' \
           'this API does not guarantee that the library would work properly at all times. ' \
           'so please use this library if you don’t care about stability.'
    to_lang = 'zh-cn'
    # 单次调用
    google_translate_crack_test(text, to_lang)
    # 并发调用
    text_list = [text for i in range(20)]
    google_translate_crack_batch_test(text_list, to_lang, 5)