## 作业
1. information.py
    帮助:
        该程序目前只完成部分功能，后期需要进行优化处理...
        1.查询语言实例:
            a.删除仅支持根据id判断('>','<','=','<=','>=')以及limit关键字
            select * from db.emp limit 10
            select * from db.emp where id >= 20
            select id,name,age from db.emp where id < 15
        2.插入数据实例:
            insert into db.emp values Bigbang,22,17233786749,ops,2012-01-10
        3.更新实例:
            update db.emp set dept=Market where dept = IT(未完成)
        4.删除实例:
            a.删除仅支持根据id判断('>','<','=')以及like关键字
            delect from db.emp where id > 30
            delect from db.emp where id = 30
            delect from db.emp where name like 娟
2. 存在问题
      1.编程思想
      2.函数在定义的时候，究竟该传几个参数比较合适
      3.如何将功能模块拆分成函数的形式来实现
      4. update功能未完成
      5. 有重复代码,还可以提炼优化

3. Blog地址
* http://www.cnblogs.com/aslongas/p/6785698.html
* http://www.cnblogs.com/aslongas/p/6856301.html

作业可参考: http://www.echojb.com/perl-python/2017/05/16/387937.html
