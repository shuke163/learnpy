# _*_coding:utf-8_*_
 # Author:Jaye He
 import re
 import os
 
 
 def sql_parse(sql, key_lis):
     '''
     解析sql命令字符串,按照key_lis列表里的元素分割sql得到字典形式的命令sql_dic
     :param sql:
     :param key_lis:
     :return:
     '''
     sql_list = []
     sql_dic = {}
     for i in key_lis:
         b = [j.strip() for j in sql.split(i)]
         if len(b) > 1:
             if len(sql.split('limit')) > 1:
                 sql_dic['limit'] = sql.split('limit')[-1]
             if i == 'where' or i == 'values':
                 sql_dic[i] = b[-1]
             if sql_list:
                 sql_dic[sql_list[-1]] = b[0]
             sql_list.append(i)
             sql = b[-1]
         else:
             sql = b[0]
         if sql_dic.get('select'):
             if not sql_dic.get('from') and not sql_dic.get('where'):
                 sql_dic['from'] = b[-1]
     if sql_dic.get('select'):
         sql_dic['select'] = sql_dic.get('select').split(',')
     if sql_dic.get('where'):
         sql_dic['where'] = where_parse(sql_dic.get('where'))
     return sql_dic
 
 
 def where_parse(where):
     '''
     格式化where字符串为列表where_list,用'and', 'or', 'not'分割字符串
     :param where:
     :return:
     '''
     casual_l = [where]
     logic_key = ['and', 'or', 'not']
     for j in logic_key:
         for i in casual_l:
             if i not in logic_key:
                 if len(i.split(j)) > 1:
                     ele = i.split(j)
                     index = casual_l.index(i)
                     casual_l.pop(index)
                     casual_l.insert(index, ele[0])
                     casual_l.insert(index+1, j)
                     casual_l.insert(index+2, ele[1])
                     casual_l = [k for k in casual_l if k]
     where_list = three_parse(casual_l, logic_key)
     return where_list
 
 
 def three_parse(casual_l, logic_key):
     '''
     处理临时列表casual_l中具体的条件,'staff_id>5'-->['staff_id','>','5']
     :param casual_l:
     :param logic_key:
     :return:
     '''
     where_list = []
     for i in casual_l:
         if i not in logic_key:
             b = i.split('like')
             if len(b) > 1:
                 b.insert(1, 'like')
                 where_list.append(b)
             else:
                 key = ['<', '=', '>']
                 new_lis = []
                 opt = ''
                 lis = [j for j in re.split('([=<>])', i) if j]
                 for k in lis:
                     if k in key:
                         opt += k
                     else:
                         new_lis.append(k)
                 new_lis.insert(1, opt)
                 where_list.append(new_lis)
         else:
             where_list.append(i)
     return where_list
 
 
 def sql_action(sql_dic, title):
     '''
     把解析好的sql_dic分发给相应函数执行处理
     :param sql_dic:
     :param title:
     :return:
     '''
     key = {'select': select,
            'insert': insert,
            'delete': delete,
            'update': update}
     res = []
     for i in sql_dic:
         if i in key:
             res = key[i](sql_dic, title)
     return res
 
 
 def select(sql_dic, title):
     '''
     处理select语句命令
     :param sql_dic:
     :param title:
     :return:
     '''
     with open('staff_data', 'r', encoding='utf-8') as fh:
         filter_res = where_action(fh, sql_dic.get('where'), title)
         limit_res = limit_action(filter_res, sql_dic.get('limit'))
         search_res = search_action(limit_res, sql_dic.get('select'), title)
     return search_res
 
 
 def insert(sql_dic, title):
     '''
     处理insert语句命令
     :param sql_dic:
     :param title:
     :return:
     '''
     with open('staff_data', 'r+', encoding='utf-8') as f:
         data = f.readlines()
         phone_list = [i.strip().split(',')[4] for i in data]
         ins_count = 0
         if not data:
             new_id = 1
         else:
             last = data[-1]
             last_id = int(last.split(',')[0])
             new_id = last_id+1
         record = sql_dic.get('values').split('/')
         for i in record:
             if i.split(',')[3] in phone_list:
                 print('33[1;31m%s 手机号已存在33[0m' % i)
             else:
                 new_record = '%s,%sn' % (str(new_id), i)
                 f.write(new_record)
                 new_id += 1
                 ins_count += 1
         f.flush()
     return ['insert successful'], [str(ins_count)]
 
 
 def delete(sql_dic, title):
     '''
     处理delete语句命令
     :param sql_dic:
     :param title:
     :return:
     '''
     with open('staff_data', 'r', encoding='utf-8') as r_file,
             open('staff_data_bak', 'w', encoding='utf-8') as w_file:
         del_count = 0
         for line in r_file:
             dic = dict(zip(title.split(','), line.split(',')))
             filter_res = logic_action(dic, sql_dic.get('where'))
             if not filter_res:
                 w_file.write(line)
             else:
                 del_count += 1
         w_file.flush()
     os.remove('staff_data')
     os.rename('staff_data_bak', 'staff_data')
     return ['delete successful'], [str(del_count)]
 
 
 def update(sql_dic, title):
     '''
     处理update语句命令
     :param sql_dic:
     :param title:
     :return:
     '''
     set_l = sql_dic.get('set').strip().split(',')
     set_list = [i.split('=') for i in set_l]
     update_count = 0
     with open('staff_data', 'r', encoding='utf-8') as r_file,
             open('staff_data_bak', 'w', encoding='utf-8') as w_file:
         for line in r_file:
             dic = dict(zip(title.split(','), line.strip().split(',')))
             filter_res = logic_action(dic, sql_dic.get('where'))
             if filter_res:
                 for i in set_list:
                     k = i[0]
                     v = i[-1]
                     dic[k] = v
                 line = [dic[i] for i in title.split(',')]
                 update_count += 1
                 line = ','.join(line)+'n'
             w_file.write(line)
         w_file.flush()
     os.remove('staff_data')
     os.rename('staff_data_bak', 'staff_data')
     return ['update successful'], [str(update_count)]
 
 
 def where_action(fh, where_list, title):
     '''
     具体处理where_list里的所有条件
     :param fh:
     :param where_list:
     :param title:
     :return:
     '''
     res = []
     if len(where_list) != 0:
         for line in fh:
             dic = dict(zip(title.split(','), line.strip().split(',')))
             if dic['name'] != 'name':
                 logic_res = logic_action(dic, where_list)
                 if logic_res:
                     res.append(line.strip().split(','))
     else:
         res = [i.split(',') for i in fh.readlines()]
     return res
     pass
 
 
 def logic_action(dic, where_list):
     '''
     判断数据文件中每一条是否符合where_list条件
     :param dic:
     :param where_list:
     :return:
     '''
     logic = []
     for exp in where_list:
         if type(exp) is list:
             exp_k, opt, exp_v = exp
             if exp[1] == '=':
                 opt = '=='
             logical_char = "'%s'%s'%s'" % (dic[exp_k], opt, exp_v)
             if opt != 'like':
                 exp = str(eval(logical_char))
             else:
                 if exp_v in dic[exp_k]:
                     exp = 'True'
                 else:
                     exp = 'False'
         logic.append(exp)
     res = eval(' '.join(logic))
     return res
 
 
 def limit_action(filter_res, limit_l):
     '''
     用列表切分处理显示符合条件的数量
     :param filter_res:
     :param limit_l:
     :return:
     '''
     if limit_l:
         index = int(limit_l[0])
         res = filter_res[:index]
     else:
         res = filter_res
     return res
 
 
 def search_action(limit_res, select_list, title):
     '''
     处理需要查询并显示的title和相应数据
     :param limit_res:
     :param select_list:
     :param title:
     :return:
     '''
     res = []
     fields_list = title.split(',')
     if select_list[0] == '*':
         res = limit_res
     else:
         fields_list = select_list
         for data in limit_res:
             dic = dict(zip(title.split(','), data))
             r_l = []
             for i in fields_list:
                 r_l.append((dic[i].strip()))
             res.append(r_l)
     return fields_list, res
 
 
 if __name__ == '__main__':
     with open('staff_data', 'r', encoding='utf-8') as f:
         title = f.readline().strip()
     key_lis = ['select', 'insert', 'delete', 'update', 'from', 'into', 'set', 'values', 'where', 'limit']
     while True:
         sql = input('请输入sql命令,退出请输入exit:').strip()
         sql = re.sub(' ', '', sql)
         if len(sql) == 0:continue
         if sql == 'exit':break
         sql_dict = sql_parse(sql, key_lis)
         fields_list, fields_data = sql_action(sql_dict, title)
         print('33[1;33m结果如下:33[0m')
         print('-'.join(fields_list))
         for data in fields_data:
             print('-'.join(data))