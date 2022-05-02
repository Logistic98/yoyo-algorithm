# -*- coding: utf-8 -*-

import json
import os
from uuid import uuid1

from flask import Flask, request, jsonify
from flask_cors import CORS
from gtts import gTTS

from code import ResponseCode, ResponseMessage
from log import logger
from base_config import PROXY_OPEN, PROXY_URL, LANGUAGES
from utils import replaceAll, downloadFile

# 是否开启代理
if PROXY_OPEN:
    os.environ["https_proxy"] = PROXY_URL

# 创建一个服务
app = Flask(__name__)
CORS(app, supports_credentials=True)

"""
# 使用gTTS将文本转语音提供文件下载
"""
@app.route(rule='/gtts/textToVoice', methods=['POST'])
def textToVoice():

    # 获取JSON格式的请求体，并解析
    request_data = request.get_data(as_text=True)
    request_body = json.loads(request_data)

    # 参数获取及校验模块
    text = request_body.get("text")
    if not text:
        fail_response = dict(code=ResponseCode.RARAM_FAIL, msg=ResponseMessage.RARAM_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)
    text = replaceAll(replaceAll(replaceAll(replaceAll(text, '\r', ''), '\n', ''), '\u3000', ''), '\x01', '')
    lang = request_body.get("lang")
    if not lang:
        fail_response = dict(code=ResponseCode.RARAM_FAIL, msg=ResponseMessage.RARAM_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)
    if lang not in LANGUAGES:
        fail_response = dict(code=ResponseCode.RARAM_FAIL, msg=ResponseMessage.RARAM_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)

    # 将文本转语音并提供mp3文件下载
    try:
        mp3_path = './tmp/{}.mp3'.format(uuid1())
        if not os.path.exists('./tmp'):
            os.makedirs('./tmp')
        audio = gTTS(text=text, lang=lang)
        audio.save(mp3_path)
        return downloadFile(mp3_path)
    except Exception as e:
        logger.error(e)
        fail_response = dict(code=ResponseCode.BUSINESS_FAIL, msg=ResponseMessage.BUSINESS_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)


if __name__ == '__main__':
    # 解决中文乱码问题
    app.config['JSON_AS_ASCII'] = False
    # 启动服务，指定主机和端口
    app.run(host='0.0.0.0', port=5003, debug=False, threaded=True)