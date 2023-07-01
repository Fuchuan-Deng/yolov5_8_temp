import json
import os
import argparse
from tqdm import tqdm
from collections import Counter



# 拉线 291
# 裸导线 2006
# 导线 5278
# 导线-跳线 1247
# 地线 1181
# 地线-跳线 546
# 绝缘导线 395



def convert_label_json(json_dir, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    classes = []

    json_file_list=[]
    file_list = os.listdir(json_dir)
    for fl in file_list:
        if os.path.splitext(fl)[1]==".json":
            json_file_list.append(fl)
            
    for json_path in tqdm(json_file_list):
        path = os.path.join(json_dir,json_path)
        # print(json_path)
        with open(path,'r',encoding="utf-8") as load_f:
            json_dict = json.load(load_f)
        # h, w = json_dict['imageHeight'], json_dict['imageWidth']
 
        for shape_dict in json_dict['shapes']:
            classes.append(shape_dict['label'])

    count = Counter(classes)
    for k,v in count.items():
        print(k, v)
 
if __name__ == "__main__":
    json_dir = "/data1/dataset_duangusangu_seg/seg"
    save_dir = "/data1/dataset_duangusangu_seg/labels"
    convert_label_json(json_dir, save_dir)