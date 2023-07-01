# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ['04010005', '02030006', '06020003', '01010008', '01020001', '03060011', '07010041',
           '07010043', '03060020', '03030007', '03060004', '03040026', '07010034', '07010035',
           '07010036', '07010037', '07010048', '07010038', '07010039', '07010046', '07010045',
           '07010050', '07010052', '07010054', '07010056', '01010010', '07010057', '07010058',
           '07010059', '07010060', '07010061', '07010062', '07010063', '07010064', '07010065']


# 设置错误标签的log输出位置
write_path = open(r'/data1/jinjuxiushi/error.txt', 'w')

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


def convert_annotation(image_id):
    in_file = open('/data1/jinjuxiushi/Annotations/%s.xml' % (image_id), encoding="utf-8")
    out_file = open('/data1/jinjuxiushi/labels/%s.txt' % image_id, 'w')
    #这里根据自己的路径修改
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    if w == 0 or h == 0:
        return

    flag = True
    for obj in root.iter('object'):
        # difficult = obj.find('difficult').text
        cls = obj.find('name').text
        # if cls not in classes or int(difficult) == 1:
        #     continue
        # print(in_file)
        # 标签自查
        if cls not in classes:
            print(in_file, cls)
            continue
        else:
            flag = False
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text),
                 float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    if flag is True:
        write_path.write('%s.xml' % image_id + ' ' + '\n')


if __name__ == "__main__":
    file_path = '/data1/jinjuxiushi/Annotations'

    xml_list = os.listdir(file_path)
    for xml_file in xml_list:
        print('xml_file[:-4]', xml_file)
        convert_annotation(xml_file[:-4])



# wd = getcwd()

# for year, image_set in sets:
#     if not os.path.exists('VOCdevkit/VOC%s/labels/' % (year)):
#         os.makedirs('VOCdevkit/VOC%s/labels/' % (year))
#     image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt' % (year, image_set)).read().strip().split()
#     list_file = open('%s_%s.txt' % (year, image_set), 'w')
#     for image_id in image_ids:
#         list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg\n' % (wd, year, image_id))
#         convert_annotation(year, image_id)
#     list_file.close()

# os.system("cat 2007_train.txt 2007_val.txt 2012_train.txt 2012_val.txt > train.txt")
# os.system("cat 2007_train.txt 2007_val.txt 2007_test.txt 2012_train.txt 2012_val.txt > train.all.txt")


