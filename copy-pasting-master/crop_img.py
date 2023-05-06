import os  # 多种操作系统接口
import shutil
from os.path import join
import cv2
import glob

# 本代码实现对原图进行裁剪目标，运行该程序会生成剪切图片（存在crop文件夹），剪切图片相对路径（在dpj_small.txt）

# 原图存放路径（将原图上目标进行裁剪）
root_dir = "./save_path"
# 裁剪后的小图像块保存路径
save_dir = "./crop"
# 遍历所有图片，将路径存入jpg_list中
jpg_list = glob.glob(root_dir + "/*.jpeg")

classes = ['Boerner', 'Leconte', 'Linnaeus', 'acuminatus', 'armandi', 'coleoptera', 'linnaeus']

fo = open("crop_small2.txt", "w")

max_s = -1
min_s = 1000

# jpg_path为每张图像的相对路径
for jpg_path in jpg_list:
    # jpg_path = jpg_list[3]
    # 将原图的相对路径中.jpeg 换成.txt，得到原图对应的yolo型txt文件的路径txt_path
    txt_path = jpg_path.replace("jpeg", "txt")
    jpg_name = os.path.basename(jpg_path)
    # 打开txt文件
    f = open(txt_path, "r")
    # img为图片的三维数组，shape为(h, w, 3)
    img = cv2.imread(jpg_path)

    height, width, channel = img.shape
    # 图片对应的txt文件中的行，file_contents为列表，存放txt文件中的行
    file_contents = f.readlines()

    # num为行下标编号，file_contents为某行内容（class x_center y_center width height）
    for num, file_content in enumerate(file_contents):
        print(num)
        # 把某行的内容按空格划分为 类别号、框中心x、框中心y、框宽、框高
        clss, xc, yc, w, h = file_content.split()
        # 把坐标四个值转化为浮点型
        xc, yc, w, h = float(xc), float(yc), float(w), float(h)

        # 把框中心分别乘以原图宽高（因为刚开始在生成txt时除了原图宽高，现在要变回去）
        xc *= width
        xc += 1
        yc *= height
        yc += 1
        w *= width
        h *= height

        max_s = max(w*h, max_s)
        min_s = min(w*h, min_s)
        # 得到框的宽高的一半
        half_w, half_h = w // 2, h // 2
        # 由中心点求出左上角右下角
        x1, y1 = int(xc - half_w), int(yc - half_h)
        x2, y2 = int(xc + half_w), int(yc + half_h)

        # crop_img为裁剪图像的数组，shape为(y2-y1, x2-x1, 3)
        crop_img = img[y1:y2, x1:x2]

        # 裁剪图像命名
        new_jpg_name = jpg_name.split('.')[0] + "_crop_" + str(clss) + ".jpeg"
        cv2.imwrite(os.path.join(save_dir, new_jpg_name), crop_img)
        # cv2.imshow("croped",crop_img)
        # cv2.waitKey(0)e

        # 在crop_small.txt文件中写入裁剪后得到的所有图片的路径：如 ./crop\1_crop_0.jpeg
        fo.write(os.path.join(save_dir, new_jpg_name)+"\n")

    f.close()


fo.close()

print(max_s, min_s)