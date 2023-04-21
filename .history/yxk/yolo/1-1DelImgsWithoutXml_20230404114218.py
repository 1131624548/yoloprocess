'''
Descripttion: Del images without xml
version: 1.0
Author: xiaoxuesheng
Date: 2023-02-04 16:21:45
LastEditors:  *****
LastEditTime: *****
'''
#coding:utf-8
import time
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
# # 导入Python 内置模块
# import os      # 多种操作系统接口

# imgs_dir = r'***\img' # imgs文件夹
# xmls_dir = r'***\xml'    # xmls文件夹
 
# # 创建xml列表
# xmls = []

# # 读取xml文件名(即：标注的图片名)
# for xml in os.listdir(xmls_dir):
#     # xmls.append(os.path.splitext(xml)[0])    #append()参数：在列表末尾添加新的对象，即将所有文件名读入列表
#     xmls.append(xml.split('.')[0])  # splitext和split的区别：前者('0001','.jpg'), 后者('0001','jpg') 在此可选用
# #print(xmls)
 
# # 读取所有图片
# for img in os.listdir(imgs_dir):
#     image_name = img.split('.')[0]
#     if image_name not in xmls:
#         image_name = image_name + '.jpg'
#         #print(image_name)
#         os.remove(os.path.join(imgs_dir, image_name))