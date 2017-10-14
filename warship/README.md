# wariship 项目

1. 登陆： http://127.0.0.1:8080/login/  
   username:shuke   passwd:123  

2. 已实现功能  
    a. 增加  
    b. 删除  
    c. 自定义分页  
    d. 查看业务线下面所有的主机  
    e. 注销  
    f. agent上报主机信息进行注册
    
3. agent主机注册接口(method=POST)  
 [注册地址](http://127.0.0.1:9000/host/asset/)


4. 遗留问题  
   a. 编辑操作时候ajax中{% url 'edithost' %}语法使用问题  
