# -*- coding: utf-8 -*-
# @Time    : 2019-09-25 16:40
# @Author  : ken
'''
构建自己的代理池
1.扩充代理源.
2.所有参数写死,不依赖外部脚本参数.
'''
import time
import threading
import requests
from bs4 import BeautifulSoup
from basic.utils.config import *
from fastapi import FastAPI
from robobrowser import RoboBrowser


class RedisObject:
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance

    def get_connection(self):
        '''获取redis连接'''
        redis_host, redis_pass, redis_port, redis_db = '192.168.1.233', 'yMxsueZD9yx0AkfR', '6543', '3'
        pool = redis.ConnectionPool(host=redis_host, password=redis_pass, port=redis_port, db=redis_db, socket_timeout=5, max_connections=469)
        conn = redis.StrictRedis(connection_pool=pool, decode_responses=True)
        return conn


class Proxy:
    '''
    爬取各大ip代理网站的免费ip地址,
    '''

    def __init__(self):
        self.conn = RedisObject().get_connection()

    def quanwang_dai_li(self):
        '''
        爬取免费ip
        :数据源:全网代理IP
        :return:
        '''
        url = 'http://www.goubanjia.com/'
        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        }

        result = self.request_proxy('GET', url, headers=headers)
        soup = BeautifulSoup(result.text, 'html.parser')
        ips = soup.find_all('td', class_='ip')
        for ip in ips:
            self._format_ip({'http': f'http://{ip.get_text()}'})

    def xici_daili(self):
        '''
        爬取免费ip
        :数据源:西刺免费代理IP
        :return:
        '''
        url = 'https://www.xicidaili.com/wt/'
        headers = {
            'Accept': "application/json, text/plain, */*",
            'Origin': "https://www.feixiaohao.com",
            'Host': 'www.xicidaili.com',
            'Connection': 'close',
            'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTg2ZDE5YTVlNjVlZWQxY2VjYjIwMTAxMmI3M2ZiOWUyBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMXB3akxTTUk1TUlkaUxLWFhKQjQvV2kzT2ZlY3JDYjVKdmRkdUFKVFJ6bDg9BjsARg%3D%3D--3bdabaa014c4a7cc1539ef4efe232d9be38c7660; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1568950864,1569400872,1569403860; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1579403894',
            'Sec-Fetch-Mode': "cors",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        }
        result = self.request_proxy('GET', url, headers=headers)
        soup = BeautifulSoup(result.text, 'html.parser')
        ips = soup.find_all('tr', class_='odd')
        for ip in ips:
            td = ip.find_all('td')
            host = td[1].get_text()
            port = td[2].get_text()
            self._format_ip({'http': f'http://{host}:{port}'})

    def xila_daili(self):
        '''
        爬取免费ip
        :数据源:西拉免费代理IP
        :return:
        '''
        url = 'http://www.xiladaili.com/http/2/'
        headers = {
            'Connection': 'close',
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        }
        result = self.request_proxy('GET', url, headers=headers)
        soup = BeautifulSoup(result.text, 'html.parser')
        ips = soup.find('table', class_='fl-table').find('tbody').find_all('tr')
        for ip in ips:
            td = ip.find_all('td')
            host_port = td[0].get_text()
            # port = td[2].get_text()
            self._format_ip({'http': f'http://{host_port}'})

    def kuai_dai_li(self):
        '''
        快代理
        :return:数据需要使用无头爬取
        '''
        url = 'https://www.kuaidaili.com/free/intr/'
        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_ ≥14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            'Connection': 'close'
        }

        result = self.request_proxy('GET', url, headers=headers)
        soup = BeautifulSoup(result.text, 'html.parser')
        ips = soup.find('table', class_='layui-table').find('tbody').find('tr')
        for ip in ips:
            td = ip.find_all('td')
            host = td[0].get_text().lower()
            port = td[1].get_text().strip()
            self._format_ip({'http': f'http://{host}:{port}'})

        browser = RoboBrowser()
        browser.open(url)
        time.sleep(3)
        table = browser.select('table.table table-bordered table-striped')
        print(table)

    def bajiu_daili(self):
        '''
        89免费代理
        :return:
        '''
        url = 'http://www.89ip.cn/'
        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            'Connection': 'close'
        }
        result = self.request_proxy('GET', url, headers=headers)
        # print(result.text)
        soup = BeautifulSoup(result.text, 'html.parser')
        ips = soup.find('table', class_='layui-table').find('tbody').find_all('tr')
        for ip in ips:
            td = ip.find_all('td')
            host = td[0].get_text().strip()
            port = td[1].get_text().strip()
            self._format_ip({'http': f'http://{host}:{port}'})

    def start(self):
        while 1:
            self.quanwang_dai_li()
            self.xici_daili()
            self.xila_daili()
            time.sleep(60)

    def _format_ip(self, ip):
        '''
        效验ip地址是否成功
        :param ips: [{'http':'http://111.222.33.1234:8080'},...]
        :return:
        '''
        result = self.conn.sadd('proxypool', str(ip))
        if result == 1:
            print(f'{ip} 成功')
        if result == 0:
            print(f'{ip} 已存在集合.')
        if result != 0 and result != 1:
            print(result)

    def request_proxy(self, method, url, headers=None):
        '''

        :return:
        '''
        name = 'proxypool'
        ip = self.conn.srandmember(name)
        if ip:
            try:
                ip = eval(ip.decode('utf-8'))
                data = requests.request(method, url, proxies=ip, headers=headers, timeout=10)
                print(f'此次请求使用代理: {ip}')
                return data
            except BaseException as e:
                print(e)
                data = requests.request(method, url, headers=headers, timeout=10)
                print(f'此次请求使用代理: None')
                return data
        else:
            data = requests.request(method, url, headers=headers, timeout=10)
            print(f'此次请求使用代理: None')
            return data

    def sort_ip(self):
        '''清理失效ip;单独开启一个线程'''
        name = 'proxypool'
        while 1:
            ips = self.conn.smembers(name)  # 返回集合
            for ip in ips:
                try:
                    ip = ip.decode('utf-8')
                    url = 'https://www.kuaidaili.com/'
                    headers = {
                        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
                        'Connection': 'close'
                    }
                    data = requests.get(url, proxies=eval(ip), headers=headers, timeout=15)
                    print(data.status_code, ip)
                    if data.status_code == 200: continue
                    self.conn.srem(name, ip)
                    print(f'删除无效ip: {ip}')
                except:
                    self.conn.srem(name, ip)
                    print(f'删除无效ip: {ip}')
            print(f'休息5s..')
            time.sleep(5)

    def get_proxy(self):
        '''
        获取代理ip
        :return: dict
        '''
        name = 'proxypool'
        ip = self.conn.srandmember(name).decode('utf-8')
        if not ip: return 'ip池已空...'
        return eval(ip)


app = FastAPI()

p = Proxy()


@app.get("/")
def get_ip():
    return p.get_proxy()


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == '__main__':
    '''爬取代理'''
    # t2 = threading.Thread(target=Proxy().start())
    # t2.start()
    '''效验代理'''
    t1 = threading.Thread(target=Proxy().sort_ip)
    t1.start()
