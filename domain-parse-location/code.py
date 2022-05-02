# -*- coding: utf-8 -*-


class ResponseCode(object):
    SUCCESS = 200
    RARAM_FAIL = 500
    BUSINESS_FAIL = 500


class ResponseMessage(object):
    SUCCESS = "请求成功"
    RARAM_FAIL = "参数校验失败"
    BUSINESS_FAIL = "业务处理失败"