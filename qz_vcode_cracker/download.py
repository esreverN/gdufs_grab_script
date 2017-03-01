#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 下载一些测试的验证码图片，需要自己核对结果并修改图片文件名为 [result].jpg，如 xa2w.jpg

import urllib
import config
import time
import random

def dl_vcode(num, dir):
    for i in range(num):
        print "下载第(%d/%d)张验证码" % (i+1, num)
        urllib.urlretrieve(config.LOGIN_URL + config.VCODE_SRC, dir + _random_filename() + config.EXT)

def _random_filename():
    return str(int(time.time() * random.random()))

if __name__ == '__main__':
    dl_vcode(200, "./training_pic/")
    print "下载完成，请自行修改图片名为对应的[结果.jpg]"