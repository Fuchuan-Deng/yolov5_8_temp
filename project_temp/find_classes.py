# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join


def convert_annotation(image_id):
    in_file = open('/data1/dataset_damenxiangmen/Annotations/%s.xml' % (image_id), encoding="utf-8")
    tree = ET.parse(in_file)
    root = tree.getroot()

    classes = []
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            classes.append(cls)
    print(classes)


if __name__ == "__main__":
    file_path = '/data1/dataset_damenxiangmen/Annotations'

    xml_list = os.listdir(file_path)
    for xml_file in xml_list:
        print('xml_file[:-4]', xml_file)
        convert_annotation(xml_file[:-4])