#coding:utf-8
import os
folder_path= r'E:\workspace\20230329\xml'     # 文件夹路径
xml_files = []
# 遍历文件夹
for dirpath, dirnames, filenames in os.walk(folder_path):
    # 遍历文件
    for filename in filenames:
        # 判断文件名是否以.xml结尾
        if filename.endswith('.xml'):
            # 添加到xml_files列表中
            xml_files.append(os.path.join(dirpath, filename))

# print(xml_files)                                                                      
for m in xml_files:                                                                         
    os.remove(m)                     