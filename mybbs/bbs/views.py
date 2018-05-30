from django.shortcuts import render, HttpResponse
from utils.response import BaseResponse
from bbs import models
import requests
from bs4 import BeautifulSoup
import json
import os


def register(request):
    """
    注册
    :param request:
    :return:
    """
    pass


def login(request):
    """
    登陆
    :param request:
    :return:
    """
    pass


def index(request, *args, **kwargs):
    """
    首页
      - 显示所有的新闻类型
      - 显示所有的新闻列表
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    current_new_type_id = kwargs.get('new_type_id')
    if current_new_type_id:
        current_new_type_id = int(current_new_type_id)
    new_type_list = models.NewsType.objects.all()
    print(kwargs)

    news_list = models.News.objects.filter(**kwargs).values('id', 'title', 'url', 'avatar', 'summary',
                                                            'new_type_id__caption',
                                                            'ctime', 'like_count', 'comment_count')

    return render(request, "bbs/index.html",
                  {"new_type_list": new_type_list, 'current_new_type_id': current_new_type_id, 'news_list': news_list})


def upload(request):
    new_type_list = models.NewsType.objects.all()
    return render(request, 'bbs/upload.html', locals())


def upload_img(request):
    response = BaseResponse
    try:
        obj = request.FILES.get('fileupload')
        print(obj)
        img_path = os.path.join('static', 'img', obj.name)
        with open(img_path, mode='wb') as f:
            for chunk in obj.chunks():
                f.write(chunk)
    except Exception as e:
        print("Error: ", e)
        response.msg = str(e)
    else:
        response.status = True
        response.data = img_path
    return HttpResponse(json.dumps(response.__dict__))


def get_title_summary(request):
    """解析url爬取新闻"""
    url = request.POST.get('url')

    response = requests.get('http://music.163.com/#/song?id=188057')
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text
    desc = soup.find('meta', attrs={'name': 'description'}).get('content')
    data = {'title': title, 'desc': desc}
    return HttpResponse(json.dumps(data))


def build_comment_data(comment_li):
    """
    处理查询的评论数据
    :param comment_li:
    :return:
    """
    dic = {}
    for item in comment_li:
        item['children'] = []
        dic[item['id']] = item

    result = []
    for item in comment_li:
        pid = item['parent_id']
        if pid:
            dic[pid]['children'].append(item)
        else:
            result.append(item)
    print(result)
    return result


def comment_list(request):
    """
    评论信息
    :param request:
    :return:
    """
    response = BaseResponse()
    try:
        newId = request.GET.get('newId')
        comment_li = models.News2Comment.objects.filter(new_id=newId).values('id', 'new_id', 'user__username',
                                                                             'content', 'parent_id')
        print(comment_li)
        comm_li = build_comment_data(list(comment_li))
        response.status = True
        response.data = comm_li
    except Exception as e:
        print("ERROR: ", e)
    else:
        return HttpResponse(json.dumps(response.__dict__))
