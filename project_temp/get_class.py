import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
from collections import Counter

names = {
    '01010001':'散股',	 
    '01010002':'断股',
}



def get_class(dir):
    xml_list = os.listdir(dir)
    classes = []

    for xml_file in xml_list:
        file = os.path.join(dir, xml_file)

        in_file = open(file, encoding="utf-8")
    
        # 这里根据自己的路径修改
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')

        for obj in root.iter('object'):
            cls = obj.find('name').text
            # if cls not in classes:
            classes.append(cls)
    
    count = Counter(classes)
    for k,v in count.items():
        if k in names.keys():
            print(names[k], v)
    return

if __name__ == "__main__":
    file_path = r'/data1/dataset_jinjuxiushi/Annotations'
    get_class(file_path)