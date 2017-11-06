#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/11/3


import os
import time
import requests
import json


def exec_script(path):
    os.popen(path)
    push_data = []
    metric_dic = {
        'metric': None,
        'endpoint': 'consumer-prod-shanxin-oracle-database',
        'timestamp': int(time.time()),
        'step': 60,
        'value': None,
        'counterType': 'GAUGE',
        'tags': None
    }
    with open('/tmp/tablespace.log','r') as f:
        for line in f.readlines()[6:-2]:
            data = line.strip().split('\t')
            metric_dic['metric'] = 'oracle.tablespace.%s' % data[1].strip()
            metric_dic['value'] = data.pop(-1).strip()
            metric_dic['tags'] = 'db=oracle,tablespace=%s' % data[1].strip()
            push_data.append(metric_dic)
            print json.dumps(push_data,indent=4)
    return push_data


if __name__ == '__main__':
    path = "/app/oracle/oracle_cron.sh"
    url = 'http://127.0.0.1:1988/v1/push'
    data = exec_script(path)
    response = requests.post(url, data=json.dumps(data))
    print(response.status_code, response.text)
