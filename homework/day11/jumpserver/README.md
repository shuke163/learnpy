## 简单主机批量管理工具  
主机信息从mysql库中获取,采用线程池的方式并发执行任务,默认管理员账号为admin,可以修改表数据


* 目录结构  
[root@minion managetool]# tree -L 2  
.
|-- bin
|   |-- start.py                # 程序启动文件  
|-- conf  
|   |-- settings.py             # 程序配置参数文件  
|-- core  
|   |-- execcom.py              # 执行命令处理  
|   |-- login.py                # 登陆认证及显示用户信息  
|   |-- manage.py               # admin管理员操作表数据处理  
|-- db  
|   |-- jumpserver.sql          # 数据库初始化sql  
|-- logs  
|   |-- result.log              # log记录  
|-- README.md                   # 使用说明文件  


* 使用方法:  
账户分为两种:  
1. 普通账户,执行命令;  
2. 管理员账户，可以针对表数据进行增删改查操作;  
```
eg: batch_run -h web09,web07 -g web,db -cmd  "df -Th"
eg: (q|Q)
```

* 待优化项  
1. 部分命令不支持，需优化处理;  
2. 需增加文件上传下载功能;  
3. 完善日志记录功能;

* Blog  
[python操作MySql](http://www.cnblogs.com/aslongas/p/7146844.html)  


