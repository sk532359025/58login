#-*- encoding:utf8 -*-
import requests
import time
import random
import math
import re
import json
import execjs

ret = random.random()
ret = math.floor(ret*1e3)
timestamp = int(time.time()*1000)


class Spider:
    Session = {}
    token = ''
    rsaExponent = ''
    rsaModulus = ''
    password = ''
    username = ''
    def getLogin(self):
        loginHeader = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'passport.58.com',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
        }
        Response = self.Session.get(url="https://passport.58.com/login",headers=loginHeader, verify=False)
        print(Response)

    #获取token
    def init(self):
        # 验证-------------
        params = {
            'path':'http://my.58.com/?pts=%d' % (timestamp),
            'source': '58-default-pc',
            'psdk-d': 'jsdk',
            'psdk-v': '1.0.3',
            'callback': str(timestamp+ret)
        }
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'passport.58.com',
            'Pragma': 'no-cache',
            'Referer': 'https://passport.58.com/login',
            'Sec-Fetch-Dest': 'script',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
        }
        Response = self.Session.get(url="https://passport.58.com/58/login/init", params=params, headers=headers, verify=False)
        responseStr = Response.text
        findRes = re.findall('({.*})', responseStr)[0]
        if (len(findRes) == 0):
            print('init error')
            exit()
        jsonRes = json.loads(findRes)
        self.token = jsonRes['data']['token']
        print('Init Token:', self.token)
    #获取rsa
    def rsa(self):
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'passport.58.com',
            'Pragma': 'no-cache',
            'Referer': 'https://passport.58.com/login',
            'Sec-Fetch-Dest': 'script',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
        }

        params = {
            'source': '58-default-pc',
            'psdk-d': 'jsdk',
            'psdk-v': '1.0.3',
            'callback': 'JsonpCallBack'+str(timestamp+ret)
        }
        Response = self.Session.get(url="https://passport.58.com/58/rsa", params=params, headers=headers, verify=False)
        responseStr = Response.text
        findRes = re.findall('({.*})', responseStr)[0]
        if (len(findRes) == 0):
            print('rsa error')
            exit()
        jsonRes = json.loads(findRes)
        self.rsaExponent = jsonRes['data']['rsaExponent']
        self.rsaModulus = jsonRes['data']['rsaModulus']

        print('rsa rsaExponent',self.rsaExponent)
        print('rsa rsaModulus',self.rsaModulus)
    #password加密
    def encryptString(self):

        with open('./58test.js',mode="r", encoding="utf8") as f:
            jsScript = f.read()
        ctx = execjs.compile(jsScript)
        result = ctx.call('encrypt',self.password, self.rsaExponent, self.rsaModulus)
        print('encrypt', result)
        return result
    
    def btData(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length':'267',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host': 'cdata.58.com',
            'Origin': 'https://passport.58.com',
            'Referer': 'https://passport.58.com/login',
            'Sec-Fetch-Dest': 'iframe',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
        }
        postdata = {
            'xxzltr':'1$$dX9wW15mEC5cwF33tRFD9g==|-1$$-1$$https://passport.58.com/login$$%d$$3$$-1$$%d,529,524$$btn_account,%d,281,433$$password,%d$$-1$$14,14' % (timestamp, timestamp+101, timestamp+240, timestamp+105),
        }
        Response = self.Session.post(url="https://cdata.58.com/btData", headers=headers, data=postdata, verify=False)
        print('btData:', Response.text)
    
    def dologin(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host': 'passport.58.com',
            'Origin': 'https://passport.58.com',
            'Referer': 'https://passport.58.com/login',
            'Sec-Fetch-Dest': 'iframe',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
        }
        postdata = {
            'username': self.username,
            'password': self.password,
            'token': self.token,
            'source': '58-default-pc',
            'path': 'http://my.58.com/?pts=%d' % (timestamp),
            'domain': '58.com',
            'finger2': 'zh-CN|24|1|6|1920_1080|1920_1040|-480|1|1|1|undefined|1|unknown|Win32|unknown|3|false|false|false|false|false|0_false_false|d41d8cd98f00b204e9800998ecf8427e|f377b67b8c23303f805ef733d2c27fe6',
            'psdk-d': 'jsdk',
            'psdk-v': '1.0.3',
            'fingerprint': '37FY60tpRetEg2ym5sr6RTeJbCkRiOkB',
            'callback': 'SDK_CALLBACK_FUN.successFun',
        }
        Response = self.Session.post(url="https://passport.58.com/58/login/pc/dologin", headers=headers, data=postdata, verify=False)
        print('btData:', Response.text)
    #run
    def run(self):
        self.username = 'phone'
        self.password = '123456'
        self.Session = requests.session()
        self.getLogin()
        self.init()
        self.rsa()
        #加密后的password
        self.password = self.encryptString()
        self.btData()
        self.dologin()





Spider = Spider()
Spider.run()

"""
    def beData(self):
        pass
        #btdata
        # postdata = {
        #     'xxzltr': '1$$dX9wW15mEC5cwF33tRFD9g==|-1$$-1$$https://passport.58.com/login$$%d$$3$$-1$$%d,408,252$$btn_account,%d,209,409$$password,%d$$-1$$6,6' % (timestamp, timestamp+3, timestamp+6, timestamp+3),
        #     'source': '',
        # }
        # loginHeader['Origin'] = 'https://passport.58.com'
        # loginHeader['Host'] = 'cdata.58.com'
        # loginHeader['Referer'] = 'https://passport.58.com/login'

        # Response = Session.post(url="https://cdata.58.com/btData", data=postdata, headers=loginHeader, verify=False)
        # print('btData', Response.text)

"""
