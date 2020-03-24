# -*- coding: utf-8 -*-
# @Time    : 2020-03-24 11:43
# @Author  : ken
'''

'''
import time
import threading
import requests
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
from storage.RedisObject import RedisObject


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

    @classmethod
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

    def get_proxy(self):
        '''
        获取代理ip
        :return: dict
        '''
        name = 'proxypool'
        ip = self.conn.srandmember(name).decode('utf-8')
        if not ip: return 'ip池已空...'
        return eval(ip)


if __name__ == "__main__":
    Proxy.start()
