#!/usr/bin/python2
# -*- coding:utf-8 -*-
"""
一个简单的Python爬虫, 用于抓取coursera网站的下载链接

Anthor: Andrew Liu
Version: 0.0.1
Date: 2014-12-04
Language: Python2.7.8
Editor: Sublime Text2
Operate: 具体操作请看README.md介绍
"""

import sys
import string
import re, random
import urllib, urllib2
import cookielib
import getpass


class Coursera(object) :
    """Coursera类定义
    
    实现模拟登陆,抓取网页代码和正则匹配, 保存连接到文件

    Attributes:
        login_url: 保存真正的登陆页面url
        url: 保存用于爬取下载连接的url
        user_name: 存储用户登陆Email
        password: 存储用户登陆密码
    """

    def __init__(self, url, user_name, password) :
        """
        初始化构造函数

        Args:
            url: 存储抓取页面的url
            user_name: 存储用户登陆Email
            password: 存储用户登陆密码

        Raises:
            UserOrPwdNone: 当用户名或者密码为空时,引起异常
        """
        self.login_url = "https://accounts.coursera.org/api/v1/login"
        self.url = url
        if user_name == "" or password == "" :
            raise UserOrPwdNone("the username or password can't empty string")
            sys.exit(2)
        else :
            self.user_name = user_name
            self.password = password

    def simulation_login(self) :
        """
        模拟登陆函数
        """
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        urllib2.install_opener(opener)
        form_data, request_header = self.structure_headers()
        req = urllib2.Request(self.login_url, data = form_data, headers = request_header)
        try :
            result = urllib2.urlopen(req)
        except urllib2.URLError,e :
            if hasattr(e, "code"):
                print "The server couldn't fulfill the request.Please check your url and read the Reason"
                print "Error code: %s" % e.code
            elif hasattr(e, "reason"):
                print "We failed to reach a server. Please check your url and read the Reason"
                print "Reason: %s" % e.reason
            sys.exit(2)
        if result.getcode() == 200 :
            print "登陆成功..."

    def structure_headers(self) :
        """
        头部构造函数

        Return:
            form_data: 返回表单数据
            request_header: 返回伪装头部
        """
        #模拟表单数据,这个参数不是字典
        form_data = urllib.urlencode({
            "email": self.user_name,
            "password": self.password,
            "webrequest": "true"
        })  
        user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/38.0.2125.111 Safari/537.36")
        XCSRF2Cookie = 'csrf2_token_%s' % ''.join(self.random_string(8))
        XCSRF2Token = ''.join(self.random_string(24))
        XCSRFToken = ''.join(self.random_string(24))
        cookie = "csrftoken=%s; %s=%s" % (XCSRFToken, XCSRF2Cookie, XCSRF2Token)

        request_header = {
            "Referer": "https://accounts.coursera.org/signin",  #对付防盗链设置, 为跳转来源的url
            "User-Agent": user_agent, #伪装成浏览器访问
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRF2-Cookie": XCSRF2Cookie,
            "X-CSRF2-Token": XCSRF2Token,
            "X-CSRFToken": XCSRFToken,
            "Cookie": cookie
        }
        return form_data, request_header

    def random_string(self, length):
        """
        随机生成指定长度的字母和数字序列
        """
        return ''.join(random.choice(string.letters + string.digits) for i in xrange(length))

    def get_links(self) :
        """
        爬取页面代码,获取下载MP4和pdf连接

        Return:
            down_links: 返回MP4下载链接list
            down_pdfs: 返回PDF下载链接list
        """
        try :
            result = urllib2.urlopen(self.url)
        except urllib2.URLError,e :
            if hasattr(e, "code"):
                print "The server couldn't fulfill the request."
                print "Error code: %s" % e.code
            elif hasattr(e, "reason"):
                print "We failed to reach a server. Please check your url and read the Reason"
                print "Reason: %s" % e.reason
            sys.exit(2)
        content = result.read().decode("utf-8")
        # with open("page.html", "w") as my_file :
        #     my_file.write(content)
        print "读取网页成功..."
        #content = content.decode("utf-8")
        down_links = re.findall(r'<a.*?href="(.*?mp4.*?)"', content)
        down_pdfs = re.findall(r'<a.*?href="(.*?pdf)"', content)
        print "正则匹配结束..."
        return down_links, down_pdfs

    def start_spider(self) :
        """
        运行爬虫,将爬取链接分别写入不同文件
        """
        self.simulation_login()
        down_links, down_pdfs = self.get_links()
        with open("coursera.html", "w+") as my_file :
            print "下载链接的长度", len(down_links)
            for link in down_links :
                print link
                try :
                    my_file.write(link + "\n")
                except UnicodeEncodeError:
                    sys.exit(2)
        with open("coursera.pdf", "w+") as my_file :
            print "下载pdf的长度", len(down_pdfs)
            for pdf in down_pdfs :
                try :
                    my_file.write(pdf + "\n")
                except UnicodeEncodeError :
                    sys.exit(2)
        print "抓取Coursera课程下载链接和pdf链接成功"

class UserOrPwdNone(BaseException):
    """
    Raised if the username or password is empty string
    """

def main() :
    if len(sys.argv) != 2 :
        print "Please Input what course you want to download.."
        sys.exit(2)
    url = "https://class.coursera.org/{course}/lecture"

    user_name = raw_input("Input your Email > ")
    password = getpass.getpass("Input your Password > ")
    spider = Coursera(url.format(course = sys.argv[1]), user_name, password)
    spider.start_spider()

if __name__ == '__main__':
    main()




