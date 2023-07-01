# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["01010001", "01010002", "01010005", "01010006", "01010007", "01010011"]
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


def get_name_index(shaixuan_path):
    names = {}
    files = os.listdir(shaixuan_path)
    for file in files:
        if file.split('.')[0][:10] not in list(names.keys()):
            names[file.split('.')[0][:10]] = []
        names[file.split('.')[0][:10]].append(int(file.split('.')[0][-3:]))
    return names


def convert_annotation(src_xml_dir, dst_txt_dir, names):
    xml_list = os.listdir(src_xml_dir)
    for xml_file in xml_list:
        print('xml_file[:-4]', xml_file)
        image_id = xml_file[:-4]
        indexes = names[xml_file[:-4]]

        in_file = open(os.path.join(src_xml_dir, '%s.xml' % image_id), encoding="utf-8")
        out_file = open(os.path.join(dst_txt_dir, '%s.txt' % image_id), 'w')
        #这里根据自己的路径修改
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        if w == 0 or h == 0:
            return

        flag = True
        for i, obj in enumerate(root.iter('object')):
            # difficult = obj.find('difficult').text
            flag = True
            if i in indexes:
                flag = False
                cls = obj.find('name').text
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
    src_xml_dir = '/data1/dataset_duangusuangu/shai/Annotations'
    dst_txt_dir = "/data1/dataset_duangusuangu/dataset/train/labels/train2017"
    shaixuan_dir = "/data1/dataset_duangusuangu/shaixuan/shaixuan"

    if not os.path.exists(dst_txt_dir):
        os.makedirs(dst_txt_dir)

    names = get_name_index(shaixuan_dir)
    convert_annotation(src_xml_dir, dst_txt_dir, names)