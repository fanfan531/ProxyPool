# -*- coding: utf-8 -*-
# @Time    : 2020-03-24 12:01
# @Author  : ken
'''

'''
import requests
import time


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


if __name__ == "__main__":
    sort_ip()
