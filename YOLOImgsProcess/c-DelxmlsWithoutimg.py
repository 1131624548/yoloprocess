'''
Descripttion: 1删除未标记图片
version: 1.0
Author: xiaoxuesheng
Date: 2023-02-04 16:21:45
LastEditors:  *****
LastEditTime: *****
'''
#coding:utf-8
import os # 导入os库

imgs_dir = r'***\img' # imgs文件夹
xmls_dir = r'***\xml'    # xmls文件夹
# 删除没有img的xml
imgs = []
for img in os.listdir(imgs_dir):
    imgs.append(img.split('.')[0])
#print(imgs)
# 读取所有图片
for xml in os.listdir(xmls_dir):
    xml_name = xml.split('.')[0]
    if xml_name not in imgs:
        xml_name = xml_name + '.xml'
    
        os.remove(os.path.join(xmls_dir, xml_name))
