# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import cv2

sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = [
    '04010005', '02030006', '06020003', '01010008', '01020001',
    '03060011', '07010041', '07010043', '03060020', '03030007',
    '03060004', '03040026', '07010034', '07010035', '07010036',
    '07010037', '07010048', '07010038', '07010039', '07010046',
    '07010045', '07010050', '07010052', '07010054', '07010056',
    '07010057', '07010058', '07010059', '07010060', '07010061',
    '07010062', '07010063', '07010064', '07010065'
]

names = {
    '04010005':	'塔材锈蚀', 
    '02030006':	'陶瓷绝缘子锈蚀',
    '06020003':	'接地引下线锈蚀', 
    '01010008':	'导线锈蚀', 
    '01020001':	'拉线锈蚀', 
    '03060011':	'拉线金具锈蚀', 
    '07010041':	'耐张线夹锈蚀', 
    '07010043':	'T型线夹锈蚀', 
    '03060020':	'钢筋混凝土悬锤挂环锈蚀', 
    '03030007':	'防振锤锈蚀', 
    '03060004':	'悬垂直线夹锈蚀', 
    '03040026':	'均压环锈蚀', 
    '07010034':	'链条锈蚀',
    '07010035':	'拉线夹锈蚀', 
    '07010036':	'长夹片锈蚀', 
    '07010037':	'短夹片锈蚀', 
    '07010048':	'管道夹片锈蚀', 
    '07010038':	'直角挂板锈蚀', 
    '07010039':	'U型挂环锈蚀', 
    '07010046':	'并沟线夹锈蚀', 
    '07010045':	'金具三角板锈蚀', 
    '07010050':	'金具四角板锈蚀', 
    '07010052':	'金具蝶板锈蚀', 
    '07010054':	'金具长板锈蚀', 
    '07010056':	'金具短板锈蚀', 
    '07010057':	'螺栓螺帽锈蚀', 
    '07010058':	'重锤挂点锈蚀', 
    '07010059':	'绝缘子串钢帽锈蚀', 
    '07010060':	'放电间隙锈蚀', 
    '07010061':	'屏蔽环圆环锈蚀', 
    '07010062':	'避雷针锈蚀', 
    '07010063':	'调整板锈蚀', 
    '07010064':	'长间隔棒锈蚀', 
    '07010065':	'其他U型环锈蚀' 
}



def convert(image_id, imgs_dir, xmls_dir, save_dir):
    in_file = open(os.path.join(xmls_dir, '%s.xml' % (image_id)), encoding="utf-8")
    img_file = os.path.join(imgs_dir, '%s.jpg' % image_id)
    #这里根据自己的路径修改
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    if w == 0 or h == 0:
        return

    image = cv2.imread(img_file, cv2.IMREAD_COLOR)
    if image is None:
        return

    for i, obj in enumerate(root.iter('object')):
        cls = obj.find('name').text
        if cls not in list(names.keys()):
            continue
        else:
            name = names[cls]
            dest_file = image_id + "_" + name + "_%03d.jpg" % i
            dest_file = os.path.join(save_dir, dest_file)
            xmlbox = obj.find('bndbox')
            xmin = int(xmlbox.find('xmin').text)
            xmax = int(xmlbox.find('xmax').text)
            ymin = int(xmlbox.find('ymin').text)
            ymax = int(xmlbox.find('ymax').text)
            
            xmin = max(0, xmin)
            xmax = min(w, xmax)
            ymin = max(0, ymin)
            ymax = min(h, ymax)
            sub_img = image[ymin:ymax, xmin:xmax]
            if sub_img.size == 0:
                continue
            cv2.imwrite(dest_file, sub_img, [cv2.IMWRITE_JPEG_QUALITY, 100])
    return 


def read(imgs_dir, xmls_dir, save_dir):
    xmls_file = os.listdir(xmls_dir)
    for i, xml_file in enumerate(xmls_file):
        print(i, len(xmls_file))
        xml_name = xml_file.split('.')[0]
        convert(xml_name, imgs_dir, xmls_dir, save_dir)

if __name__ == "__main__":
    imgs_dir = "/data1/dataset_jinjuxiushi/dataset/images"
    xmls_dir = "/data1/dataset_jinjuxiushi/dataset/Annotations"
    save_dir = "/data1/dataset_jinjuxiushi/shaixuan"
    read(imgs_dir, xmls_dir, save_dir)

    


