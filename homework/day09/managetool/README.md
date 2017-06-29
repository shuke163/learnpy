## 简单主机批量管理工具  


* 目录结构  
[root@minion managetool]# tree -L 2  
.  
├── bin  
│   └── start.py			# 程序启动文件  
├── command				# 核心代码目录  
│   ├── execcom.py			# 执行命令处理  
│   ├── readconf.py			# 处理hosts文件  
│   └── scpfile.py			# 处理上传下载文件  
├── conf  
│   ├── host.ini			# hosts文件  
│   └── settings.py			# 程序配置参数文件  
├── db  
│   └── __init__.py  
├── logs  
│   ├── __init__.py  
├── __init__.py  
└── README.md				# 说明文件  

* 使用方法:  
```
eg: batch_run -h h1,h2,h3 -g web,db -cmd  "df -Th"
eg: batch_scp -h h1,h2,h3 -g web,db -action put -local /data/study/pid.py -remote /tmp
eg: batch_scp -h h1,h2,h3 -g web,db -action get -local /data/study/pid.py -remote /tmp
eg: (q|Q)
```

* 待优化项  
1. 上传下载文件时远程路径为目录,需优化为完整路径;  
2. 部分命令不支持，需优化处理;  
3. 增加账号认证功能;  
4. 增加log记录操作日志功能;  

* Blog  
[python基础之进程与线程](http://www.cnblogs.com/aslongas/p/7078565.html)  


