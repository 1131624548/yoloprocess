from os import listdir, getcwd
from os.path import join
import xml.etree.ElementTree as ET
import glob
'''
    本脚本功能：将每张图像转化为yolov5格式的txt文件
'''

classes = ['Boerner', 'Leconte', 'Linnaeus', 'acuminatus', 'armandi', 'coleoptera', 'linnaeus']


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


# image_name为图像文件名，如 1.jpeg
def convert_annotation(image_name):
    # in_file为对应图像的xml文件路径，注意：-3和-4
    in_file = open('xmls/' + image_name[:-4] + 'xml', encoding='utf-8')
    # out_file为写入路径, txt文件保存路径
    out_file = open('insect_image/' + image_name[:-4] + 'txt', 'w')

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            print(cls)
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


wd = getcwd()

if __name__ == '__main__':
    # 括号中为图像保存路径
    for image_path in glob.glob('insect_image/*.jpeg'):
        image_name = image_path.split('\\')[-1]
        convert_annotation(image_name)
    # for image_path in glob.glob('D:/python_project/yolov5/VOC_small/images/val/*.jpg'):
    #     image_name = image_path.split('\\')[-1]
    #     convert_annotation(image_name, 'val')