'''
Descripttion:  同一文件夹中的图片和xml标签文件分别移动到各自文件夹，删除没有xml的img，删除没有img的xml
version: 1.0
Author: xiaoxuesheng
Date: 2023-02-08 15:10:15
LastEditors:  *****
LastEditTime: *****
import time
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))   
'''
#coding:utf-8
import os      # 导入os文件操作模块
import shutil  # 导入shutil高级文件操作模块


root =r"E:\workspace\20230412" # 图片和标签在同一个文件夹中
if not os.path.exists(root):
    os.makedirs(root)

#源文件夹路径
path = r"E:\workspace\datasets\4-11\x13"
folders= os.listdir(path)
for folder in folders:
    dir = path + '\\' +  str(folder)
    files = os.listdir(dir)
    for file in files:
        source = dir + '\\' + str(file)
        deter = root + '\\' +str(file)
        shutil.copyfile(source, deter)


# 同一个文件夹中的图片标签分类
for x in os.listdir(root):
    if not os.path.exists(os.path.join(root,"img")):
        os.mkdir(os.path.join(root,"img"))
    if not os.path.exists(os.path.join(root,"xml")):
        os.mkdir(os.path.join(root,"xml"))
    if not os.path.exists(os.path.join(root,"txt")):
        os.mkdir(os.path.join(root,"txt"))
    if x.endswith(".jpg"):
        oldpath = os.path.join(root,x)
        newpath = os.path.join(root,"img",x)
        shutil.move(oldpath,newpath) # shutil.move("oldpos","newpos")   
    if x.endswith(".xml"):
        oldpath = os.path.join(root,x)
        newpath = os.path.join(root,"xml",x)
        shutil.move(oldpath,newpath)
    if x.endswith(".txt"):
        oldpath = os.path.join(root,x)
        newpath = os.path.join(root,"txt",x)
        shutil.move(oldpath,newpath)

# 删除没有xml的img
xmls = []
for xml in os.listdir(os.path.join(root,"xml")):
    xmls.append(xml.split('.')[0])  # splitext和split的区别：前者('0001','.jpg'), 后者('0001','jpg') 在此可选用
#print(xmls)
 
# 读取所有图片
for img in os.listdir(os.path.join(root,"img")):
    image_name = img.split('.')[0]
    if image_name not in xmls:
        image_name = image_name + '.jpg'
        #print(image_name)
        os.remove(os.path.join(root,"img", image_name))


# 删除没有img的xml
imgs = []
for img in os.listdir(os.path.join(root,"img")):
    imgs.append(img.split('.')[0])
#print(imgs)
# 读取所有图片
for xml in os.listdir(os.path.join(root,"xml")):
    xml_name = xml.split('.')[0]
    if xml_name not in imgs:
        xml_name = xml_name + '.xml'
    
        os.remove(os.path.join(root,"xml", xml_name))




# # 同一个文件夹中的图片标签分类
# for x in os.listdir(root):
#     if not os.path.exists(os.path.join(root,"img")):
#         os.mkdir(os.path.join(root,"img"))
#     if not os.path.exists(os.path.join(root,"txt")):
#         os.mkdir(os.path.join(root,"txt"))
#     if x.endswith(".jpg"):
#         oldpath = os.path.join(root,x)
#         newpath = os.path.join(root,"img",x)
#         shutil.move(oldpath,newpath) # shutil.move("oldpos","newpos")   
#     elif x.endswith(".txt"):
#         oldpath = os.path.join(root,x)
#         newpath = os.path.join(root,"txt",x)
#         shutil.move(oldpath,newpath)

# # 删除没有txt的img
# txts = []
# for txt in os.listdir(os.path.join(root,"txt")):
#     txts.append(txt.split('.')[0])  # splitext和split的区别：前者('0001','.jpg'), 后者('0001','jpg') 在此可选用
# #print(xmls)
 
# # 读取所有图片
# for img in os.listdir(os.path.join(root,"img")):
#     image_name = img.split('.')[0]
#     if image_name not in txts:
#         image_name = image_name + '.jpg'
#         #print(image_name)
#         os.remove(os.path.join(root,"img", image_name))


if __name__ == '__main__':
    pass