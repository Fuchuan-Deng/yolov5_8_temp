import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
from collections import Counter
import numpy as np
import tqdm


classes = [
    '04010005', '02030006', '06020003', '01010008', '01020001',
    '03060011', '07010041', '07010043', '03030007',
    '03060004', '03040026', '07010034', '07010035', '07010036',
    '07010037', '07010048', '07010038', '07010039', '07010046',
    '07010045', '07010050', '07010052', '07010054', '07010056',
    '07010057', '07010058', '07010059', '07010060', '07010061',
    '07010062', '07010063', '07010064', '07010065'
]
names = {
    '04010005':	'塔材锈蚀', 
    '02030006':	'陶瓷绝缘子锈蚀',
    '06020003':	'接地引下线锈蚀', 
    '01010008':	'导线锈蚀', 
    '01020001':	'拉线锈蚀', 
    '03060011':	'拉线金具锈蚀', 
    '07010041':	'耐张线夹锈蚀', 
    '07010043':	'T型线夹锈蚀', 
    '03030007':	'防振锤锈蚀', 
    '03060004':	'悬垂直线夹锈蚀', 
    '03040026':	'均压环锈蚀', 
    '07010034':	'链条锈蚀',
    '07010035':	'拉线夹锈蚀', 
    '07010036':	'长夹片锈蚀', 
    '07010037':	'短夹片锈蚀', 
    '07010048':	'管道夹片锈蚀', 
    '07010038':	'直角挂板锈蚀', 
    '07010039':	'U型挂环锈蚀', 
    '07010046':	'并沟线夹锈蚀', 
    '07010045':	'金具三角板锈蚀', 
    '07010050':	'金具四角板锈蚀', 
    '07010052':	'金具蝶板锈蚀', 
    '07010054':	'金具长板锈蚀', 
    '07010056':	'金具短板锈蚀', 
    '07010057':	'螺栓螺帽锈蚀', 
    '07010058':	'重锤挂点锈蚀', 
    '07010059':	'绝缘子串钢帽锈蚀', 
    '07010060':	'放电间隙锈蚀', 
    '07010061':	'屏蔽环圆环锈蚀', 
    '07010062':	'避雷针锈蚀', 
    '07010063':	'调整板锈蚀', 
    '07010064':	'长间隔棒锈蚀', 
    '07010065':	'其他U型环锈蚀' 
}



def get_class(dir):
    xml_list = os.listdir(dir)
    counts = np.zeros(len(classes)).astype(np.int16)

    for i, xml_file in enumerate(xml_list):
        print(i, len(xml_list))
        file = os.path.join(dir, xml_file)
        in_file = open(file, encoding="utf-8")
    
        # 这里根据自己的路径修改
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        indexes = np.zeros(len(classes)).astype(np.int16)
        for obj in root.iter('object'):
            cls = obj.find('name').text
            # if cls not in classes:

            if cls in classes and indexes[classes.index(cls)] == 0:
                counts[classes.index(cls)] += 1
                indexes[classes.index(cls)] = 1
            
    for i in range(len(classes)):
        print(classes[i], names[classes[i]], counts[i])

    return

if __name__ == "__main__":
    file_path = r'/data1/dataset_jinjuxiushi/Annotations'
    get_class(file_path)