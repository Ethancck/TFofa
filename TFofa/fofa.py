import requests
import base64
import pandas as pd
from core.banner import banner
from core.log import logger
from core.cmdline import args
from core.conf import email,key
from core.cidr import ip2cidr,saveContext
import json
logger=logger()
cmd=args.__dict__
num = 0
class FofaAPI(object):
    def __init__(self, email, key):
        self.email = email
        self.key = key
        self.base_url = 'https://fofa.so'
        self.search_api_url = '/api/v1/search/all'
        self.login_api_url = '/api/v1/info/my'
        self.get_userinfo()

    def get_userinfo(self):
        try:
            url = '{url}{api}'.format(url=self.base_url, api=self.login_api_url)
            data = {"email": self.email, 'key': self.key}
            req = requests.get(url, params=data)
            return req.json()
        except requests.exceptions.ConnectionError:
            error_msg = {"error": True, "errmsg": "Connect error"}
            return error_msg

    def get_data(self, query_str='',size=1000, fields='host,ip,title'):
        try:
            url = '{url}{api}'.format(url=self.base_url, api=self.search_api_url)
            query_str = bytes(query_str, 'utf-8')
            data = {'qbase64': base64.b64encode(query_str), 'email': self.email, 'key': self.key, 'size': size,
                    'fields': fields}
            req = requests.get(url, params=data, timeout=10)
            return req.json()
        except requests.exceptions.ConnectionError:
            error_msg = {"error": True, "errmsg": "Connect error"}
            return error_msg

if __name__ == '__main__':
    banner()
    ips=[]
    fofa = FofaAPI(email,key)
    try:
        result=fofa.get_data(cmd.get("query"),cmd.get("size"),"host,ip,title")
    except:
        logger.INFO("search error!!")
    for host,ip,title in result['results']:
        if cmd.get("cidr"):
            ips.append(ip2cidr(ip))
    
        logger.INFO("Host: {0} IP: {1} Title: [{2}]".format(host,ip,title)+"  is FOUND!")
        num=num+1
    if cmd.get("cidr"):
        cips=saveContext(ips)
        logger.INFO("C段为: {}".format(cips[1]))
        logger.INFO("一共查询出{}个C段 ".format(cips[0])+",保存为cidr.txt......")
    logger.INFO("一共导出{0}条数据，保存为{1}.........".format(num,cmd.get("report_name")))
    logger.INFO("保存中.....")
    df = pd.DataFrame(columns=['host', 'ip','title'], data=result['results'])
    df.to_csv("./{}".format(cmd.get("report_name")), encoding='utf-8', index=False)
    logger.INFO("保存完毕......")
