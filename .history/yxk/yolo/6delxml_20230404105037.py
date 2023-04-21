'''
Descripttion: 5 训练验证测试集的划分
version: 1.0
Author: xiaoxuesheng
Date: 2023-03-30 09:38:20
LastEditors:  *****
LastEditTime: *****
'''
#coding:utf-8
import os # 多种操作系统接口
import time
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))   

# folder_path= r'E:\workspace\20230404\xml'     # 文件夹路径
# xml_files = []
# # 遍历文件夹
# for dirpath, dirnames, filenames in os.walk(folder_path):
#     # 遍历文件
#     for filename in filenames:
#         # 判断文件名是否以.xml结尾
#         if filename.endswith('.xml'):
#             # 添加到xml_files列表中
#             xml_files.append(os.path.join(dirpath, filename))

# # print(xml_files)                                                                      
# for m in xml_files:                                                                         
#     os.remove(m)                     