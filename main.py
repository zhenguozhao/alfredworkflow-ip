# -*- coding: utf-8 -*-

import sys
import logging
from app.setting import LOGGING_SETTING, LOGGING_LEVEL
from app.ip import IP
from app.packages.workflow import Workflow3, ICON_NETWORK, ICON_ERROR

# 指定编码解码方式
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(**LOGGING_SETTING)

def main(workflow):
    ip_tool = IP()
    args = workflow.args
    if 1 > len(args):
        hostname = ip = workflow.cached_data('ip-local-{ip}'.format(ip=ip_tool.get_local), lambda : ip_tool.get_public, max_age=600)
    else:
        hostname, ip = ip_tool.resolve_from_dns(str(args[0]).strip())
    location_information = workflow.cached_data('ip-location-cached-data-{ip}'.format(ip=ip), lambda : ip_tool.get_location_information(ip), max_age=600)
    if location_information is not None:
        # 显示的地址，减少重复显示
        location_list = []
        for i in [location_information['country'], location_information['province'], location_information['city']]:
            if i not in location_list:
                location_list.append(i)
        location = '-'.join(location_list)

        subtitle = '{ip} {location} {isp}'.format(ip=ip, location=location, isp=location_information['isp'])
        arg = 'https://www.ipip.net/ip/{ip}.html'.format(ip=ip)
        # @todo icon设置国家的国旗
        workflow.add_item(title=hostname, subtitle=subtitle, valid=True, arg=arg, icon=ICON_NETWORK)
    else:
        workflow.add_item('暂没有 "{hostname}" 的信息'.format(hostname=hostname), icon=ICON_ERROR)
    workflow.send_feedback()


if __name__ == '__main__':
    workflow = Workflow3()
    workflow.logger.setLevel(LOGGING_LEVEL)
    sys.exit(workflow.run(main))
