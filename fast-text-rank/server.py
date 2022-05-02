# -*- coding: utf-8 -*-

import csv
import json
import os
from collections import Counter
from uuid import uuid1

from flask import Flask, request, jsonify
from flask_cors import CORS

from code import ResponseCode, ResponseMessage
from log import logger
from utils.CommonUtils import readTxtToList, downloadFile, replaceAll, sortByFrequency
from utils.FastTextRank4Sentence import FastTextRank4Sentence
from utils.FastTextRank4Word import FastTextRank4Word

# 创建一个服务
app = Flask(__name__)
CORS(app, supports_credentials=True)

"""
# 从中文文本中提取关键词并统计词频
"""
@app.route(rule='/fastTextRank/getKeyWord', methods=['POST'])
def getKeyWord():

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
    check_type = ["map", "array", "file"]
    if not type:
        fail_response = dict(code=ResponseCode.RARAM_FAIL, msg=ResponseMessage.RARAM_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)
    if type not in check_type:
        fail_response = dict(code=ResponseCode.RARAM_FAIL, msg=ResponseMessage.RARAM_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)

    # 提取关键词
    try:
        # 从中文文本抽取关键词
        mod = FastTextRank4Word(tol=0.0001, window=2)
        keyword_list = mod.summarize(text)
        # 过滤无用关键词（stopwords里的、单个字的），并统计词频
        filter_txt = './stopwords/stopwords.txt'
        keyword_filter = readTxtToList(filter_txt)
        keyword_count_dir = Counter(keyword_list)
        filter_keyword = []
        for keyword in keyword_list:
            if keyword in keyword_filter and keyword not in filter_keyword:
                filter_keyword.append(keyword)
            else:
                if len(keyword) == 1 and keyword not in filter_keyword:
                    filter_keyword.append(keyword)
                else:
                    continue
        for keyword_item in filter_keyword:
            keyword_count_dir.pop(keyword_item)

    except Exception as e:
        logger.error(e)
        fail_response = dict(code=ResponseCode.BUSINESS_FAIL, msg=ResponseMessage.BUSINESS_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)

    # 按照词频降序排序
    keyword_count_sorted = sortByFrequency(keyword_count_dir)

    # 成功的结果返回
    if type == "file":
        try:
            # 生成csv文件
            csv_path = './tmp/{}.csv'.format(uuid1())
            if not os.path.exists('./tmp'):
                os.makedirs('./tmp')
            with open(csv_path, 'w', newline='', encoding='GBK') as f:
                csv_write = csv.writer(f)
                csv_head = ["关键词", "词频"]
                csv_write.writerow(csv_head)
                for csv_body_sort_item in keyword_count_sorted:
                    csv_write.writerow(csv_body_sort_item)
            return downloadFile(csv_path)
        except Exception as e:
            logger.error(e)
            fail_response = dict(code=ResponseCode.BUSINESS_FAIL, msg=ResponseMessage.BUSINESS_FAIL, data=None)
            logger.error(fail_response)
            return jsonify(fail_response)
    elif type == "map":
        # 以map的形式返回（未排序）
        success_response = dict(code=ResponseCode.SUCCESS, msg=ResponseMessage.SUCCESS, data=keyword_count_dir)
        logger.info(success_response)
        return jsonify(success_response)
    elif type == "array":
        # 以array的形式返回(已排序)
        success_response = dict(code=ResponseCode.SUCCESS, msg=ResponseMessage.SUCCESS, data=keyword_count_sorted)
        logger.info(success_response)
        return jsonify(success_response)


"""
# 从中文文本中提取句子摘要
"""
@app.route(rule='/fastTextRank/getSentence', methods=['POST'])
def getSentence():

    # 获取JSON格式的请求体，并解析
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

    # 提取句子概要
    try:
        # 从中文文本提取句子概要
        mod = FastTextRank4Sentence(use_w2v=False, tol=0.0001)
        sentence_list = mod.summarize(text)
        # 句子列表去重、去空
        last_sentence_list = list(set(sentence_list))
        for sentence in last_sentence_list:
            if sentence == "":
                last_sentence_list.remove(sentence)
    except Exception as e:
        logger.error(e)
        fail_response = dict(code=ResponseCode.BUSINESS_FAIL, msg=ResponseMessage.BUSINESS_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)

    # 成功的结果返回
    success_response = dict(code=ResponseCode.SUCCESS, msg=ResponseMessage.SUCCESS, data=last_sentence_list)
    logger.info(success_response)
    return jsonify(success_response)


if __name__ == '__main__':
    # 解决中文乱码问题
    app.config['JSON_AS_ASCII'] = False
    # 启动服务，指定主机和端口
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)