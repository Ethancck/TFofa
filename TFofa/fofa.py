import requests
import base64
import pandas as pd
from core.banner import banner
from core.log import logger
from core.cmdline import args
from core.conf import email,key
from  core.colors import red
from core.lib import ip2cidr,saveContext,readFile
import json
logger=logger()
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

    def get_data(self, query_str,size=1000, fields='host,ip,title'):
        try:
            url = '{url}{api}'.format(url=self.base_url, api=self.search_api_url)
            query_str =query_str.encode(encoding="utf-8")
            base64_str=base64.b64encode(query_str)
            data = {'qbase64': base64_str, 'email': self.email, 'key': self.key, 'size': size,
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
    if args.cert:
        f = readFile(args.cert)
        domains = f.readlines()
        for domain in domains:
            domain = domain.strip()
            if args.status_code:
                query = 'cert="{}" && type="subdomain" && country="CN" && status_code="{}"'.format(domain,args.status_code)
            else:
                query='cert="{}" && type="subdomain" && country="CN"'.format(domain)
            logger.INFO(red+"Finding.....................................[{}]!".format(domain))
            try:
                result = fofa.get_data(query,args.size, "host,ip,title")
            except:
                logger.INFO("search error!!")
            try:
                for host, ip, title in result['results']:
                    if args.cidr:
                        ips.append(ip2cidr(ip))
                    logger.INFO("Host: {0} IP: {1} Title: [{2}]".format(host, ip, title) + "  is FOUND!")
                    num = num + 1

                if args.cidr:
                    cips = saveContext(ips, domain+"_cidr"+".csv")
                    logger.INFO("C段为: {}".format(cips[1]))
                    logger.INFO("一共查询出{}个C段 ".format(cips[0]) + ",保存为{}......".format(domain+"_cidr"+".csv"))
                logger.INFO("一共导出{0}条数据，保存为{1}........................".format(num,"{}_{}.csv".format(args.status_code,domain) ))
                logger.INFO("保存中.....")
                num=0
                df = pd.DataFrame(columns=['host', 'ip', 'title'], data=result['results'])
                df.to_csv("./{}".format("{}_{}.csv".format(args.status_code,domain)), encoding='utf-8', index=False)
                logger.INFO("保存完毕......")
            except:
                logger.INFO("search [{}] error!! please check your query words!!".format(domain))
    else:
        try:
            result=fofa.get_data(args.query,args.size,"host,ip,title")
        except:
            logger.INFO("search error!!")
        try:
            for host,ip,title in result['results']:
                if args.cidr:
                    ips.append(ip2cidr(ip))
                logger.INFO("Host: {0} IP: {1} Title: [{2}]".format(host,ip,title)+"  is FOUND!")
                num=num+1

            if args.cidr:
                cips=saveContext(ips,args.cidr)
                logger.INFO("C段为: {}".format(cips[1]))
                logger.INFO("一共查询出{}个C段 ".format(cips[0])+",保存为{}......".format(args.cidr))
            logger.INFO("一共导出{0}条数据，保存为{1}.........".format(num,args.report_name))
            logger.INFO("保存中.....")
            df = pd.DataFrame(columns=['host', 'ip','title'], data=result['results'])
            df.to_csv("./{}".format(args.report_name), encoding='utf-8', index=False)
            logger.INFO("保存完毕......")
        except:
            logger.INFO("search [{}] error!! please check your query words!!".format(args.query))
