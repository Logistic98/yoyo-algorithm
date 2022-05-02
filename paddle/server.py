# -*- coding: utf-8 -*-

import os
from uuid import uuid1
import json

from flask import Flask, request, jsonify
from flask_cors import CORS

from code import ResponseCode, ResponseMessage
from log import logger
from utils.CommonUtils import base64_to_img, replaceAll
from utils.PaddleModuleUtils import get_paddle_nlp_result, get_paddle_ocr_result

# 创建一个服务
app = Flask(__name__)
CORS(app, supports_credentials=True)

"""
# PaddleOCR：图片OCR内容识别算法
"""
@app.route(rule='/paddle/paddleOcr', methods=['POST'])
def getOcrText():

    # 从请求中解析出图像的base64字符串
    request_data = request.get_data(as_text=True)
    request_data = ''.join(request_data.split())
    request_body = json.loads(request_data)

    image_b64 = request_body.get("img")
    if not image_b64:
        fail_response = dict(code=ResponseCode.RARAM_FAIL, msg=ResponseMessage.RARAM_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)

    # 将base64字符串解析成图片保存
    if not os.path.exists('./tmp'):
        os.makedirs('./tmp')
    uuid = uuid1()
    img_path = './tmp/{}.jpg'.format(uuid)
    base64_to_img(image_b64, img_path)

    # 读取图片获取ocr识别结果
    try:
        result = get_paddle_ocr_result(img_path)
    except Exception as e:
        os.remove(img_path)
        logger.error(e)
        fail_response = dict(code=ResponseCode.BUSINESS_FAIL, msg=ResponseMessage.BUSINESS_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)

    # OCR识别完后删除生成的图片文件
    os.remove(img_path)

    # 成功的结果返回
    success_response = dict(code=ResponseCode.SUCCESS, msg=ResponseMessage.SUCCESS, data=result)
    logger.info(success_response)
    return jsonify(success_response)

    # 最终对请求进行响应
    return response_body

"""
# PaddleNLP：自然语言处理算法
# 只封装了中文分词(word_segmentation)、词性标注(pos_tagging)、名词短语标注(knowledge_mining)、情感分析(sentiment_analysis)
"""
@app.route(rule='/paddle/paddleNlp', methods=['POST'])
def getEmotionAnalysis():

    # 获取JSON格式的请求体，并解析
    global csv_path
    request_data = request.get_data(as_text=True)
    request_data = ''.join(request_data.split())
    request_body = json.loads(request_data)

    # 参数获取及校验模块
    text = request_body.get("text")
    if not text:
        fail_response = dict(code=ResponseCode.RARAM_FAIL, msg=ResponseMessage.RARAM_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)
    text = replaceAll(replaceAll(replaceAll(replaceAll(text, '\r', ''), '\n', ''), '\u3000', ''), '\x01', '')
    type = request_body.get("type")
    check_type = ["word_segmentation", "pos_tagging", "knowledge_mining", "sentiment_analysis"]
    if not type:
        fail_response = dict(code=ResponseCode.RARAM_FAIL, msg=ResponseMessage.RARAM_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)
    if type not in check_type:
        fail_response = dict(code=ResponseCode.RARAM_FAIL, msg=ResponseMessage.RARAM_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)

    # 调用自然语言处理算法
    try:
        result = get_paddle_nlp_result(text, type)
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
    # 启动服务 指定主机和端口
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)



