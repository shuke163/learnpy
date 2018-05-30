from django.conf.urls import url
from bbs import  views

urlpatterns = [
    url(r'^newtype/(?P<new_type_id>\d+)/', views.index, name="newtype"),
    url(r'^$', views.index, name="index"),
    url(r'^upload/$', views.upload, name="upload"),
    url(r'^upload_img/$', views.upload_img, name="upload_img"),
    url(r'^comment_list/$', views.comment_list, name="comment_list")
]
