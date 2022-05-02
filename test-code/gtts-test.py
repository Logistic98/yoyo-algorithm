# -*- coding: utf-8 -*-

import os
from uuid import uuid1
import requests
import json
from config import ip
from playsound import playsound


# 测试gTTS文本合成语音
def gtts_test(text, lang):
    # 测试请求
    url = 'http://{0}:{1}/gtts/textToVoice'.format(ip, "5003")
    # 传输的数据格式
    data = {'text': text, 'lang': lang}
    # post传递数据
    r = requests.post(url, data=json.dumps(data))
    # 写入文件
    file_path = './output/{}.mp3'.format(uuid1())
    with open(file_path, 'ab') as file:
        file.write(r.content)
        file.flush()
    # 播放语音
    playsound(file_path)
    # 删除语音文件
    os.remove(file_path)


if __name__ == '__main__':

    print("测试文本合成语音")
    gtts_test("Python library and CLI tool to interface with Google Translate's text-to-speech API", "en")