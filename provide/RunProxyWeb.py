# -*- coding: utf-8 -*-
# @Time    : 2020-03-24 11:40
# @Author  : ken
'''

'''
from fastapi import FastAPI
from reptile.Proxy import Proxy
from config import flask_debug, flask_host, flask_threaded, flast_port

app = FastAPI()
p = Proxy()


@app.get("/")
def get_ip():
    return p.get_proxy()


if __name__ == "__main__":
    app.run(host=flask_host, port=flast_port, debug=flask_debug, threaded=flask_threaded)
