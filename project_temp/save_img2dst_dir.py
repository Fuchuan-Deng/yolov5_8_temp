# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import os
import shutil
import numpy as np


classes = ["03040009", "03040014", "03040013", "03040024", "03040025", "03040015", "03040001", "03040005"]


if __name__ == "__main__":
    file_path = ""         # 当前保存xml文件的文件夹路径
    dst_path = ""          # 想要保存xml文件的文件夹路径
    if not os.path.exists(dst_path):
        print("建立目标文件夹: "， dst_path)
        os.makedirs(dst_path)
    
    for cls in classes:
        path = os.path.join(dst_path, cls)
        if not os.path.exists(path):
            print("建立标签文件夹: "， path)
            os.makedirs(path)

    xml_list = glob.glob(os.path.join(file_path, "*.xml"))
    for i, xml_file in enumerate(xml_list):
        print(i, " / ", len(xml_list), xml_file)

        in_file = open(xml_file, encoding="utf-8")
        tree = ET.parse(in_file)
        root = tree.getroot()

        indexes = np.zeros(len(classes)).astype(np.int16)
        for obj in root.iter('object'):
            cls = obj.find('name').text
            
            if cls not in classes:
                continue
            elif cls in classes and indexes[classes.index(cls)] != 0:
                save_path = os.path.join(dst_path, cls)
                indexes[classes.index(cls)] = 1
                shutil.copy(xml_file, save_path)       # 复制到指定标签文件夹
                # shutil.move(xml_file, save_path)     # 剪切到指定标签文件夹