# tjsfjwlogin
Python模拟登录师大教务系统

jwlogin.py---登录模块  
queryscores.py---查询成绩  

### 教务系统登录接口加密规则
用户名采用base64加密，规则为：base64(username + ';;' + sessionid)   
username为学号，sessionid为会话id  
密码采用两重md5加密，规则为：md5(md5(password) + md5(verificationcode))  
password为密码，verificationcode为验证码  

### 怎么使用
1.复制两个脚本到本地或clone该仓库到本地  
2.使用pip安装必要的模块，如requests,lxml,pillow,tkinter  
3.使用命令`python3 queryscores.py`执行  
