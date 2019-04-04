# -*- coding: utf-8 -*-

"""
IP工具类
"""

import ssl
import logging
import socket
from commands import getoutput
from datetime import datetime
from packages.workflow import web
from urlparse import urlparse

# 取消全局urllib的证书认证
ssl._create_default_https_context = ssl._create_unverified_context


class IP(object):
    @property
    def get_local(self):
        """
        获取本机内网ip
        >>> ip = IP()
        >>> ip.get_local != ''
        True
        """
        return getoutput('ipconfig getifaddr en0')

    @property
    def get_public(self):
        """
        获取本机公网ip
        >>> ip = IP()
        >>> ip.get_public is not None
        True
        """
        url = 'http://{year}.ip138.com/ic.asp'.format(year=datetime.now().strftime('%Y'))
        logging.debug('IP.get_public request url: {url}'.format(url=url))

        try:
            response = web.get(url)
            response.raise_for_status()
        except Exception as e:
            logging.warning('IP.get_public exception: {exception}'.format(exception=e))
            return None

        content = response.text
        logging.debug('IP.get_public response content: {content}'.format(content=content))
        if content.find('[') != -1 and content.find(']') != -1:
            return content[content.find('[')+1: content.find(']')]
        else:
            return None

    def resolve_from_dns(self, string):
        """
        从dns中解析ip
        >>> ip = IP()
        >>> ip.resolve_from_dns('127.0.0.1')
        ('127.0.0.1', '127.0.0.1')
        >>> ip.resolve_from_dns('https://www.baidu.com/query?key=1')[0]
        'www.baidu.com'
        >>> ip.resolve_from_dns('https://www.baidu.com/query?key=1')[1] is not None
        True
        >>> ip.resolve_from_dns('www.baidu.com')[0]
        'www.baidu.com'
        >>> ip.resolve_from_dns('www.baidu.com')[1] is not None
        True
        >>> ip.resolve_from_dns('test')
        ('test', None)
        """
        hostname = urlparse(string).hostname
        if hostname is None:
            hostname = string

        try:
            ip = socket.gethostbyname(hostname)
        except socket.gaierror as e:
            logging.warning('IP.resolve_from_dns exception: {exception}'.format(exception=e))
            ip = None

        return hostname, ip

    def get_location_information(self, ip):
        """
        获取ip的地址信息
        >>> ip = IP()
        >>> ip.get_location_information('8.8.8.8') is not None
        True
        >>> ip.get_location_information('test') is None
        True
        """
        url = 'https://clientapi.ipip.net/browser/chrome?ip={ip}'.format(ip=ip)
        logging.debug('IP.get_location_information request url: {url}'.format(url=url))

        try:
            response = web.get(url)
            response.raise_for_status()
        except Exception as e:
            logging.warning('IP.get_location_information exception: {exception}'.format(exception=e))
            return None

        logging.debug('IP.get_location_information response content: {content}'.format(content=response.text))
        response_data = response.json()
        if 0 == response_data['ret']:
            return response.json()['data']
        else:
            return None


if __name__ == '__main__':
    """
    文档测试
    """
    import doctest

    # 指定编码解码方式
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    doctest.testmod(verbose=False)
