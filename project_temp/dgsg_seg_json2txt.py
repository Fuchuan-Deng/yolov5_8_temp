import json
import os
import argparse
from tqdm import tqdm

###当前脚本能自动创建save-dir
classes = [
    "散股 01010001", 
    "断股 01010002", 
    "悬垂线夹散股 01010005", 
    "保护线散股 01010006", 
    "保护线断股 01010007",
    "保护线 01010011", 
    "预绞丝 01010018",
    "跳线断股 01010021",
    "跳线散股 01010022",
    "导线",
    "导线-跳线",
    "地线",
    "地线-跳线",
    "绝缘导线",
    "拉线",
    "无效 07040006"
]

nc = 16
# 散股 01010001 370
# 断股 01010002 1643
# 悬垂线夹散股 01010005 1183
# 保护线散股 01010006 608
# 保护线断股 01010007 327
# 保护线 01010011 4078
# 预绞丝 01010018 748
# 跳线断股 01010021 426    # 跳线断股01010021 184
# 跳线散股01010022 233   # 跳线散股 01010022 509
# 导线 5278       # 裸导线 2006
# 导线-跳线 1247
# 地线 1181
# 地线-跳线 546
# 绝缘导线 395 
# 拉线 291
# 无效 07040006 257

names = {
    "01010001":"散股",         # 370
    "01010002":"断股",         # 1643
    "01010005":"悬垂线夹散股",  # 1183
    "01010006":"保护线散股",   # 608
    "01010007":"保护线断股",   # 327
    "01010011":"保护线",       # 4078
    "01010018":"预绞丝",       # 748
    "01010021":"跳线断股",     # 610
    "01010022":"跳线散股",     # 724
    "01010023":"导线",
    "01010024":"导线-跳线",
    "01010025":"地线",
    "01010026":"地线-跳线",
    "01010027":"绝缘导线", 
    "01020003":"拉线",
    "07040006":"无效"         # 257
}


def convert_label_json(json_dir, save_dir, classes):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    json_file_list=[]
    file_list = os.listdir(json_dir)
    for fl in file_list:
        if os.path.splitext(fl)[1]==".json":
            json_file_list.append(fl)
            
    for json_path in tqdm(json_file_list):
        
        path = os.path.join(json_dir,json_path)
        with open(path,'r',encoding="utf-8") as load_f:
            json_dict = json.load(load_f)
        h, w = json_dict['imageHeight'], json_dict['imageWidth']

        txt_path = os.path.join(save_dir, json_path.replace('json', 'txt'))
        txt_file = open(txt_path, 'w')
 
        for shape_dict in json_dict['shapes']:
            label = shape_dict['label']
            if label == "跳线断股01010021":
                label = "跳线断股 01010021"
            elif label == "跳线散股01010022":
                label = "跳线散股 01010022"
            elif label == "裸导线":
                label = "导线"
            
            if label not in classes:
                continue

            label_index = classes.index(label)
            points = shape_dict['points']
 
            points_nor_list = []
 
            for point in points:
                points_nor_list.append(point[0]/w)
                points_nor_list.append(point[1]/h)
 
            points_nor_list = list(map(lambda x:str(x),points_nor_list))
            points_nor_str = ' '.join(points_nor_list)
            
            label_str = str(label_index) + ' ' +points_nor_str + '\n'
            txt_file.writelines(label_str)
 
if __name__ == "__main__":
    json_dir = "/data1/dataset_duangusangu_seg/annotations"
    save_dir = "/data1/dataset_duangusangu_seg/data/train/labels/train2017"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    convert_label_json(json_dir, save_dir, classes)