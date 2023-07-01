# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
from collections import Counter
import shutil
import glob
import cv2


classes = [
    '04010005', '02030006', '06020003', '01010008', '01020001',
    '03060011', '07010041', '07010043', '03060020', '03030007',
    '03060004', '03040026', '07010034', '07010035', '07010036',
    '07010037', '07010048', '07010038', '07010039', '07010046',
    '07010045', '07010050', '07010052', '07010054', '07010056',
    '07010057', '07010058', '07010059', '07010060', '07010061',
    '07010062', '07010063', '07010064', '07010065'
]
names = ['塔材锈蚀', '陶瓷绝缘子锈蚀', '接地引下线锈蚀', '导线锈蚀', '拉线锈蚀', 
         '拉线金具锈蚀', '耐张线夹锈蚀', 'T型线夹锈蚀', '钢筋混凝土悬锤挂环锈蚀', '防振锤锈蚀', 
         '悬垂直线夹锈蚀', '均压环锈蚀', '链条锈蚀', '拉线夹锈蚀', '长夹片锈蚀', 
         '短夹片锈蚀',  '管道夹片锈蚀', '直角挂板锈蚀', 'U型挂环锈蚀', '并沟线夹锈蚀', 
         '金具三角板锈蚀', '金具四角板锈蚀', '金具蝶板锈蚀', '金具长板锈蚀', '金具短板锈蚀', 
         '螺栓螺帽锈蚀', '重锤挂点锈蚀', '绝缘子串钢帽锈蚀', '放电间隙锈蚀', '屏蔽环圆环锈蚀', 
         '避雷针锈蚀', '调整板锈蚀', '长间隔棒锈蚀', '其他U型环锈蚀' 
]



def get_name_index(shaixuan_path):
    names = {}
    files = os.listdir(shaixuan_path)
    for file in files:
        if file.split('.')[:6] not in list(names.keys()):
            names[file.split('.')[:6]] = []
        names[file.split('.')[:6]].append(file.split('.').split('.')[0][-3:])
    return names

def copy_image(yuanshi_path, save_path, names):
    for k in list(names.keys()):
        file = os.path.join(yuanshi_path, k + '.jpg')
        shutio.copy(file, save_path)
    return 


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


def convert_annotation(xml_path, save_txt_path, names):
    for filename in list(names.keys()):
        in_file = open(os.path.join(xml_path, '%s.xml' % filename, encoding="utf-8")
        out_file = open(os.path.join(save_txt_path,'%s.txt' % filename, 'w')

        indexes = names[filename]

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
            cls = obj.find('name').text
            if i not in indexes:
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
    shaixuan_path = r'/data1/dataset_jinjuxiushi/Annotations'
    img_path = r"/data1/dataset_jinjuxiushi/all"
    xml_path = r""
    save_img_path = r"/data1/dataset_duangusuangu/val"
    save_txt_path = r""

    names = get_name_index(shaixuan_path)
    copy_image(img_path, save_img_path, names)

    convert_annotation(xml_path, save_txt_path, names)