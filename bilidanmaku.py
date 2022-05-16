#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
from functools import wraps

# you need to copy your cookie from your browser and paste it here
cookie = {"cookie": ""}

class Danmaku():

    def getMedalList(self):                 # get all medals you have
        roomList = dict()                   # a dict mapping roomid(url) to liver's nickname
        url = r'https://api.live.bilibili.com/xlive/app-ucenter/v1/fansMedal/panel?page_size=1001&page=1'
        response = requests.get(
            url = url,
            headers = cookie
        ).json()
        if response["code"] == 0:           # if response normally
            data = response["data"]
            li = data["list"]
            spe_li = data["special_list"]
            for item in li:
                roomList[item["room_info"]["room_id"]] = item["anchor_info"]["nick_name"]
            for item in spe_li:
                roomList[item["room_info"]["room_id"]] = item["anchor_info"]["nick_name"]
        else:
            raise RuntimeError('Fail to get medal list.')
        return roomList


    def __init__(self):
        self.url = r'https://api.live.bilibili.com/msg/send'
        self.send_data = {
            'bubble': 0,
            'color': 16777215,
            'mode': 1,
            'fontsize': 25,
            # you need to copy your csrf from your browser and paste it here
            'csrf': '',
            # you need to copy your csrf_tokern from your browser and paste it here
            'csrf_token': ''}
        self.targets = self.getMedalList()      # live rooms you subscribe

    def log_danmaku(func):                      # use decorator for practicing... just kidding :P
        @wraps(func)
        def wrapper(self, roomid):
            result = func(self, roomid)
            if result:
                print('已向 {0} 的直播间发送弹幕"{1}"'.format(self.targets[roomid], self.send_data['msg']))
            else:
                raise RuntimeError('Fail to send danmaku to {0}, roomid={1}'.format(self.targets[roomid], roomid))
            return result
        return wrapper

    @log_danmaku
    def sendto(self, roomid):
        self.send_data['rnd'] = time.time()
        self.send_data['roomid'] = roomid
        response = requests.post(
            url = self.url,
            data = self.send_data,
            headers = cookie,
        ).json()
        return response["code"] == 0

    def __call__(self, msg = 'ε=ε=(｀・ω・´)'):     # here you can change the msg to send
        self.send_data['msg'] = msg
        for roomid in self.targets:
            self.sendto(roomid)
            time.sleep(1.0)
        print('今日弹幕已发送')


def bililiveSign():
    url = r'https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign'
    response = requests.get(
        url = url,
        headers = cookie
    ).json()
    if response["code"] == 0:
        print('直播签到: 成功')
    elif response["code"] == 1011040:
        print('直播签到: {0}'.format(response["message"]))
    else:
        print('直播签到: 失败')
        return response

def main():
    Danmaku()()
    bililiveSign()

if __name__ == '__main__':
    main()
    input("按Enter键退出")