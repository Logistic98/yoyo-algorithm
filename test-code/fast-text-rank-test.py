# -*- coding: utf-8 -*-

from uuid import uuid1
import requests
import json
from config import ip


# 测试FastTextRank
def fast_text_rank_test(text, type, method):
    # 测试请求
    global url
    if method == "keyword":
        url = 'http://{0}:{1}/fastTextRank/getKeyWord'.format(ip, "5000")
    elif method == "sentence":
        url = 'http://{0}:{1}/fastTextRank/getSentence'.format(ip, "5000")
    # 传输的数据格式
    data = {'text': text, 'type': type}
    # post传递数据
    r = requests.post(url, data=json.dumps(data))
    if type == "map" or type == "array":
        print(r.text.encode().decode('unicode_escape'))
    elif type == "file":
        file_path = './output/{}.csv'.format(uuid1())
        with open(file_path, 'wb') as f:
            f.write(r.content)


if __name__ == '__main__':

    print("1.测试提取关键词")
    print("1.1 以map形式返回")
    fast_text_rank_test("文本关键词及概要提取FastTextRank：从中文文本中提取摘要及关键词，并对算法时间复杂度进行了修改，"
                        "计算图最大权节点的时间复杂度由o（n^2）降低到了o（n）。在有限的测试文本上，其运行速度相比于textrank4zh这个包快了8倍。", "map", "keyword")
    print("1.2 以array形式返回")
    fast_text_rank_test("文本关键词及概要提取FastTextRank：从中文文本中提取摘要及关键词，并对算法时间复杂度进行了修改，"
                        "计算图最大权节点的时间复杂度由o（n^2）降低到了o（n）。在有限的测试文本上，其运行速度相比于textrank4zh这个包快了8倍。", "array", "keyword")
    print("1.3 以csv文件形式返回")
    fast_text_rank_test("文本关键词及概要提取FastTextRank：从中文文本中提取摘要及关键词，并对算法时间复杂度进行了修改，"
                        "计算图最大权节点的时间复杂度由o（n^2）降低到了o（n）。在有限的测试文本上，其运行速度相比于textrank4zh这个包快了8倍。", "file", "keyword")

    print("2.测试提取句子摘要")
    fast_text_rank_test("文本关键词及概要提取FastTextRank：从中文文本中提取摘要及关键词，并对算法时间复杂度进行了修改，"
                        "计算图最大权节点的时间复杂度由o（n^2）降低到了o（n）。在有限的测试文本上，其运行速度相比于textrank4zh这个包快了8倍。", "no", "sentence")