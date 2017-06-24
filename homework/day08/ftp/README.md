## 模拟FTP实现上传下载功能  

1. 输入用户名(shuke,jack,john),密码123,账号信息保存在db/account.json文件中。
2. 上传: put D:\Learnpy\homework\ftp\README.md,上传完成后会进行md5值校验。
3. 下载: get data.json,下载完成后会进行md5值校验。
4. 断点续传下载: reget data.json 下载完成后会进行md5检验,目前只支持断点续传下载。
5. dir 查看用户家目录下的文件列表
6. exit 退出程序

* 目录结构
[root@shuke ftp]# tree -L 2
.
├── bin
│   ├── start_client.py		# 客户端程序启动文件
│   └── start_server.py		# 服务端程序启动文件
├── client
│   ├── Download		# 客户端下载文件存放路径
│   ├── ftpclient.py		# ftpclient端主程序
├── conf
│   └── settings.py
├── db
│   ├── accounts.json
├── home
│   ├── jack			# 账户家目录
│   └── shuke			# 账户家目录
├── __init__.py
├── README.md
└── server
    ├── account.py		# 账号处理脚本
    ├── ftpserver.py		# ftpserver端主程序


* 遗留问题  
1. 如何根据文件传输大小占文件总大小的百分比输出进度条信息
2. 断点续传上传功能未实现
3. 账户磁盘配额功能未实现

* Blog  
[python面向对象进阶](http://www.cnblogs.com/aslongas/p/7002799.html)
[python基础之socket编程](http://www.cnblogs.com/aslongas/p/7071324.html)
