'''
Descripttion: 4 同一文件夹中的图片和xml标签文件分别移动到各自文件夹
version: 1.0
Author: xiaoxuesheng
Date: 2023-02-04 17:39:15
LastEditors:  *****
LastEditTime: *****
'''
#coding:utf-8
import os      # 导入os文件操作模块
import shutil  # 导入shutil高级文件操作模块
root =r"E:\workspace\2-7\6\15L\17_34_48"   
image =r"E:\workspace\2-7\6\15L\17_34_48\img"
label =r"E:\workspace\2-7\6\15L\17_34_48\xml"

for x in os.scandir(root):
    if x.name.endswith(".jpg"):
        needpath = r"E:\workspace\2-7\6\15L\17_34_48/{name}".format(name=x.name)
        shutil.move(needpath,image)
    if x.name.endswith(".xml"):
        needpath =r"E:\workspace\2-7\6\15L\17_34_48/{name}".format(name=x.name)
        shutil.move(needpath,label)
