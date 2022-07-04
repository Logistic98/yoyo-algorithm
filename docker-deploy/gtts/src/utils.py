# -*- coding: utf-8 -*-

import os
import urllib.parse
from flask import Response


# 检验是否含有中文字符
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


# 将文件转成文件流提供下载
def download_file(file_path):

    # 文件路径、文件名、后缀分割
    file_dir, file_full_name = os.path.split(file_path)
    file_name, file_ext = os.path.splitext(file_full_name)

    # 文件名如果包含中文则进行编码
    if is_contains_chinese(file_name):
        file_name = urllib.parse.quote(file_name)
    new_file_name = file_name + file_ext

    # 流式读取下载
    def send_file():
        with open(file_path, 'rb') as targetfile:
            while 1:
                data = targetfile.read(20 * 1024 * 1024)   # 每次读取20M
                if not data:
                    break
                yield data
    response = Response(send_file(), content_type='application/octet-stream')
    response.headers["Content-disposition"] = 'attachment; filename=%s' % new_file_name
    return response


# 实现replaceAll功能
def replaceAll(input, toReplace, replaceWith):
    while (input.find(toReplace) > -1):
        input = input.replace(toReplace, replaceWith)
    return input