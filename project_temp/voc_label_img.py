# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import shutil

# sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["01010001", "01010002", "01010005", "01010006", "01010007"]
names = ["散股", "断股", "悬垂线夹散股", "保护线散股", "保护线断股"]

# 这里根据自己的路径修改


# 设置错误标签
write_path = open(os.path.join('/data1/dataset_duangusuangu', 'error.txt'), 'w')


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


def convert_annotation(anno_path, jpeg_path, image_path, label_path):
    xml_list = os.listdir(anno_path)
    for xml_file in xml_list:
        image_id = xml_file.split('.')[0]
        in_file = open(os.path.join(anno_path, '%s.xml' % image_id), encoding="utf-8")

        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        if w == 0 or h == 0:
            continue

        flag = True
        for obj in root.iter('object'):
            # difficult = obj.find('difficult').text
            cls = obj.find('name').text
            # if cls not in classes or int(difficult) == 1:
            #     continue
            # print(in_file)
            # 标签自查
            if cls not in classes:
                # print(in_file, cls)
                continue
            else:
                out_file = open(os.path.join(label_path, '%s.txt' % image_id), 'w+')
                flag = False
                cls_id = classes.index(cls)
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text),
                     float(xmlbox.find('xmax').text),
                     float(xmlbox.find('ymin').text),
                     float(xmlbox.find('ymax').text))
                bb = convert((w, h), b)
                out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

        if flag is False:
            filename = image_id + ".jpg"
            # print("****************")
            # print(filename)   
            # print(xml_file)
            if not os.path.exists(os.path.join(jpeg_path, filename)):
                print("not exists file: ", os.path.join(jpeg_path, filename))
                continue
            else:
                shutil.copy(os.path.join(jpeg_path, filename), image_path)
                # print(os.path.join(jpeg_path, filename), "   to    ", image_path)
        elif flag is True:
            write_path.write('%s.xml' % image_id + ' ' + '\n')


if __name__ == "__main__":
    root = "/data1/dataset_duangusuangu"
    destroot = "/data1/dataset_duangusuangu/train"
    annotation_path = 'Annotations'
    JPEGImages_path = "JPEGImages"
    IMAGES_path = "images/train2017"
    LABELS_path = "labels/train2017"

    anno_path = os.path.join(root, annotation_path)
    jpeg_path = os.path.join(root, JPEGImages_path)
    image_path = os.path.join(destroot, IMAGES_path)
    label_path = os.path.join(destroot, LABELS_path)

    if not os.path.exists(image_path):
        os.makedirs(image_path)

    if not os.path.exists(label_path):
        os.makedirs(label_path)

    convert_annotation(anno_path, jpeg_path, image_path, label_path)
