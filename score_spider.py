# Created by WuLei on February 1, 2018
# wuleiatso@gmail.com

import requests
import time
from lxml import etree

def getpage(user_code = 0):
    url = 'http://202.113.110.22:8088/tjsfjw/student/xscj.stuckcj_data.jsp'
    headers = {'Host':'202.113.110.22:8088',
                'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding':'gzip, deflate',
                'Referer':'http://202.113.110.22:8088/tjsfjw/student/xscj.stuckcj.jsp?menucode=JW130706',
                'Content-Type':'application/x-www-form-urlencoded',
                'Content-Length':'161',
                'Connection':'keep-alive',
                'Upgrade-Insecure-Requests':'1',
                'Pragma':'no-cache',
                'Cache-Control':'no-cache'}
    params = {'sjxz':'sjxz3','ysyx':'yscj','zx':1,'fx':1,'userCode':user_code,'xypjwchcnckcj':0,'pjwchckcjklpbcj':0,'xn':2017,'xn1':2018,'xq':0,'ysyxS':'on','sjxzS':'on','zxC':'on','fxC':'on','menucode_current':'JW1314'}
    try:
        content = requests.get(url, headers=headers, params = params, timeout = 2)
    except BaseException:
        return -1
    if content.status_code != 200:
        #print('usercode :', user_code, 'download failed!')
        return -1
    selector = etree.HTML(content.text)
    try:
        collage = selector.xpath("/html/body/div[3]/div[1]/text()")[0]
        classes = selector.xpath("/html/body/div[3]/div[2]/text()")[0]
        number = selector.xpath("/html/body/div[3]/div[3]/text()")[0]
        name = selector.xpath("/html/body/div[3]/div[4]/text()")[0]
    except BaseException:
        return -1
    collage = ''.join(list(collage)[7:])
    classes = ''.join(list(classes)[5:])
    number = ''.join(list(number)[3:])
    name = ''.join(list(name)[3:])
    #encoding_change =  selector.xpath("/html/head/meta[2]")
    #encoding_change.text = '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
    filepath = 'pages/' + number + '-' + name + '-' + collage + '-' + classes + '.html'
    fd = open(filepath, 'w+')
    t = content.text
    t_list = list(t)
    t_list[219:222] = ['U', 'T', 'F', '-', '8']
    fd.write(''.join(t_list))
    fd.close()
    return collage, classes, number, name

if __name__ == '__main__':
    fd = open('pages/log.txt', 'a+')
    for i in range(201734441, 201734442):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), i, 'downloading...')
        result = getpage(i)
        if result == -1:
            msg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '   ' + str(i) + ' failed'
            print(msg)
            fd.write(msg + '\n')
        else:
            msgs = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '   ' + str(i) + ' success' + ' '+result[0]+' ' + result[1]+' ' + result[2] +' '+ result[3]
            print(msgs)
            fd.write(msgs + '\n')
        time.sleep(0.3)
    fd.close()
