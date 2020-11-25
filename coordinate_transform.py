# ! /usr/bin/env python3
# -*- coding:utf-8 -*-

import math

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方


def bd09_to(lng, lat):
    """百度坐标转其他"""
    bd09_lng, bd09_lat = float(lng), float(lat)
    gcj02_lng, gcj02_lat = bd09_to_gcj02(bd09_lng, bd09_lat)
    wgs84_lng, wgs84_lat = gcj02_to_wgs84(gcj02_lng, gcj02_lat)

    data = {
        "bd09_lng": str(bd09_lng),
        "bd09_lat": str(bd09_lat),
        "gcj02_lng": str(gcj02_lng),
        "gcj02_lat": str(gcj02_lat),
        "wgs84_lng": str(wgs84_lng),
        "wgs84_lat": str(wgs84_lat),
    }

    return data


def gcj02_to(lng, lat):
    """百度坐标转其他"""
    gcj02_lng, gcj02_lat = float(lng), float(lat)
    bd09_lng, bd09_lat = gcj02_to_bd09(gcj02_lng, gcj02_lat)
    wgs84_lng, wgs84_lat = gcj02_to_wgs84(gcj02_lng, gcj02_lat)

    data = {
        "bd09_lng": str(bd09_lng),
        "bd09_lat": str(bd09_lat),
        "gcj02_lng": str(gcj02_lng),
        "gcj02_lat": str(gcj02_lat),
        "wgs84_lng": str(wgs84_lng),
        "wgs84_lat": str(wgs84_lat),
    }

    return data


def gcj02_to_bd09(lng, lat):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    :param lng:火星坐标经度
    :param lat:火星坐标纬度
    :return:
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]


def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]


def wgs84_to_gcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    if out_of_china(lng, lat):  # 判断是否在国内
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]


def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def bd09_to_wgs84(bd_lon, bd_lat):
    lon, lat = bd09_to_gcj02(bd_lon, bd_lat)
    return gcj02_to_wgs84(lon, lat)


def wgs84_to_bd09(lon, lat):
    lon, lat = wgs84_to_gcj02(lon, lat)
    return gcj02_to_bd09(lon, lat)


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)


def out_of_duobianxing(lng, lat, duobianxing):
    """判断坐标点是否在多边形范围内

    Args:
        lng: 经度
        lat: 维度
        duobianxing: 121.51816552554746,31.05266457956204;121.60808277372263,31.05266457956204;121.60808277372263,31.102357646715326;121.51816552554746,31.102357646715326

    Returns:
        121.51816552554746,31.05266457956204;121.60808277372263,31.05266457956204;121.60808277372263,31.102357646715326;121.51816552554746,31.102357646715326
        121.51816552554746,31.102357646715326;121.60808277372263,31.102357646715326;121.60808277372263,31.15205071386861;121.51816552554746,31.15205071386861
        121.51816552554746,31.15205071386861;121.60808277372263,31.15205071386861;121.60808277372263,31.201743781021896;121.51816552554746,31.201743781021896
        121.60808277372263,31.05266457956204;121.69800002189783,31.05266457956204;121.69800002189783,31.102357646715326;121.60808277372263,31.102357646715326
        121.60808277372263,31.102357646715326;121.69800002189783,31.102357646715326;121.69800002189783,31.15205071386861;121.60808277372263,31.15205071386861
        121.60808277372263,31.15205071386861;121.69800002189783,31.15205071386861;121.69800002189783,31.201743781021896;121.60808277372263,31.201743781021896
        121.69800002189783,31.05266457956204;121.787917270073,31.05266457956204;121.787917270073,31.102357646715326;121.69800002189783,31.102357646715326
        121.69800002189783,31.102357646715326;121.787917270073,31.102357646715326;121.787917270073,31.15205071386861;121.69800002189783,31.15205071386861
        121.69800002189783,31.15205071386861;121.787917270073,31.15205071386861;121.787917270073,31.201743781021896;121.69800002189783,31.201743781021896
    """
    lng = float(lng)
    lat = float(lat)

    min_point = duobianxing.split(";")[0].split(",")  # ['121.51816552554746', '31.05266457956204']
    max_point = duobianxing.split(";")[2].split(",")  # ['121.60808277372263', '31.102357646715326']

    min_point = [float(i) for i in min_point]
    max_point = [float(i) for i in max_point]

    assert (min_point[0] < max_point[0]) and (
            min_point[1] < max_point[1]), "Error lnglat: min_point is bigger than max_point!!!"

    # 判断目标点是否在多边形范围内
    if (min_point[0] < lng < max_point[0]) and (min_point[1] < lat < max_point[1]):
        print("存在： ", duobianxing)
        return duobianxing


if __name__ == '__main__':
    lng, lat = "113.71147169605", "34.800301319151"
    bd09_to(lng, lat)
