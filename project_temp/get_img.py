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


classes = ["01010001", "01010002", "01010005", "01010006", "01010007"]
names = ["散股", "断股", "悬垂线夹散股", "保护线散股", "保护线断股"]


def get_img(dir, imgs_path, save_path):
    xml_list = os.listdir(dir)
    classes = []

    for xml_file in xml_list:
        file = os.path.join(dir, xml_file)

        in_file = open(file, encoding="utf-8")
    
        # 这里根据自己的路径修改
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')

        flag = False
        for obj in root.iter('object'):
            cls = obj.find('name').text
            # if cls not in classes:
            if cls in names.keys():
                flag = True
                break
        if flag == True:
            filename = xml_file.split(".")[0]
            img_file = glob.glob(os.path.join(imgs_path, filename+ '*') )
            img_save = os.path.join(save_path, filename + '.jpg')
            image = cv2.imread(img_file[0], cv2.IMREAD_COLOR)
            cv2.imwrite(img_save, image, [cv2.IMWRITE_JPEG_QUALITY, 100])
    
    return

if __name__ == "__main__":
    file_path = r'/data1/dataset_jinjuxiushi/Annotations'
    imgs_path = r"/data1/dataset_jinjuxiushi/all"
    save_path = r"/data1/dataset_duangusuangu/val/images/train2017"
    get_img(file_path, imgs_path, save_path)

