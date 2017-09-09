#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/9/9


class Page(object):
    def __init__(self, current_page, all_count, base_url, per_page=10, pager_page_count=11):
        """
        :param current_page: 当前页
        :param all_count: 数据总条数
        :param base_url: 分页的url
        :param per_page: 每页显示的数据条数
        :param pager_page_count: 每页显示的页码数量
        """
        self.current_page = current_page
        self.per_page = per_page
        self.all_count = all_count
        self.base_url = base_url
        self.pager_page_count = pager_page_count
        pager_count, b = divmod(all_count, per_page)
        if b != 0:
            pager_count += 1
        self.pager_count = pager_count

    @property
    def start(self):
        """
        数据库获取值的起始索引位置
        :return:
        """
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        """
        数据库获取值的结束索引位置
        :return:
        """
        return self.current_page * self.per_page

    def page_html(self):
        """
        渲染的HTML页码
        :return:
        """
        # 页码
        pager_page_count = self.pager_page_count
        half_pager_page_count = int(pager_page_count / 2)

        if self.pager_count < self.pager_page_count:
            pager_start = 1
            pager_end = self.pager_count
        else:
            # 数据较多，页码超过11，最少110条
            if self.current_page <= half_pager_page_count:
                pager_start = 1
                pager_end = pager_page_count
            else:
                if (self.current_page + half_pager_page_count) > self.pager_count:
                    pager_start = self.pager_count - pager_page_count + 1
                    pager_end = self.pager_count
                else:
                    pager_start = self.current_page - half_pager_page_count
                    pager_end = self.current_page + half_pager_page_count
        page_list = []
        if self.current_page <= 1:
            # prev = '<a href="#">上一页</a>'
            prev = '<li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'
        else:
            # prev = '<a href="%s?page=%s">上一页</a>' % (self.base_url, self.current_page - 1,)
            prev = '<li><a href="%s?page=%s" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>' % \
                   (self.base_url, self.current_page - 1)
        page_list.append(prev)
        for i in range(pager_start, pager_end + 1):
            if self.current_page == i:
                # tpl = '<a class="active" href="%s?page=%s">%s</a>' % (self.base_url, i, i)
                tpl = '<li class="active"><a href="%s?page=%s">%s</a></li>' % (self.base_url, i, i)
            else:
                # tpl = '<a href="%s?page=%s">%s</a>' % (self.base_url, i, i)
                tpl = '<li><a href="%s?page=%s">%s</a></li>' % (self.base_url, i, i)
            page_list.append(tpl)

        if self.current_page >= self.pager_count:
            # nex = '<a href="#">下一页</a>'
            nex = '<li class="disabled"><a href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
        else:
            # nex = '<a href="%s?page=%s">下一页</a>' % (self.base_url, self.current_page + 1,)
            nex = '<li><a href="%s?page=%s" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>' % \
                  (self.base_url, self.current_page + 1)
        page_list.append(nex)
        page_str = "".join(page_list)
        return page_str
