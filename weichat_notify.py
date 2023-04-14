# -*- coding: utf-8 -*-
# @Time : 2023/3/6 13:53
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : weichat_notify.py
# @Project : 东方财富OCR
import json

import requests


def send_weixin_message(key, content):
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}".format(key)
    headers = {"Content-Type": "application/json"}  # http数据头，类型为json
    data = {
        "msgtype": "text",
        "text": {
            "content": content,  # 让群机器人发送的消息内容。
            "mentioned_list": [],
        }
    }
    requests.post(url, headers=headers, json=data)  # 利用requests库发送post请求


def send_dingding_message(access_token, content):
    dingd_url = "https://oapi.dingtalk.com/robot/send?access_token={}".format(access_token)  # 这里替换为你刚才复制的内容
    headers = {'Content-Type': 'application/json'}
    data = {"msgtype": "text", "text": {"content": content}}
    requests.post(dingd_url, data=json.dumps(data), headers=headers)


if __name__ == '__main__':
    key = "42b80f3b-8443-4d4f-989a-2e14f0f931e8"
    send_weixin_message(key, "消息内容")
    # 必须包含 关键字 通知，不然收不到消息
    token = "ede2dde41e62a4f5a45484cfaa1703234965723cb43551b256b3cdd812c32d42"
    send_dingding_message(token, "通知121")