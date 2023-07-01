# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import cv2

sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]


classes = ["03040009", "03040014", "03040013", "03040024", "03040025", "03040015", "03040001", "03040005"]
# names = {
#     '03040005':	'均压环缺失', 
#     '03040001':	'均压环'
# }

# names: [
#     "03040009", "03040014", "03040013", "03040024", "03040025", "03040015", "03040001", "03040005"
# ]


names = {
    "03040009":	"常见均压环",
    "03040014":	"均压环轻微歪斜",
    "03040013":	"均压环严重歪斜",
    "03040024":	"均压环支架破损",
    "03040025": "均压环变形",
    "03040015":	"均压环严重破损",
    "03040001":	"均压环",
    "03040005": "均压环缺失"
}




def convert(image_id, imgs_dir, xmls_dir, save_dir):
    in_file = open(os.path.join(xmls_dir, '%s.xml' % (image_id)), encoding="utf-8")
    img_file = os.path.join(imgs_dir, '%s.JPG' % image_id)
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
        if cls not in classes:
            continue
        else:
            name = names[cls]
            dir_path = os.path.join(save_dir, cls)
            dest_file = image_id + "_" + name + "_%03d.jpg" % i
            dest_file = os.path.join(dir_path, dest_file)
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
    imgs_dir = "/data1/dataset_junyahuanqueshi/data/images"
    xmls_dir = "/data1/dataset_junyahuanqueshi/data/annotations"
    save_dir = "/data1/dataset_junyahuanqueshi/data/fenlei"
    for cls in classes:
        dir_path = os.path.join(save_dir, cls)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    read(imgs_dir, xmls_dir, save_dir)

    


