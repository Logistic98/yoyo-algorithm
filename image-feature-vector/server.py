# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask_cors import CORS
from pre_request import pre, Rule
import base64
import numpy as np
import cv2
import extract_vgg19_keras as search

from code import ResponseCode, ResponseMessage
from log import logger

app = Flask(__name__)
CORS(app, supports_credentials=True)
model = search.VGG19Net()


def base64_cv2(base64_str):
    imgString = base64.b64decode(base64_str)
    nparr = np.fromstring(imgString, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image = cv2.resize(image, (224, 224))
    return image


@app.route('/imageFeatureVector/calFeatureVector', methods=['post'])
def imageFeatureVector():

    # 参数校验并获取参数
    rule = {
        "img": Rule(type=str, required=True)
    }
    try:
        params = pre.parse(rule=rule)
        image_b64 = params.get("img")
    except Exception as e:
        logger.error(e)
        fail_response = dict(code=ResponseCode.RARAM_FAIL, msg=ResponseMessage.RARAM_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)

    # 计算图片特征向量
    try:
        image_file = base64_cv2(image_b64)
        newvector = model.main_model(image_file).tolist()
    except Exception as e:
        logger.error(e)
        fail_response = dict(code=ResponseCode.BUSINESS_FAIL, msg=ResponseMessage.BUSINESS_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)

    # 成功的结果返回
    success_response = dict(code=ResponseCode.SUCCESS, msg=ResponseMessage.SUCCESS, data=newvector)
    logger.info(success_response)
    return jsonify(success_response)


if __name__ == '__main__':
    # 解决中文乱码问题
    app.config['JSON_AS_ASCII'] = False
    # 启动服务 指定主机和端口
    app.run(host='0.0.0.0', port=5004, debug=False)
