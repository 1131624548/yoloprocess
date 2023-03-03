# -*- coding: utf-8 -*-
from opencv_vision.keypoints import Keypoints_service,SiftDetector
from base.db.sqlite_db import SqliteDictKVDB
from base.utils.image_helper import get_file_md5
from multiprocessing import Pool
import os
import time
import logging as logger
def add(imagepath):
    des = SiftDetector(nfeatures=500)
    featuredb = SqliteDictKVDB(dbfile="siftdb_houshi.sqlite")
    server = Keypoints_service(des, featuredb)
    imglist = os.listdir(imagepath)
    for img in imglist:
        imagename = os.path.join(imagepath, img)
        fileid = get_file_md5(imagename)
        print(fileid)
        server.addImage(imagename, img.split(".")[0])
    logger.info("db info: {}".format(server.dbinfo("1")))
    return 0

def query(imagepath):
    pool = Pool(4)
    start1 = time.time()
    des = SiftDetector(nfeatures=500)
    featuredb = SqliteDictKVDB(dbfile="siftdb_houshi.sqlite")
    # featuredb = SqliteDictKVDB(dbfile="siftdb_lungu.sqlite")
    server = Keypoints_service(des, featuredb)
    start2 = time.time()
    name_list, color_list = server.query(imagepath)
    # res = server.query(r"E:\data\qirui\ann\1be73c77fee9d0e6863653b05da8668e.jpg")

    print(time.time() - start2)
    print(time.time() - start1)
    print(name_list)
    print(color_list)

    # for i in range(100):
    #     print(i)
    #     pool.apply_async(server.query, (r"D:\data\old\1c6fc07fccb1cbeedb141a18aa5c4be5.bmp", ))
    # pool.close()
    # pool.join()

if __name__=="__main__":
    # imagepath = r"E:\data\car_hub\houshijin"
    # add(imagepath)
    #
    # query_img = r"E:\data\xunfei\LVVDB11B0MD324622\left.jpg"
    query_img = r"E:\data\dataset\qiruidata\cam4\2022_4_9_11_1_28_dev4.bmp"
    # query_img = r"E:\data\luntai\0a7c263dec27a49b9bb762915cee7d54.bmp"
    query(query_img)
