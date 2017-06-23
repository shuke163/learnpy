## 模拟FTP实现上传下载功能  

1. 输入用户名(shuke,jack,john),密码123,账号信息保存在db/account.json文件中。
2. 上传: put D:\Learnpy\homework\ftp\README.md,上传完成后会进行md5值校验。
3. 下载: get data.json,下载完成后会进行md5值校验。
4. dir 查看用户家目录下的文件列表
5. exit 退出程序

* 遗留问题  
1. 如何根据文件传输大小占文件总大小的百分比输出进度条信息
2. 断点续传功能未完成

* Blog  
[python面向对象进阶](http://www.cnblogs.com/aslongas/p/7002799.html)
[python基础之socket编程](http://www.cnblogs.com/aslongas/p/7071324.html)
