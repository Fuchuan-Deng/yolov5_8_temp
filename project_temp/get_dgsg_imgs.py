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


classes = ["01010001", "01010002", "01010005", "01010006", "01010007", "07040006"]
names = ["散股", "断股", "悬垂线夹散股", "保护线散股", "保护线断股", "无效"]


def get_img(dir, imgs_path, save_path):
    xml_list = os.listdir(dir)
    classes = []

    for xml_file in xml_list:
        filename = xml_file.split(".")[0]
        img_file = glob.glob(os.path.join(imgs_path, filename+ '*') )
        shutil.copy(img_file[0], save_path)
    
    return

if __name__ == "__main__":
    file_path = r'/data1/dataset_duangusuangu/val/labels/train2017'
    imgs_path = r"/data1/dataset_jinjuxiushi/all"
    save_path = r"/data1/dataset_duangusuangu/val/images/train2017"
    get_img(file_path, imgs_path, save_path)

