import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import cv2
import glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]


classes = ["40011004", "40011005", "40030001", "40041021", "40041022", "40011006"]  # class names
names = {
    "40011004":"陶瓷支柱式瓷绝缘子",  
    "40011005":"陶瓷针式瓷绝缘子", 
    "40030001":"复合绝缘子", 
    "40041021":"陶瓷支柱式瓷绝缘子顶", 
    "40041022":"针式绝缘子顶", 
    "40011006":"陶瓷悬式瓷绝缘子"}


def cv2ImgAddText(img, text, left, top, textColor, textSize):
    if isinstance(img, np.ndarray):
        # import pdb;pdb.set_trace()
        img=Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    ttf = "./simhei.ttf"
    fontStyle = ImageFont.truetype(ttf, textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)


def convert(image_id, imgs_dir, xmls_dir, save_dir):
    in_file = open(os.path.join(xmls_dir, '%s.xml' % (image_id)), encoding="utf-8")
    # img_file = os.path.join(imgs_dir, '%s.JPG' % image_id)
    img_file = glob.glob(os.path.join(imgs_dir, image_id + "*"))[0]
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
    
    flag = False
    for i, obj in enumerate(root.iter('object')):
        cls = obj.find('name').text
        if cls != "40011005" and cls != "40041022":
            continue
        else:
            flag = True
            # name = names[cls]
            if cls == "40011005":
                color = (255, 0, 0)
            elif cls == "40041022":
                color = (0, 0, 255)

            xmlbox = obj.find('bndbox')
            xmin = int(xmlbox.find('xmin').text)
            xmax = int(xmlbox.find('xmax').text)
            ymin = int(xmlbox.find('ymin').text)
            ymax = int(xmlbox.find('ymax').text)

            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 5)
            textColor = color
            textSize = 30
            # text = name
            left = xmin
            top = ymin
            # image = cv2ImgAddText(image, text, left, top, textColor, textSize)
    if flag == True:
        dest_file = image_id + ".jpg"
        dest_file = os.path.join(save_dir, dest_file)
        cv2.imwrite(dest_file, image, [cv2.IMWRITE_JPEG_QUALITY, 100])
    return 


def read(imgs_dir, xmls_dir, save_dir):
    xmls_file = os.listdir(xmls_dir)
    for i, xml_file in enumerate(xmls_file):
        print(i, len(xmls_file))
        xml_name = xml_file[:-4]
        convert(xml_name, imgs_dir, xmls_dir, save_dir)

if __name__ == "__main__":
    imgs_dir = "/data1/dataset_zhenshijueyuanzi/JPEGImages"
    xmls_dir = "/data1/dataset_zhenshijueyuanzi/Annotations"
    save_dir = "/data1/dataset_zhenshijueyuanzi/testimg"
    # for cls in classes:
    #     dir_path = os.path.join(save_dir, cls)
    #     if not os.path.exists(dir_path):
    #         os.makedirs(dir_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    read(imgs_dir, xmls_dir, save_dir)