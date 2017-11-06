from django.shortcuts import render, HttpResponse, redirect
import requests
from bs4 import BeautifulSoup
import re
import time
import json


def login(req):
    """
    login view
    :param req:
    :return:
    """
    current_time = int(time.time() * 1000)
    if req.method == "GET":
        base_qcode_url = "https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_={0}"
        qcode_url = base_qcode_url.format(current_time)
        response = requests.get(qcode_url)
        uuid = re.findall('window.QRLogin.uuid = "(.*)";', response.text)[0]
        print(response.text, uuid)
        req.session['UUID'] = uuid
        return render(req, 'login.html', {'uuid': uuid})


def check_login(req):
    print("*" * 100)
    # https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=4b7s39SgHg==&tip=1&r=-805658091&_=1508339178397
    if req.method == "GET":
        response = {'code': 408, 'data': None}
        ctime = int(time.time() * 1000)
        base_login_url = 'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip=0&r=-806232477&_={1}'
        login_url = base_login_url.format(req.session['UUID'], ctime)
        ret = requests.get(login_url)
        if 'window.code=408' in ret.text:
            response['code'] = 408
        elif 'window.code=201' in ret.text:
            response['code'] = 201
            user_avatar = re.findall("window.userAvatar = '(.*)';", ret.text)[0]
            response['data'] = user_avatar
        elif 'window.code=200' in ret.text:
            req.session['LOGIN_COOKIE'] = ret.cookies.get_dict()
            base_redirect_url = re.findall('window.redirect_uri="(.*)";', ret.text)[0]
            redirect_url = base_redirect_url + '&fun=new&version=v2'
            r1 = requests.get(redirect_url)
            soup = BeautifulSoup(r1.text, 'html.parser')
            result = {}
            for tag in soup.find(name='error').find_all():
                result[tag.name] = tag.text
            req.session['TICKET_DICT'] = result
            req.session['TICKET_COOKIE'] = r1.cookies.get_dict()

            # 初始化
            print(result)
            """https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-980737284&pass_ticket=NvFTskmGufqAeOePf%252BnuAKQKHlAQ1Yg62WfxQpRU8nH5MMMvgztOME8UAlpVMIID"""
            init_url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-1019705917&lang=zh_CN&pass_ticket={0}".format(
                result['pass_ticket'])
            post_data = {
                'BaseRequest': {
                    'DeviceID': "e200822626698201",
                    'Sid': result['wxsid'],
                    'Skey': result['skey'],
                    'Uin': result['wxuin'],
                }
            }
            r3 = requests.post(url=init_url, json=post_data)
            r3.encoding = 'utf-8'

            init_dict = json.loads(r3.text)
            req.session['INIT_DICT'] = init_dict
            for k, v in init_dict['User'].items():
                print(k, v)
            response['code'] = 200
        return HttpResponse(json.dumps(response))


def index(req):
    avatar = req.session['INIT_DICT']['User']['HeadImgUrl']
    img_url = "Https://wx.qq.com" + avatar
    res = requests.get(img_url, headers={'Referer': 'https://wx.qq.com/?&lang=zh_CN'})
    print(res.url, res.content)

    return render(req, 'index.html', {'img': res.content})
