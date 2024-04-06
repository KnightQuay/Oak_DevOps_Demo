import datetime
import hashlib
import time

from rest_framework.views import exception_handler


def md5value(key):
    input_name = hashlib.md5()
    input_name.update(key.encode("utf-8"))
    md5str = (input_name.hexdigest()).lower()
    print('计算md5:', md5str)
    return md5str


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def get_ip(request):
    """
    获取请求者的IP信息
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_ua(request):
    """
    获取请求者的IP信息
    """
    ua = request.META.get('HTTP_USER_AGENT')
    return ua[0:200]



