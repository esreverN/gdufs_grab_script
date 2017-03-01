#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageEnhance
import hashlib
import time
import os
import math
import config
import download


class VectorCompare:
    # 计算矢量大小
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.iteritems():
            total += count ** 2
        return math.sqrt(total)

    # 计算矢量之间的cos值
    def relation(self, concordance1, concordance2):
        relevance = 0
        topvalue = 0
        for word, count in concordance1.iteritems():
            if concordance2.has_key(word):
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

# 转换成8位像素模式 && 增加对比度
def pre(img):
    imgry = img.convert("P")
    enhancer = ImageEnhance.Contrast(imgry)
    return enhancer.enhance(2)

# 去除噪点和噪线，并二值化
def denoise(img):
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
    res_img = Image.new("P", img.size, 255)
    for x in xrange(1, w - 1):
        for y in xrange(1, h - 1):
            if (x, y) in ba:
                res_img.putpixel((x, y), 0)
    return res_img

# 获得纵向切割的坐标
def get_x_cut_points(img):
    inletter = False
    foundletter = False
    start = 0
    end = 0
    letters = []
    for y in range(img.size[0]):
        for x in range(img.size[1]):
            pix = img.getpixel((y, x))
            if pix != 255:
                inletter = True
        if foundletter == False and inletter == True:
            foundletter = True
            start = y

        if foundletter == True and inletter == False:
            foundletter = False
            end = y
            letters.append((start, end))

        inletter = False
    if len(letters) == config.LETTERS_FIXED_LENGTH + 1:
        # 多识别一个字母，去掉最前面的，加大成功率
        del letters[0]
    return letters

# 切割操作，并保存图片(用于制作训练集)
def cut_pic(img, letters):
    count = 0
    pic_list = []
    for letter in letters:
        m = hashlib.md5()
        i = img.crop((letter[0], 0, letter[1], img.size[1]))
        m.update("%s%s" % (time.time(), count))
        i.save("./cut_pic/%s.gif" % (m.hexdigest()))
        pic_list.append(m.hexdigest())
        count += 1
    return pic_list

#将图片转换为矢量
def buildvector(img):
    d1 = {}
    count = 0
    for i in img.getdata():
        d1[count] = i
        count += 1
    return d1

# 加载训练集
def load_imageset(basedir = ""):
    iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
               'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    imageset = []
    for letter in iconset:
        for i in os.listdir('./%siconset/%s/' % (basedir, letter)):
            temp = []
            if i != "Thumbs.db" and i != ".DS_Store" and i != "place":
                temp.append(buildvector(Image.open("./%siconset/%s/%s" % (basedir, letter, i))))
            imageset.append({letter: temp})
    return imageset

# 比较训练片段，得出结果
def guess_res(img, letters, imageset):
    v = VectorCompare()
    res = []
    for letter in letters:
        i = img.crop((letter[0], 0, letter[1], img.size[1]))
        guess = []
        # 将切割得到的验证码小片段与每个训练片段进行比较
        for image in imageset:
            for x, y in image.iteritems():
                if len(y) != 0:
                    guess.append((v.relation(y[0], buildvector(i)), x))

        guess.sort(reverse=True)
        res.append(guess[0])
    #  匹配度与匹配结果的元组数组 [(1.0, 'n'), (1.0, 'b'), (0.9896253015904012, 'b'), (0.9952267030562387, 'c')]
    # print res
    res_str = ""
    for t in res:
        res_str += t[1]
    return res_str

# 获取训练片段
def get_training_part(img, letters):
    cut_pic(img, letters)

# 破解验证码
def cracker(img, letters, basedir = ""):
    imageset = load_imageset(basedir)
    return guess_res(img, letters, imageset)

# 破解率检测
def crack_rate():
    test_pic_list = os.listdir('./test_pic')
    success = 0
    for fname in test_pic_list:
        if fname == "Thumbs.db" or fname == '.DS_Store' or fname == 'place':
            continue
        img = Image.open("./test_pic/" + fname)
        img = pre(img)
        img = denoise(img)
        letters = get_x_cut_points(img)
        res_msg = ["失败", "成功"]
        flag = 0
        res = "识别字母数错误"
        if config.LETTERS_FIXED_LENGTH == 0 or len(letters) == config.LETTERS_FIXED_LENGTH:
            res = cracker(img, letters)
            if fname.split('.')[0] == res:
                success += 1
                flag = 1
        print res_msg[flag], fname.split('.')[0], res
    return float(success) / len(test_pic_list)

if __name__ == '__main__':

    # 训练集生成
    # for fname in os.listdir('./training_pic'):
    #     if fname == "Thumbs.db" or fname == '.DS_Store' or fname == 'place':
    #         continue
    #     img = Image.open("./training_pic/" + fname)
    #     img = pre(img)
    #     img = denoise(img)
    #     letters = get_x_cut_points(img)
    #     if config.LETTERS_FIXED_LENGTH == 0 or len(letters) == config.LETTERS_FIXED_LENGTH:
    #         get_training_part(img, letters)
    #         # print cracker(img, letters)

    # 破解率
    print "目前在test_pic目录中的测试图片的破解率为：" + str(crack_rate())

    # 单独某个图片的破解
    test_pic_list = os.listdir('./test_pic')
    print "目前的图片列表有："
    print test_pic_list
    fname_without_ext = raw_input("输入测试图片的文件名(不含后缀)：")
    img = Image.open("./test_pic/" + fname_without_ext + config.EXT)
    img = pre(img)
    img = denoise(img)
    letters = get_x_cut_points(img)
    if config.LETTERS_FIXED_LENGTH == 0 or len(letters) == config.LETTERS_FIXED_LENGTH:
        res = cracker(img, letters)
        print "结果：" + res
        if fname_without_ext == res:
            print "破解成功"
        else:
            print "破解失败"
    else:
        print "破解失败"



