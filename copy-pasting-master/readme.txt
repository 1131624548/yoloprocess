数据增强步骤：
1、先得到裁剪的图片，将要裁剪的原图放入crop_iamges文件夹下，运行crop_img.py，得到裁剪后的各个目标小图（保存在crop下）和小图对应的crop_small.txt文件
2、将数据集原图复制到insect_image文件夹下，再把对应的xml标签文件复制到xmls/文件夹下，运行voc2yolo.py文件，在insect_image下生成对应图片的txt文件（yolov5格式）；
3、由于crop下已经有分割好的小图了，故直接运行demo.py，程序结束后在save_path下生成增强后的图片，在save_txt下生成增强后图片的txt文件（用于生成xml文件）
4、运行yolo2voc.py生成增强后图像的xml文件，在aug_xml中


注意：
* utils.py文件中的random_add_patches函数，函数内的cl变量存的是目标类别的下标，-6代表字符串倒数第六位，如188_crop_1.jpeg倒数第六位就是1，对应1号类别
