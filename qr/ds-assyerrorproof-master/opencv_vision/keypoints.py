# -*- coding: utf-8 -*-
import cv2, os,time
from base.utils.image_helper import prepare_cv_image, convert_dict2keypoint,convert_keypoint2dict,cv_imread
from base.db.sqlite_db import SqliteDictKVDB
from threading import RLock
import logging as logger
import numpy as np
from opencv_vision.color_recongnzie import get_color
FLANN_INDEX_KDTREE = 1
indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=10)
searchParams = dict(checks=50)

class KeypointsDetector():
    def __init__(self,detector,support_describe=True):
        self._detector = detector
        self.support_describe = support_describe

    def detectAndCompute(self,img,kps=None,mask=None):
        if self.support_describe:
            try:
                if kps is not None:
                    kps, descs = self._detector.compute(img,kps)
                else:
                    kps, descs = self._detector.detectAndCompute(img,mask)
                return (kps, descs)
            except Exception as e:
                logger.error("{}  detectAndCompute failed, {}".format(self.__class__.__name__,e))
        return (None, None)


class SiftDetector(KeypointsDetector):
    def __init__(self, **kwargs):

        if cv2.getVersionMajor() ==3 or cv2.getVersionMajor() == 4:
            detector = cv2.xfeatures2d.SIFT_create(**kwargs)
        else:
        #    detector = cv2.FastFeatureDetector_create()
            detector = None
        super(SiftDetector, self).__init__(detector, True)

class Keypoints_service():
    def __init__(self, descriptor, feturedb, **kwargs):
        #descriptor = SiftDetector(nfeatures=500)
        self.lock = RLock()
        # self.feturedb = SqliteDictKVDB(dbfile=kwargs.get("dbfile","siftdb1.sqlite"))
        self.feturedb = feturedb
        self.des = descriptor
        self.flann = cv2.FlannBasedMatcher(indexParams, searchParams)
        self.images = {}
        self.load_from_featdb(self.feturedb)

    def load_from_featdb(self, featdb):
        """
        从特征库加载特征
        :param featdb: 库文件或SqliteDictKVDB对象
        :return:
        """
        if isinstance(featdb, str):
            # 库文件
            featdb = SqliteDictKVDB(dbfile=featdb)

        for fileid, v in featdb.items():
            keypoints = convert_dict2keypoint(v[0])
            if len(v) == 2:
                points, descriptors = v
                self.images[fileid] = (keypoints, descriptors)
            else:
                points, descriptors, shapes = v
                self.images[fileid] = (keypoints, descriptors, shapes)

    def addImage(self, image, fileid=None, **kwargs):
        resize_width = int(kwargs.get("resize_width")) if "resize_width" in kwargs else None
        resize_height = int(kwargs.get("resize_height")) if "resize_height" in kwargs else None
        if resize_width is not None:
            img = prepare_cv_image(image, resize_width, resize_height)
        else:
            img = cv_imread(image)
        if img is None:
            return -1
        else:
            if fileid is None:
                fileid = os.path.basename(image)
            with self.lock:
                if self.feturedb and self.feturedb.get(fileid):
                    v = self.feturedb.get(fileid)
                    points, descriptors = v[:2]
                    keypoints = convert_dict2keypoint(points)
                else:
                    (keypoints, descriptors) = self.des.detectAndCompute(img)
                    if self.feturedb:
                        self.feturedb.put(fileid, (convert_keypoint2dict(keypoints),descriptors,img.shape[:2]))
                self.images[fileid] = (keypoints, descriptors,img.shape[:2])
                mask = len(keypoints)/100
        return mask

    def query(self, image, **kwargs):

        name_list, color_list = [],[]
        resize_width = int(kwargs.get("resize_width")) if "resize_width" in kwargs else 800
        resize_height = int(kwargs.get("resize_height")) if "resize_height" in kwargs else None
        result = []
        # score_img = cv2.imread(image)
        img = prepare_cv_image(image, resize_width, resize_height,cvt2gray=False)
        if img is None:
            print("{} read error.".format(image))
            return result
        (query_keypoints, query_descriptors) = self.des.detectAndCompute(img)
        try:
            if query_keypoints:
                result, pt_size = self.search(query_keypoints, query_descriptors, **kwargs)
                print(result)
                name_list, color_list = self.parse_result(result)
                # if pt_size:
                #     cropped = img[pt_size[0]:pt_size[1], pt_size[2]:pt_size[3]]
                #     color = get_color(cropped)
        except Exception as e:
            logger.exception("recognize catch exception:{}".format(e))
            cv2.imwrite("./exception"+str(time.time())+".jpg", img)
        logger.error("result====================={}".format(result))
        return name_list, color_list

    def search(self, query_keypoints, query_descriptors, key_range:list=None, **kwargs):
        """
        特征点和描述子去库中搜索
        :param query_keypoints: 特征点
        :param query_descriptors: 描述子
        :param key_range: 只比较关注的范围图片
        :param position:
        :param kwargs:
            matchid: 上次匹配库指纹ID
        :return: list [((filename, value))]
        """
        pt_size = None
        results = {}
        matchid = kwargs.get("matchid", None) #节约时间 直接上次的ID拿来
        match_score = 0.0
        if key_range is None:
            if matchid in self.images:
                imageid = matchid
                imagefeatures = self.images[imageid]
                match_score, pt_size = self.match(query_keypoints, query_descriptors, imagefeatures, **kwargs)
                results[imageid] = match_score

            if match_score <0.01:
                for imageid,imagefeatures in self.images.items():
                    match_score, pt_size = self.match(query_keypoints, query_descriptors, imagefeatures, **kwargs)
                    if match_score>0:
                        results[imageid] = match_score
        else:
            for imageid in key_range:
                if imageid in self.images:
                    imagefeatures = self.images[imageid]
                    match_score, pt_size = self.match(query_keypoints, query_descriptors, imagefeatures, **kwargs)
                    if match_score > 0:
                        results[imageid] = match_score
        search_results = []
        if len(results)>0:
            search_results = sorted([(k, v) for (k, v) in results.items() if v > 0], key=lambda x:x[1], reverse=True)
        return search_results, pt_size

    def match(self, query_keypoints, query_descriptors, imagefeatures,**kwargs):
        pt_size = None
        if len(imagefeatures) == 2:
            (keypoints, descriptors) = imagefeatures
        else:
            (keypoints, descriptors, shapes) = imagefeatures
        matches = self.flann.knnMatch(descriptors, query_descriptors, k=2)
        # 准备空的掩膜 画好的匹配项
        # matchesMask = [[0, 0] for i in range(len(matches))]
        good = []
        for i, (m, n) in enumerate(matches):
            if m.distance < 0.7 * n.distance:
                good.append(m)
                # matchesMask[i] = [1, 0]
        #根据匹配点去截图
        # if len(good) > 10:
        #     dst_pts = np.float32([query_keypoints[m.trainIdx].pt for m in good]).reshape(-1, 2, 1)
        #     x1 = int(max(dst_pts, key=lambda x: x[0][0])[0][0])
        #     y1 = int(max(dst_pts, key=lambda y: y[1][0])[1][0])
        #     x0 = int(min(dst_pts, key=lambda x: x[0][0])[0][0])
        #     y0 = int(min(dst_pts, key=lambda y: y[1][0])[1][0])
        #     pt_size = [y0, y1, x0, x1]
        # src_pts = np.float32([query_keypoints[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        match_score = len(good)/len(query_keypoints)
        # logger.error("===len(good):{}======len(query_keypoints)===========:{}".format(len(good),len(query_keypoints)))
        # logger.error("===match_score===========:{}".format(match_score))
        return match_score, pt_size

    def dbinfo(self, dbname, **kwargs):
        dbinfo = {}
        if dbname:
            dbinfo["dbname"] = dbname
        dbinfo["cnt"] = len(self.images)
        ids = list(self.images.keys())
        dbinfo["ids"] = ids if len(ids) < 1000 else ids[:1000]
        return dbinfo

    def parse_result(self, result):
        name_list = []
        color_dic = {}
        if result:
            for index, res in enumerate(result):
                color_name = res[0].split("_")
                name = color_name[0]
                # 获取轮胎和格栅型号
                if "lungu" in name or "geshan" in name:
                    if index < 2:
                        if name not in name_list:
                            name_list.append(name)
                        else:
                            name_list = [name]
                            color_dic[name] = color_name[-1]
                            break
                else:
                    # 获取后视镜，门把手，装饰条颜色
                    if name not in name_list:
                        name_list.append(name)
                        color_dic[name] = color_name[-1]
        return name_list, color_dic
