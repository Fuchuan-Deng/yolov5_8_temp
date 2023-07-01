import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import cv2
import glob

sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]


classes = ["40011004", "40011005", "40030001", "40041021", "40041022", "40011006"]  # class names
names = {
    "40011004":"陶瓷支柱式瓷绝缘子",  
    "40011005":"陶瓷针式瓷绝缘子", 
    "40030001":"复合绝缘子", 
    "40041021":"陶瓷支柱式瓷绝缘子顶", 
    "40041022":"针式绝缘子顶", 
    "40011006":"陶瓷悬式瓷绝缘子"}




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
            ctr_x = int((xmin+xmax)/2)
            ctr_y = int((ymin+ymax)/2)
            wh = max((xmax -xmin), (ymax-ymin))
            wh = int(wh / 2)
            sub_img = image[ctr_y-wh:ctr_y+wh, ctr_x-wh:ctr_x+wh]
            if sub_img.size == 0:
                continue
            cv2.imwrite(dest_file, sub_img, [cv2.IMWRITE_JPEG_QUALITY, 100])
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
    save_dir = "/data1/dataset_zhenshijueyuanzi/fenlei"
    for cls in classes:
        dir_path = os.path.join(save_dir, cls)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    read(imgs_dir, xmls_dir, save_dir)

    


