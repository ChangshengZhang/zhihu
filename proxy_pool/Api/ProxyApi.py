# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyApi.py  
   Description :  
   Author :       JHao
   date：          2016/12/4
-------------------------------------------------
   Change Activity:
                   2016/12/4: 
-------------------------------------------------
"""
__author__ = 'JHao'

import sys
import json
from werkzeug.wrappers import Response
from flask import Flask, jsonify, request

sys.path.append('../')

from Util.GetConfig import GetConfig
from Manager.ProxyManager import ProxyManager

app = Flask(__name__)


class JsonResponse(Response):

    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (dict, list)):
            response = jsonify(response)

        return super(JsonResponse, cls).force_type(response, environ)

app.config['JSON_AS_ASCII'] = False
app.response_class = JsonResponse

api_list = {
    'get': u'get an usable proxy',
    # 'refresh': u'refresh proxy pool',
    'get_all': u'get all proxy from proxy pool',
    'delete?proxy=127.0.0.1:8080': u'delete an unable proxy',
    'get_status': u'proxy statistics'
}


@app.route('/')
def index():
    return api_list


@app.route('/get/')
def get():
    proxy = ProxyManager().get()
    return jsonify({'proxy':proxy})
    #return proxy if proxy else 'no proxy!'

@app.route('/refresh/')
def refresh():
    # TODO refresh会有守护程序定时执行，由api直接调用性能较差，暂不使用
    # ProxyManager().refresh()
    pass
    return 'success'


@app.route('/get_all/')
def getAll():
    proxies = ProxyManager().getAll()
    return jsonify(proxies)
    #return proxies


@app.route('/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    ProxyManager().delete(proxy)
    return 'success'


@app.route('/get_status/')
def getStatus():
    status = ProxyManager().getNumber()
    return status

@app.route('/validate_proxy/', methods=['GET'])
def validateProxy():
    proxy = request.args.get('proxy')
    validation_result = ProxyManager().validateProxy(proxy)
    return jsonify({'result':validation_result})
    #return json.dumps(validation_result, ensure_ascii = False)

@app.route('/refer_proxy/', methods=['GET'])
def referProxy():
    proxy = request.args.get('proxy')
    city = request.args.get('city')
    return jsonify({'proxy':ProxyManager().referProxy(proxy, city)})
    #return json.dumps(ProxyManager().referProxy(proxy,city), ensure_ascii = False)
    

def run():
    config = GetConfig()
    app.run(host=config.host_ip, port=config.host_port)


if __name__ == '__main__':
    run()
