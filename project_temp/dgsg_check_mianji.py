# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import numpy as np

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
# write_path = open(r'./error.txt', 'w')


# def convert(size, box):
#     dw = 1. / (size[0])
#     dh = 1. / (size[1])
#     x = (box[0] + box[1]) / 2.0 - 1
#     y = (box[2] + box[3]) / 2.0 - 1
#     w = box[1] - box[0]
#     h = box[3] - box[2]
#     x = x * dw
#     w = w * dw
#     y = y * dh
#     h = h * dh
#     return (x, y, w, h)


def convert_annotation(file_path):
    xml_list = os.listdir(file_path)
    rates = []
    for xml_file in xml_list:
        # print('xml_file[:-4]', xml_file)
        in_file = open(os.path.join(file_path, xml_file), encoding="utf-8")
        
        #这里根据自己的路径修改
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
            if cls not in classes:
                # print(in_file, cls)
                continue
            else:
                # out_file = open('/data1/dataset_duangusuangu/val/labels/train2017/%s.txt' % image_id, 'w+')
                flag = False
                cls_id = classes.index(cls)
                xmlbox = obj.find('bndbox')
                xmin = float(xmlbox.find('xmin').text)
                xmax = float(xmlbox.find('xmax').text)
                ymin = float(xmlbox.find('ymin').text)
                ymax = float(xmlbox.find('ymax').text)

                rates.append(np.sqrt((xmax - xmin) * (ymax - ymin) / (w * h)) * 640)
    print(rates)


if __name__ == "__main__":
    file_path = '/data1/dataset_duangusuangu/Annotations'
    convert_annotation(file_path)