'''
Descripttion: 2-2修改xml标签
version: 1.0
Author: xiaoxuesheng
Date: 2023-02-04 17:13:15
LastEditors:  *****
LastEditTime: *****
'''
#coding:utf-8

import glob  # 查找特定文件标准库模块
import xml.etree.ElementTree as ET # xml读写模块

path = r'E:\workspace\jiegou1'    # xml文件夹路径

i = 0
for xml_file in glob.glob(path + '/*.xml'):
    # print(xml_file)
    tree = ET.parse(xml_file) 
    obj_list = tree.getroot().findall('object') 
    for per_obj in obj_list:
        if per_obj[0].text == 'jiegou':    # 错误的标签
            per_obj[0].text = '0'          # 修改为的标签
            i = i+1
    tree.write(xml_file)    # 将改好的文件重新写入，会覆盖原文件
print('共完成了{}处替换'.format(i))
