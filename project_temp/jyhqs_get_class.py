import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
from collections import Counter
import glob

classes = ["03040009", "03040014", "03040013", "03040024", "03040025", "03040015", "03040001", "03040005", "02010002", "02010006"]
new_classes = ["03040009", "03040014", "03040024", "03040015", "03040005", "02010002"]
names = {
    "03040009":	"常见均压环",
    "03040014":	"均压环轻微歪斜",
    # "03040013":	"均压环严重歪斜",
    "03040024":	"均压环支架破损",
    # "03040025": "均压环变形",       ####
    "03040015":	"均压环严重破损",
    # "03040001":	"均压环",
    "03040005": "均压环缺失",
    "02010002": "绝缘子自爆", 
    # "02010006": "绝缘子自爆"
}
# 03040009 常见均压环 17931
# 03040014 均压环轻微歪斜 4685
# 03040005 均压环缺失 28259
# 02010002 绝缘子自爆 3578
# 03040015 均压环严重破损 353
# 03040024 均压环支架破损 611



def get_class(dir):
    # xml_list = os.listdir(dir)
    xml_list = glob.glob(os.path.join(dir,"*.xml"))
    clss = []

    for xml_file in xml_list:
        # file = os.path.join(dir, xml_file)

        in_file = open(xml_file, encoding="utf-8")
    
        # 这里根据自己的路径修改
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')

        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls == "03040013":
                cls = "03040014"
            elif cls == "03040025" or cls == "03040001":
                cls = "03040009"
            elif cls == "02010006":
                cls = "02010002"
            if cls in classes:
                clss.append(cls) 
    
    count = Counter(clss)
    for k,v in count.items():
        print(k, names[k], v)
    return

if __name__ == "__main__":
    file_path = r'/data1/dataset_junyahuanqueshi/data/annotations'
    get_class(file_path)