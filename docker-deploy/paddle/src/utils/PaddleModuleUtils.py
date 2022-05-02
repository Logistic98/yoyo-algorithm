# -*- coding: utf-8 -*-

from paddleocr import PaddleOCR
from paddlenlp import Taskflow

# PaddleOCR：图片OCR识别
def get_paddle_ocr_result(img_path):
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    ocr_result = ocr.ocr(img_path, cls=True)
    result = []
    for line in ocr_result:
        result.append(line[1][0])
    return result

# PaddleNLP：自然语言处理
# 仅用于：中文分词(word_segmentation)、词性标注(pos_tagging)、名词短语标注(knowledge_mining)、情感分析(sentiment_analysis)
def get_paddle_nlp_result(str_line, type):
    if type == "knowledge_mining":
        paddle_nlp = Taskflow(type, model="nptag")
    else:
        paddle_nlp = Taskflow(type)
    result = paddle_nlp(str_line)
    return result
