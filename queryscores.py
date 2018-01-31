# created by WuLei on January 31 2018
# wuleiatso@gmail.com

import jwlogin
import re
from lxml import etree

class query(object):
    def __init__(self, session, sessionid):
        self.session = session
        self.sessionid = sessionid

    def get_usercode(self):
        url = 'http://202.113.110.22:8088/tjsfjw/custom/js/SetRootPath.jsp'
        header = {'Accept':'*/*',
                    'Accept-Encoding':'gzip, deflate',
                    'Accept-Language':'zh-CN,zh;q=0.9',
                    'Connection':'keep-alive',
                    'Cookie':'JSESSIONID=' + self.sessionid,
                    'Host':'202.113.110.22:8088',
                    'Referer':'http://202.113.110.22:8088/tjsfjw/student/wsxk.pyfadb.html?menucode=JW130713',
                    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        r = self.session.get(url, headers = header)
        self.usercode = re.findall(r'G_USER_CODE = \'(.*?)\';', r.text)[0]
        print('user_code: ', self.usercode)
        print('user_name: ', re.findall(r'G_USER_NAME = \'(.*?)\';', r.text)[0])

    def loadinfo(self):
        url = 'http://202.113.110.22:8088/tjsfjw/student/xscj.stuckcj_data.jsp'
        params = {'sjxz':'sjxz3',
                    'ysyx':'yscj',
                    'zx':'1',
                    'fx':'1',
                    'userCode':str(self.usercode),
                    'xypjwchcnckcj':'0',
                    'pjwchckcjklpbcj':'0',
                    'xn':'2017',
                    'xn1':'2018',
                    'xq':'0',
                    'ysyxS':'on',
                    'sjxzS':'on',
                    'zxC':'on',
                    'fxC':'on',
                    'menucode_current':'JW1314'}
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        content = self.session.get(url, params = params, headers = headers)
        return content.text

    def parsescores(self, content = None):
        if content == None:
            print('query failed')
            exit(1)
        selector = etree.HTML(content)
        c = selector.xpath('/html/body/table[2]/tbody/tr')
        j=0
        for i in c:
            print(selector.xpath('/html/body/table[2]/tbody/tr[' + str(j+1) + ']/td[2]/text()')[0] +'   ' + selector.xpath('/html/body/table[2]/tbody/tr[' + str(j+1) + ']/td[8]/text()')[0])
            j = j + 1


    def holdconnection(self):
        url = 'http://202.113.110.22:8088/tjsfjw/online/message'
        params = {'hidOption':'getOnlineMessage'}
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        r = self.session.get(url, headers = headers, params = params)
        if r.status_code == 200:
            print('holding connection')

def go():
    s, sid = jwlogin.go()
    q = query(s, sid)
    q.holdconnection()
    q.get_usercode()
    q.holdconnection()
    q.parsescores(content=q.loadinfo())

if __name__ == '__main__':
    go()