# -*- coding: utf-8 -*-

import json
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from googletrans import Translator

from code import ResponseCode, ResponseMessage
from log import logger
from base_config import PROXY_OPEN, PROXY_URL, LANGUAGES

# 是否开启代理
if PROXY_OPEN:
    os.environ["https_proxy"] = PROXY_URL

# 初始化py-googletrans
translator = Translator()

# 按指定长度分段切割字符串或列表
def cut(obj, sec):
    return [obj[i:i+sec] for i in range(0,len(obj),sec)]

# 创建一个服务
app = Flask(__name__)
CORS(app, supports_credentials=True)

"""
# 使用py-googletrans库破解Google翻译来获取翻译后的文本
"""
@app.route(rule='/googleTranslate/getTranslateResult', methods=['POST'])
def getTranslateResult():

    # 获取JSON格式的请求体，并解析
    request_data = request.get_data(as_text=True)
    request_body = json.loads(request_data)


    # 参数获取及校验模块
    text = request_body.get("text")
    if not text:
        fail_response = dict(code=ResponseCode.RARAM_FAIL, msg=ResponseMessage.RARAM_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)
    to_lang = request_body.get("to_lang")
    if not to_lang:
        fail_response = dict(code=ResponseCode.RARAM_FAIL, msg=ResponseMessage.RARAM_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)
    if to_lang not in LANGUAGES:
        fail_response = dict(code=ResponseCode.RARAM_FAIL, msg=ResponseMessage.RARAM_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)

    # 将text按照5000字符的长度进行切分（API限制单次只能5000字符以内，超出则多次请求，拼接结果）
    text_list = cut(text, 5000)

    # 获取翻译后的文本（来源语言自动检测）
    try:
        result = ''
        for text_item in text_list:
            result = result + ' ' + translator.translate(text_item, dest=to_lang).text
    except Exception as e:
        logger.error(e)
        fail_response = dict(code=ResponseCode.BUSINESS_FAIL, msg=ResponseMessage.BUSINESS_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)

    # 成功的结果返回
    success_response = dict(code=ResponseCode.SUCCESS, msg=ResponseMessage.SUCCESS, data=result)
    logger.info(success_response)
    return jsonify(success_response)


if __name__ == '__main__':
    # 解决中文乱码问题
    app.config['JSON_AS_ASCII'] = False
    # 启动服务，指定主机和端口
    app.run(host='0.0.0.0', port=5002, debug=False, threaded=True)