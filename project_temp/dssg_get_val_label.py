# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["01010001", "01010002", "01010005", "01010006", "01010007", "01010011"]
# names = ["散股",      "断股",   "悬垂线夹散股", "保护线散股", "保护线断股", "保护线", "无效"]
names = {"01010001":"散股",
         "01010002":"断股", 
         "01010005":"悬垂线夹散股", 
         "01010006":"保护线散股",
         "01010007":"保护线断股",
         "01010011":"保护线"}

# 设置错误标签的log输出位置
write_path = open(r'./error.txt', 'w')


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
    in_file = open('/data1/dataset_jinjuxiushi/Annotations/%s.xml' % (image_id), encoding="utf-8")
    
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
        if cls not in classes:
            print(in_file, cls)
            continue
        else:
            out_file = open('/data1/dataset_duangusuangu/val/labels/train2017/%s.txt' % image_id, 'w+')
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
    file_path = '/data1/dataset_jinjuxiushi/Annotations'

    xml_list = os.listdir(file_path)
    for xml_file in xml_list:
        print('xml_file[:-4]', xml_file)
        convert_annotation(xml_file[:-4])