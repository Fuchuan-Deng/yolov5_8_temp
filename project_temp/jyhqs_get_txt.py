# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import numpy as np

sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

# classes = ["03040009", "03040014", "03040013", "03040024", "03040025", "03040015", "03040001", "03040005"]
# names = {
#     "03040009":	"常见均压环",
#     "03040014":	"均压环轻微歪斜",
#     "03040013":	"均压环严重歪斜",
#     "03040024":	"均压环支架破损",
#     "03040025": "均压环变形",       ####
#     "03040015":	"均压环严重破损",
#     "03040001":	"均压环",
#     "03040005": "均压环缺失"
# }


# 6
classes = ["03040009", "03040014", "03040013", "03040024", "03040025", "03040015", "03040001", "03040005", "02010002", "02010006"]
new_classes = ["03040009", "03040014", "03040024", "03040015", "03040005", "02010002"]
names = {
    "03040009":	"常见均压环",
    "03040014":	"均压环轻微歪斜",
    "03040024":	"均压环支架破损",
    "03040015":	"均压环严重破损",
    "03040005": "均压环缺失",
    "02010002": "绝缘子自爆", 
}

# classes: {
#     "03040009":	"常见均压环",
#     "03040014":	"均压环轻微歪斜",
#     # "03040013":	"均压环严重歪斜",
#     "03040024":	"均压环支架破损",
#     # "03040025": "均压环变形",       ####
#     "03040015":	"均压环严重破损",
#     # "03040001":	"均压环",
#     "03040005": "均压环缺失",
#     "02010002": "绝缘子自爆", 
#     # "02010006": "绝缘子自爆"
# }



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
    in_file = open('/data1/dataset_junyahuanqueshi/data/annotations/%s.xml' % (image_id), encoding="utf-8")
    out_file = open('/data1/dataset_junyahuanqueshi/dataset/train/labels/train2017/%s.txt' % image_id, 'w')
    
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
            flag = False
            if cls == "03040013":
                cls = "03040014"
            elif cls == "03040025" or cls == "03040001":
                cls = "03040009"
            elif cls == "02010006":
                cls = "02010002"

            cls_id = new_classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (np.float64(xmlbox.find('xmin').text),
                 np.float64(xmlbox.find('xmax').text),
                 np.float64(xmlbox.find('ymin').text),
                 np.float64(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    if flag is True:
        write_path.write('%s.xml' % image_id + ' ' + '\n')


if __name__ == "__main__":
    file_path = '/data1/dataset_junyahuanqueshi/data/annotations'
    if not os.path.exists('/data1/dataset_junyahuanqueshi/dataset/train/labels/train2017'):
        os.makedirs('/data1/dataset_junyahuanqueshi/dataset/train/labels/train2017')
    xml_list = os.listdir(file_path)
    for xml_file in xml_list:
        print('xml_file[:-4]', xml_file)
        convert_annotation(xml_file[:-4])