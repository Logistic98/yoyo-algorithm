# -*- coding: utf-8 -*-

import json
from flask import Flask, request, jsonify
from flask_cors import CORS

from code import ResponseCode, ResponseMessage
from log import logger
from utils import get_ip_by_domain, ip_get_location

# 创建一个服务
app = Flask(__name__)
CORS(app, supports_credentials=True)

"""
# 获取域名或IP的地理位置信息
"""
@app.route(rule='/geoIp/getDomainOrIpLocation', methods=['POST'])
def getDomainOrIpLocation():

    # 获取JSON格式的请求体，并解析
    request_data = request.get_data(as_text=True)
    request_body = json.loads(request_data)

    # 参数校验
    param = request_body.get("param")
    if not param:
        fail_response = dict(code=ResponseCode.RARAM_FAIL, msg=ResponseMessage.RARAM_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)

    # 将域名转换成IP（输入为IP的话保持不变）
    try:
        ip = get_ip_by_domain(param)
    except Exception as e:
        logger.error(e)
        fail_response = dict(code=ResponseCode.BUSINESS_FAIL, msg=ResponseMessage.BUSINESS_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)

    # 根据IP获取地理位置信息
    try:
        result = ip_get_location(ip)
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
    app.run(host='0.0.0.0', port=5005, debug=False, threaded=True)