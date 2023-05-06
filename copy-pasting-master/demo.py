# Descripttion:***
# version: 1.0 
# Author: xiaoxuesheng
# Date: 2023-05-05 09:04:26
# LastEditors:  *****
# LastEditTime: *****
# import time
# print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
# -*- coding: utf-8 -*-


import os # 多种操作系统接口
from os.path import join 
import random # 生成伪随机数



import aug
import Helpers as hp
from util import *

# ###########Pipeline##############
"""
1 准备数据集和yolo格式标签, 如果自己的数据集是voc或coco格式的，先转换成yolo格式，增强后在转回来
2 run crop_image.py  裁剪出目标并保存图片
3 run demo.py   随机将裁剪出目标图片贴到需要增强的数据集上，并且保存增强后的图片集和label文件
"""
# 获取本文件所处的上层文件夹：'D:\\python_project\\data_aug'
base_dir = os.getcwd()
# 字符串拼接，得到增强后的图片的保存路径   'D:\\python_project\\data_aug\\save_path'
save_base_dir = join(base_dir, 'save_path')
# 看save_base_dir存在否，不存在则创建
check_dir(save_base_dir)

# imgs_dir为列表，存放原始图片的路径
# imgs_dir = [f.strip() for f in open(join(base_dir, 'sea.txt')).readlines()]
imgs_dir = [os.path.join('insect_image', f) for f in os.listdir('insect_image') if f.endswith('jpg')]

# labels_dir列表存放原始图像生成的txt文件路径，
labels_dir = hp.replace_labels(imgs_dir)

# small_imgs_dir列表存放剪切图片的路径
# small_imgs_dir = [f.strip() for f in open(join(base_dir, 'dpj_small.txt')).readlines()]
small_imgs_dir = [os.path.join('crop', f) for f in os.listdir('crop') if f.endswith('jpg')]
random.shuffle(small_imgs_dir)  # 目标图片打乱
# print(small_imgs_dir)

times = 2  # 随机选择增加多少个目标

for image_dir, label_dir in zip(imgs_dir, labels_dir):
   # print(label_dir)

    # 将小目标的图片路径存入列表，如：['crop\\1_crop_2.jpeg', 'crop\\1_crop_6.jpeg']
    small_img = []
    for x in range(times):
        if small_imgs_dir == []:
            small_imgs_dir = [os.path.join('crop', f) for f in os.listdir('crop') if f.endswith('jpg')]
            random.shuffle(small_imgs_dir)
        # 列表弹出最后一个，图片路径
        small_img.append(small_imgs_dir.pop())

    # small_img = ['crop\\1840_crop_2.jpeg', 'crop\\1840_crop_3.jpeg', 'crop\\1_crop_6.jpeg']
    # image_dir：源图像路径；label_dir：原图像txt路径；save_base_dir：增强后图像保存路径；small_img：列表，存放裁剪图像路径
    aug.copysmallobjects(image_dir, label_dir, save_base_dir, small_img, times)
