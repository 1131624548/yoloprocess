#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import math
import os
import hashlib

def convert_keypoint2dict(keypoint):
    points = []
    for p in keypoint:
        pdict = {"pt": p.pt,
                 "size": p.size,
                 "angle": p.angle,
                 "res": p.response,
                 "octave": p.octave,
                 "class_id": p.class_id
                 }
        points.append(pdict)
    return points

def convert_dict2keypoint(points):
    keypoints = []
    for p in points:
        kp = cv2.KeyPoint(x=p["pt"][0], y=p["pt"][1], _size=p["size"], _angle=p["angle"],
                          _response=p["res"], _octave=p["octave"], _class_id=p["class_id"])
        keypoints.append(kp)
    return keypoints

def cv_imread(filePath, image_sz = None, grayload = False):
    """
    读取图像
        1. 解决cv2.imread不能读取中文路径的问题
        2. cv2.IMREAD_ANYCOLOR, cv2.IMREAD_ANYDEPTH, cv2.IMREAD_COLOR, etc
        3. img is a numpy array, so use img.shape, img.dtype
    :param filePath: 图像文件名
    :param image_sz: 自动将输入图像缩放到指定的尺寸
    :param grayload: 强制使用灰度图像方式读取
    :return: BGR array image
    """
    mode = cv2.IMREAD_GRAYSCALE if grayload else cv2.IMREAD_COLOR
    try:
        cv_img = cv2.imdecode(np.fromfile(filePath,dtype=np.uint8), mode)
        if cv_img is None:
            cv_img = cv2.imread(filePath)

        if image_sz is not None:
            cv_img = cv2.resize(cv_img, image_sz)
        return cv_img
    except Exception as e:
        print('cv_imread image failed: {}->{}'.format(filePath, e))
        return None

def cv_cvt2gray(image):
    shapelen = len(image.shape)
    if shapelen == 2:
        return image
    else:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 图像缩放: 保持宽高比，设置 width, height 之一即可
def cv_resize_image(image, width=None, height=None, inter=cv2.INTER_AREA):
    # Grab the image size
    (h, w) = image.shape[:2]

    # If both the width and height are None, then return the original image
    if width is None and height is None:
        return image

    # Check to see if the width is None
    if width is None:
        # Calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # Otherwise, the height is None
    elif height is None:
        # Calculate the ratio of the width and construct the dimensions
        r = width / float(w)
        dim = (width, int(h * r))
    else:
        dim = (width, height)

    # Resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # Return the resized image
    return resized

def prepare_cv_image( image, resize_width=None, resize_height=None, cvt2gray=True):
    if isinstance(image, str):
        img = cv_imread(image)
    else:
        img = image
    if img is None:
        # 读取图片异常
        return img

    if cvt2gray:
        img = cv_cvt2gray(img)
    if not resize_width or not resize_height:
        img = cv_resize_image(img, resize_width, resize_height)
    return img

def get_file_md5(filename, blocaksize=2*20):
    if not os.path.isfile(filename):
        return ""
    imgRB = open(filename, "rb")
    RBcont = imgRB.read()
    md5 = hashlib.md5(RBcont)
    return md5.hexdigest()