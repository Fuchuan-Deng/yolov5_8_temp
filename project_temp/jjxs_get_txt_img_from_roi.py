import os
import shutil
import glob
import cv2
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import numpy as np
import numpy as np
import sys
import os
import cv2
import time
import random
#from Common import XmlReadWrite
import glob
from PIL import Image, ImageDraw, ImageFont


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

def cv2ImgAddText(img, text, left, top, textColor, textSize):
    if isinstance(img, np.ndarray):
        # import pdb;pdb.set_trace()
        img=Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    ttf = "./simhei.ttf"
    fontStyle = ImageFont.truetype(ttf, textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)


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


def convert_annotation(src_xml_dir, dst_txt_dir, src_img_dir, dst_img_dir, all):
    draw_dir = "/data1/dataset_jinjuxiushi/data_revise/new_train/draw"
    if not os.path.exists(draw_dir):
        os.makedirs(draw_dir)

    for i, filename in enumerate(all.keys()):
        print(i, len(all.keys()))
        clses = all[filename][0]
        indexes = all[filename][1]

        in_file = open(os.path.join(src_xml_dir, '%s.xml' % filename), encoding="utf-8")
        
        txt_path = os.path.join(dst_txt_dir, "%s.txt" % filename)
        out_file = open(txt_path, 'w')

        img_path = os.path.join(src_img_dir, "%s.jpg" % filename)
        # SrcImg = cv2.imread(img_path, cv2.IMREAD_COLOR)

        # textColor = (0, 0, 255)
        # textSize = 30

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
            if i in indexes:
                cls_id = classes.index(clses[indexes.index(i)])
                flag = False
                xmlbox = obj.find('bndbox')
                xmin = int(xmlbox.find('xmin').text)
                xmax = int(xmlbox.find('xmax').text)
                ymin = int(xmlbox.find('ymin').text)
                ymax = int(xmlbox.find('ymax').text)

                b = (float(xmlbox.find('xmin').text),
                     float(xmlbox.find('xmax').text),
                     float(xmlbox.find('ymin').text),
                     float(xmlbox.find('ymax').text))

                bb = convert((w, h), b)
                out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
                
                # cv2.rectangle(SrcImg, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
                # text = names[clses[indexes.index(i)]]
                # left = xmin
                # top = ymin
                # SrcImg = cv2ImgAddText(SrcImg, text, left, top, textColor, textSize)

        # cv2.imwrite(os.path.join(draw_dir, filename + ".jpg"), SrcImg, [cv2.IMWRITE_JPEG_QUALITY, 100])
        if flag is True:
            write_path.write('%s.xml' % filename + ' ' + '\n')


def get_images_by_label(label_dir, src_img_dir, dst_img_dir):
    files = os.listdir(label_dir)
    dst_files = os.listdir(dst_img_dir)

    now_files = []
    for d in dst_files:
        now_files.append(d.split(".")[0])

    for i, file in enumerate(files):
        name = file.split(".")[0]
        
        if name in now_files:
            continue
        print(i , len(files) - len(now_files), file)

        path = glob.glob(os.path.join(src_img_dir, name + "*"))[0]

        image = cv2.imread(path, cv2.IMREAD_COLOR)
        w, h = image.shape[:2]
        if w > 2000 and h > 2000:
            image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

        w, h = image.shape[:2]
        if w > 2000 and h > 2000:
            image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        
        w, h = image.shape[:2]
        if w > 2000 and h > 2000:
            image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

        dest_file = os.path.join(dst_img_dir, name + ".jpg")
        cv2.imwrite(dest_file, image, [cv2.IMWRITE_JPEG_QUALITY, 100])
    return
        


if __name__ == "__main__":
    src_img_dir = "/data1/dataset_jinjuxiushi/dataset/images"
    dst_img_dir = "/data1/dataset_jinjuxiushi/data_revise/new_train/images/train2017"
    src_xml_dir = '/data1/dataset_jinjuxiushi/dataset/Annotations'
    dst_txt_dir = "/data1/dataset_jinjuxiushi/data_revise/new_train/labels/train2017"

    shaixuan = "/data1/dataset_jinjuxiushi/yishaixuan"

    if not os.path.exists(dst_img_dir):
        os.makedirs(dst_img_dir)
    if not os.path.exists(dst_txt_dir):
        os.makedirs(dst_txt_dir)

    dirs = os.listdir(shaixuan)
    file_indexes = []
    for i, dir in enumerate(dirs):
        # print(i, len(dirs), dir)
        cls = dir
        # print(cls)
        if cls in classes:
            files = os.listdir(os.path.join(shaixuan, dir))
            for file in files:
                filename = file[:7]
                index = int(file.split(".")[0][-3:])
                file_indexes.append([filename, cls, index])
    print(len(file_indexes))
    
    all = {}
    for file_index in file_indexes:
        filename = file_index[0]
        cls = file_index[1]
        index = file_index[2]

        if filename not in all.keys():
            all[filename] = [[], []]
        all[filename][0].append(cls)
        all[filename][1].append(index)
    print(len(all.keys()))

    convert_annotation(src_xml_dir, dst_txt_dir, src_img_dir, dst_img_dir, all)
    get_images_by_label(dst_txt_dir, src_img_dir, dst_img_dir)