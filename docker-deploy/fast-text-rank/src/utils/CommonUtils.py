# -*- coding: utf-8 -*-

from operator import itemgetter
from flask import Response

# 将文件转成文件流提供下载
def downloadFile(file_path):
    filename = file_path.split('/')[-1]
    # 流式读取下载
    def send_file():
        with open(file_path, 'rb') as targetfile:
            while 1:
                data = targetfile.read(20 * 1024 * 1024)   # 每次读取20M
                if not data:
                    break
                yield data

    response = Response(send_file(), content_type='application/octet-stream')
    response.headers["Content-disposition"] = 'attachment; filename=%s' % filename
    return response

# 实现replaceAll功能
def replaceAll(input, toReplace, replaceWith):
    while (input.find(toReplace) > -1):
        input = input.replace(toReplace, replaceWith)
    return input

# 按行读取txt文件的内容，保存成列表
def readTxtToList(txt_path):
    result = []
    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            result.append(line.strip('\n'))
    return result

# 按照词频降序排序
def sortByFrequency(keyword_count_dir):
    keyword_count_dir_unsorted = []
    for kv in keyword_count_dir.items():
        keyword_item = []
        keyword_item.append(kv[0])
        keyword_item.append(kv[1])
        keyword_count_dir_unsorted.append(keyword_item)
    keyword_count_sorted = sorted(keyword_count_dir_unsorted, key=itemgetter(1), reverse=True)
    return keyword_count_sorted




