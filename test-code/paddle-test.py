# -*- coding: utf-8 -*-

import base64
import requests
import json
from config import ip


# 测试PaddleOCR
def paddle_ocr_test():
    # 测试请求
    url = 'http://{0}:{1}/paddle/paddleOcr'.format(ip, "5001")
    f = open('./img/ocr_test.png', 'rb')
    # base64编码
    base64_data = base64.b64encode(f.read())
    f.close()
    base64_data = base64_data.decode()
    # 传输的数据格式
    data = {'img': base64_data}
    # post传递数据
    r = requests.post(url, data=json.dumps(data))
    print(r.text)


# 测试PaddleNLP
def paddle_nlp_test(text, type):
    # 测试请求
    url = 'http://{0}:{1}/paddle/paddleNlp'.format(ip, "5001")
    # 传输的数据格式
    data = {'text': text, 'type': type}
    # post传递数据
    r = requests.post(url, data=json.dumps(data))
    print(r.text)


if __name__ == '__main__':

    print("1.测试PaddleOCR")
    paddle_ocr_test()

    print("2.测试PaddleNLP")
    print("2.1 中文分词(word_segmentation)")
    paddle_nlp_test("第十四届全运会在西安举办", "word_segmentation")
    print("2.2 词性标注(pos_tagging)")
    paddle_nlp_test("第十四届全运会在西安举办", "pos_tagging")
    print("2.3 名词短语标注(knowledge_mining)")
    paddle_nlp_test("红曲霉菌", "knowledge_mining")
    print("2.4 情感分析(sentiment_analysis)")
    paddle_nlp_test("这个产品用起来真的很流畅，我非常喜欢", "sentiment_analysis")
