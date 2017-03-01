# 强智教学管理系统 抓课 Python 版

## 最近更新（重要！）

`2017-03-01` 自动识别验证码并登陆，依赖`PIL`库。[安装方法](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/00140767171357714f87a053a824ffd811d98a83b58ec13000)

## 旧版(不能识别验证码，但是不需要PIL库)

[摸我](https://github.com/TyrusChin/gdufs_grab_script/tree/python_without_pil)

## 使用方法

> 安装`PIL`库

> `python play.py` 按提示输入，遇到等待不要操作，正在运行..

## 正常运行显示结果

> `{"success":false,"message":"选课失败：此课堂选课人数已满！"}
20152016200000000000000017507`

## 异常情况解决方案

> 正常登陆强智教学管理系统

> 似乎要用浏览器点进选课列表(进入选课)才可以运行，否则会失败，原因不详

> 每一次不同的选课(正选、补退选)的zbid会有所不同，请看情况修改script_common.sh的24行附近的zbid，具体的值请正常进入选课界面，根据url进行修改

## Python 分支

> Python版本，可以跨平台用(Windows下会出现乱码，凑合用)

> 在Windows中，请用记事本将grab.bat打开，将::去掉，并将path改为play.py所在的绝对路径，然后运行

## 对于本脚本造成的任何后果，本人概不负责，请谨慎使用
