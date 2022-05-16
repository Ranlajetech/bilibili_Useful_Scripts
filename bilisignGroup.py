#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from functools import wraps

# you need to copy your cookie from your browser and paste it here
cookie = {"cookie": ""}

class Group():
    def getGroupList(self):     # find member groups you joined in
        url = r'https://api.live.bilibili.com/link_group/v1/member/my_groups'
        response = requests.get(
            url = url,
            headers = cookie
        ).json()
        if response["code"] == 0:
            self.groupList = response["data"]["list"]

    def log_signGroup(func):
        @wraps(func)
        def wrapper(self, target):
            result = func(self, target)
            if result["code"] == 0:
                print('已在 {0} 签到, {1}'.format(target["group_name"], result["msg"]))
            else:
                raise RuntimeError('Fail to sign in {0}, group_id={1}, owner_uid={2}'.format(target["group_name"],
                    target["group_id"], target["owner_uid"]))
        return wrapper

    @log_signGroup
    def signGroup(self, target):
        url_0 = r'https://api.live.bilibili.com/link_setting/v1/link_setting/sign_in?group_id='
        url_1 = r'&owner_id='
        response = requests.get(
            url = url_0 + str(target["group_id"]) + url_1 + str(target["owner_uid"]),
            headers = cookie
        ).json()
        return response
    
    def __call__(self):
        self.getGroupList()
        for target in self.groupList:
            self.signGroup(target)
        print('今日应援团已签到')

def main():
    Group()()

if __name__ == '__main__':
    main()
    input("按Enter键退出")