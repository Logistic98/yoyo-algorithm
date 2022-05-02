# -*- coding: utf-8 -*-

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