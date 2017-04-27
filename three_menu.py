#!/usr/bin/python
# -*- coding:utf-8 -*-

dic = {
    "河北": {
        "石家庄": ["鹿泉", "藁城", "元氏"],
        "邯郸": ["永年", "涉县", "磁县"],
        "唐山": ["玉田", "乐亭", "丰南"],
    },
    "河南": {
        "郑州": ["上街", "巩义", "新郑", "登封"],
        "洛阳": ["关林", "洛川", "栾川"],
        "安阳": ["林州", "滑县", "汤阴"],
    },
    "山西": {
        "太原": ["清徐", "阳曲", "古交"],
        "晋中": ["左权", "太谷", "灵石"],
        "运城": ["永济", "万荣", "平陆"],
    }
}

pro_list = list(dic.keys())  # 获取省列表
# print(pro_list)


while True:
    print(" 省 ".center(50, '*'))
    for i in pro_list:
        print(pro_list.index(i) + 1, i)                         # 打印省列表
    pro_id = input("Please input a number or quit='q': ")       # 获取省编号
    if pro_id.isdigit():                                        # 判断输入是否为数字
        pro_id = int(pro_id)
        if (pro_id > 0) and (pro_id <= len(pro_list)):          # 判断输入序号是否在区间
            city = (list(dic[pro_list[pro_id - 1]].keys()))     # 根据用户输入查询市列表
            # print(city)
            while True:
                print(" 市 ".center(50, '*'))
                for i in city:
                    print(city.index(i) + 1, i)                 # 打印市列表
                city_id = input("Please select city or back='b' or quit='q': ")
                if city_id.isdigit():
                    city_id = int(city_id)
                    if (city_id > 0) and (city_id <= len(city)):
                        county_list = dic[pro_list[pro_id - 1]][city[city_id - 1]]      # 县列表
                        while True:
                            print(" 县 ".center(50, "*"))
                            for item in county_list:
                                print(county_list.index(item) + 1, item)                # 打印县列表
                            back = input("Please input 'b' to back or 'q' to exit: ")
                            if back == "b":                                             # 跳出县级别循环
                                break
                            elif back == "q":
                                exit()                                                  # 退出程序
                            else:
                                print("\033[1;31mSorry,please input 'b' or 'q'!\033[0m")
                    elif city_id == "b":             # 根据用户输入选择返回上一层，即市级别
                        break
                    elif city_id == "q":             # 退出程序
                        eixt()
                    else:                            # 市级别输入编号合法性判定
                        print("\033[1;31mSorry,Please input a number less than equal %d\033[0m" % len(city))
                elif city_id == "b":                 # 根据用户输入选择返回上一层，即省级别
                    break
                elif city_id == "q":                 # 根据用户输入退出程序
                    exit()
                else:                                # 市级别输入编号合法性判定
                    print("\033[1;31mSorry,your choice city is not found,please check!\033[0m")
        else:                                        # 省级别输入编号合法性判定
            print("\033[1;31mSorry,your choice province is not found,please check!\033[0m")
    elif pro_id == 'q':                              # 省级别输入判断
        exit()
    else:
        print("\033[1;31mSorry,input error,please input a number!\033[0m")
