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



def get_img(dir, imgs_path, save_path):
    xml_list = os.listdir(dir)
    classes = []
    error_txt = []

    for i, xml_file in enumerate(xml_list):
        print(i, "/", len(xml_list))
        filename = xml_file.split(".")[0]
        img_file = glob.glob(os.path.join(imgs_path, filename+ '*') )
        image = cv2.imread(img_file[0], cv2.IMREAD_COLOR)
        if image is not None:
            w, h = image.shape[:2]
            if w > 4000 or h > 4000:
                image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

            w, h = image.shape[:2]
            if w > 4000 or h > 4000:
                image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            path = os.path.join(save_path, filename + ".jpg")
            cv2.imwrite(path, image, [cv2.IMWRITE_JPEG_QUALITY, 100])
        else:
            error_txt.append(xml_file)

    for txt in error_txt:
        print(txt)
    
    return


# 326 / 15823 07758.txt
# 327 / 15823
# 

if __name__ == "__main__":
    file_path = r'/data1/dataset_junyahuanqueshi/dataset/train/labels/train2017'
    imgs_path = r"/data1/dataset_junyahuanqueshi/data/images"
    save_path = r"/data1/dataset_junyahuanqueshi/dataset/train/images/train2017"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    get_img(file_path, imgs_path, save_path)