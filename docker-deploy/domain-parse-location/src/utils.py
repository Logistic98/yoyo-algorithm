# -*- coding: utf-8 -*-

import socket
import geoip2.database

reader = geoip2.database.Reader('GeoLite2-City.mmdb')


# 通过域名获取IP（输入为IP的话保持不变）
def get_ip_by_domain(domain):
    address = socket.getaddrinfo(domain, None)
    return address[0][4][0]


# 查询IP地址对应的地理信息
def ip_get_location(ip):
    # 载入指定IP相关数据
    response = reader.city(ip)
    # 读取国家代码
    country_iso_code = str(response.country.iso_code)
    # 读取国家名称
    country_name = str(response.country.name)
    # 读取国家名称(中文显示)
    country_name_cn = str(response.country.names['zh-CN'])
    # 读取州(国外)/省(国内)名称
    country_specific_name = str(response.subdivisions.most_specific.name)
    # 读取州(国外)/省(国内)代码
    country_specific_iso_code = str(response.subdivisions.most_specific.iso_code)
    # 读取城市名称
    city_name = str(response.city.name)
    # 获取纬度
    location_latitude = str(response.location.latitude)
    # 获取经度
    location_longitude = str(response.location.longitude)
    # 返回结果
    result_dic = {}
    result_dic['ip'] = ip
    result_dic['country_iso_code'] = country_iso_code
    result_dic['country_name'] = country_name
    result_dic['country_name_cn'] = country_name_cn
    result_dic['country_specific_name'] = country_specific_name
    result_dic['country_specific_iso_code'] = country_specific_iso_code
    result_dic['city_name'] = city_name
    result_dic['location_latitude'] = location_latitude
    result_dic['location_longitude'] = location_longitude
    return result_dic
