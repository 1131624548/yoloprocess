'''
Descripttion: 2-1修改Txt标签
version: 1.0
Author: xiaoxuesheng
Date: 2023-02-04 17:13:15
LastEditors:  *****
LastEditTime: *****
'''
#coding:utf-8
import os
import re
path = r"E:\workspace\jiegou1label0imgtxt/"
# 文件列表
files = []
for file in os.listdir(path):
    if file.endswith(".txt"):
        files.append(path+file)
# 逐文件读取-修改-重写
for file in files:
    with open(file, 'r') as f:
        new_data = re.sub('^0', '1', f.read(), flags=re.MULTILINE)    # 将列中的0替换为1
    with open(file, 'w') as f:
        f.write(new_data)
