'''
Descripttion: 4 同一文件夹中的图片和xml标签文件分别移动到各自文件夹
version: 1.0
Author: xiaoxuesheng
Date: 2023-04-04 11:33:14
LastEditors:  *****
LastEditTime: *****
'''
# -*- coding: utf-8 -*-
# import time
# print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))



# 导入Python 内置模块
import os      # 多种操作系统接口
import shutil  # 高阶文件操作

root =r"E:\workspace\2-7\6\15L\17_34_48"   
image =r"E:\workspace\2-7\6\15L\17_34_48\img"
label =r"E:\workspace\2-7\6\15L\17_34_48\xml"

for x in os.scandir(root): # 返回一个 os.DirEntry 对象的迭代器，它们对应于由 path 指定目录中的条目
    if x.name.endswith(".jpg"):
        needpath = r"E:\workspace\2-7\6\15L\17_34_48/{name}".format(name=x.name)
        shutil.move(needpath,image) # 递归地将一个文件或目录 (src) 移至另一位置 (dst) 并返回目标位置。
    if x.name.endswith(".xml"):
        needpath =r"E:\workspace\2-7\6\15L\17_34_48/{name}".format(name=x.name)
        shutil.move(needpath,label)
