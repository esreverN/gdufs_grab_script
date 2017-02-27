#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import lxml.html
from PIL import Image, ImageEnhance
import pytesseract

REGISTER_URL = "http://jxgl.gdufs.edu.cn"
CODE_DIR = "qz_qrcode_img/"
EXT = ".jpg"

def get_captcha(html, cssselect):
    tree = lxml.html.fromstring(html)
    img_data = tree.cssselect(cssselect)[0].get('src')
    img_data = REGISTER_URL + img_data
    urllib.urlretrieve(img_data, CODE_DIR + 'origin' + EXT)

def captcha_to_string():
    img = Image.open(CODE_DIR + 'origin' + EXT)
    imgry = img.convert('L')
    enhancer = ImageEnhance.Contrast(imgry)
    gray = enhancer.enhance(2)
    gray.save(CODE_DIR + 'gray' + EXT)
    bw = depoint(gray)
    bw.save(CODE_DIR + 'thresholded' + EXT)
    for i in range(7, 11):
        str1 = '-psm ' + str(i)
        res = pytesseract.image_to_string(bw, config=str1)
        if res and len(res) == 4:
            return res
    return ''

# 干扰线去噪
def depoint(img):
    data = img.getdata()
    w,h = img.size
    black_point = 0
    BOLD = 1
    BLACK_CODE_LIMIT = 5
    ba = [] # 黑色
    for x in xrange(1, w - 1):
        for y in xrange(1, h - 1):
            mid_pixel = data[w * y + x]  # 中央像素点像素值
            if mid_pixel < 10:
                top_pixel = data[w * (y - BOLD) + x]
                left_pixel = data[w * y + (x - BOLD)]
                down_pixel = data[w * (y + BOLD) + x]
                right_pixel = data[w * y + (x + BOLD)]
                tl_pixel = data[w * (y - BOLD) + (x - BOLD)]
                rl_pixel = data[w * (y - BOLD) + (x + BOLD)]
                tb_pixel = data[w * (y + BOLD) + (x - BOLD)]
                rb_pixel = data[w * (y + BOLD) - (x - BOLD)]

                # 判断上下左右的黑色像素点总个数
                if top_pixel < BLACK_CODE_LIMIT:
                    black_point += 1
                if left_pixel < BLACK_CODE_LIMIT:
                    black_point += 1
                if down_pixel < BLACK_CODE_LIMIT:
                    black_point += 1
                if right_pixel < BLACK_CODE_LIMIT:
                    black_point += 1
                if tl_pixel < BLACK_CODE_LIMIT:
                    black_point += 1
                if rl_pixel < BLACK_CODE_LIMIT:
                    black_point += 1
                if tb_pixel < BLACK_CODE_LIMIT:
                    black_point += 1
                if rb_pixel < BLACK_CODE_LIMIT:
                    black_point += 1
                if black_point >= 4:
                    ba.append((x, y))
                #print black_point
                black_point = 0
    for x in xrange(1, w - 1):
        for y in xrange(1, h - 1):
            if (x, y) in ba:
                img.putpixel((x, y), 0)
            else:
                img.putpixel((x, y), 255)
    return img

def do():
    html = urllib2.urlopen(REGISTER_URL).read()
    get_captcha(html, "#SafeCodeImg")
    code = ''
    for i in range(3):
        res = captcha_to_string()
        if res:
            print "res: ", res
            code = res
            break
        else:
            code = ''
    return code

if __name__ == '__main__':
    code = do()
    print "识别结束"
