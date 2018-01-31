# created by WuLei on January 31 2018
# wuleiatso@gmail.com

import hashlib
import base64
import requests
import re
import json
from lxml import etree
from urllib import request
import tkinter as tk
from PIL import Image, ImageTk


class login(object):
    def __init__(self):
        print("username:")
        self.username = input()
        print("password:")
        self.password = input()

    def getsessionid(self):
        self.session = requests.session()
        r = self.session.get('http://202.113.110.22:8088/tjsfjw/cas/login.action')
        print('loading...')
        selector = etree.HTML(r.text)
        content = selector.xpath('/html/head/script[2]/text()')
        #self.sessionid = re.match(r'_sessionid = "(.*?)";', ''.join(content))
        self.sessionid = re.findall(r'_sessionid = "(.*?)";', ''.join(content))[0]
        #self.cookie = {'JSESSIONID':self.sessionid}
        print('sessionid: ',self.sessionid)

    def getverificationcode(self):
        url = 'http://202.113.110.22:8088/tjsfjw/cas/genValidateCode'
        #self.session.urlretrieve(url, 'verificationcode.jpg')
        ir = self.session.get(url)
        if ir.status_code == 200:
            open('verificationcode.jpg', 'wb').write(ir.content)

    def inputverifcode(self):
        root = tk.Tk()
        im = Image.open('verificationcode.jpg')
        tkimg = ImageTk.PhotoImage(im)
        label = tk.Label(root, image = tkimg).pack()
        root.mainloop()
        print('input verification code:')
        self.verifcode = input()

    def password_encode(self):
        a = hashlib.md5()
        a.update(self.password.encode('utf-8'))
        b = hashlib.md5()
        b.update(self.verifcode.encode('utf-8'))
        c = hashlib.md5()
        c.update(a.hexdigest().encode('utf-8'))
        c.update(b.hexdigest().encode('utf-8'))
        self.password = c.hexdigest()
        print('md5 encoded password: ', self.password)

    def username_encode(self):
        self.username = base64.b64encode(self.username.encode('utf-8') + b';;' + self.sessionid.encode('utf-8'))
        print('base64 encoded username: ', self.username)

    def login(self):
        un = '_u' + self.verifcode
        pw = '_p' + self.verifcode
        params = {un:self.username, pw:self.password, 'randnumber': self.verifcode, 'isPasswordPolicy':1}
        headers = {'Accept':'text/plain, */*; q=0.01',
                    'Accept-Encoding':'gzip, deflate',
                    'Accept-Language':'zh-CN,zh;q=0.9',
                    'Connection':'keep-alive',
                    'Content-Length':'142',
                    'Content-Type':'application/x-www-form-urlencoded',
                    'Cookie':'JSESSIONID='+self.sessionid,
                    'Host':'202.113.110.22:8088',
                    'Origin':'http://202.113.110.22:8088',
                    'Referer':'http://202.113.110.22:8088/tjsfjw/cas/login.action',
                    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                    'X-Requested-With':'XMLHttpRequest'}
        response = self.session.get('http://202.113.110.22:8088/tjsfjw/cas/logon.action', params = params, headers = headers)
        #print(response.text)
        result = json.loads(response.text)
        if result['status'] == '401':
            print('verification code error')
        elif result['status'] == '402':
            print('username or password error')
        elif result['status'] == '200':
            print('log in sussess')

def go():
    l = login()
    l.getsessionid()
    l.getverificationcode()
    l.inputverifcode()
    l.password_encode()
    l.username_encode()
    l.login()

if __name__ == '__main__':
    go()