import json
import os
import argparse
from tqdm import tqdm
from collections import Counter
import cv2
import glob

###当前脚本能自动创建save-dir
classes = ["01010002", 
           "01010001", 
           "01010005", 
           "01010011", 
           "01010006", 
           "01010007",
           "01010018",
           "07040006"]
names = {"01010002":"断股", 
         "01010001":"散股", 
         "01010005":"悬垂线夹散股", 
         "01010011":"保护线", 
         "01010006":"保护线散股", 
         "01010007":"保护线断股",
         "01010018":"预绞丝",
         "07040006":"无效"}

# 断股 01010002 2264
# 悬垂线夹散股 01010005 1174
# 保护线 01010011 4065
# 保护线散股 01010006 591
# 散股 01010001 1130
# 预绞丝 01010018 519
# 无效 07040006 256
# 预绞丝01010018 224
# 保护线断股 01010007 327
# 悬垂线夹散股 01010005. 2
# 预绞丝 01010018. 3


def convert_label_json(json_dir, imgs_dir, save_dir, classes):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if not os.path.exists(os.path.join(save_dir, "01010002")):
        os.makedirs(os.path.join(save_dir, "01010002"))
    if not os.path.exists(os.path.join(save_dir, "01010001")):
        os.makedirs(os.path.join(save_dir, "01010001"))

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

        image_id = json_path.split(".")[0]
        img_file = glob.glob(os.path.join(imgs_dir, image_id + "*"))[0]

        image = cv2.imread(img_file, cv2.IMREAD_COLOR)
        if image is None:
            continue

        for i, shape_dict in enumerate(json_dict['shapes']):
            label = shape_dict['label']
            
            if "01010002" in label or "01010001" in label:
                if "01010002" in label:
                    label = "01010002"
                if "01010001" in label:
                    label = "01010001"
                name = names[label]

                dest_file = image_id + "_%03d.jpg" % i
                dest_file = os.path.join(save_dir, label, dest_file)

                points_w = []
                points_h = []
                points = shape_dict['points']
                for point in points:
                    points_w.append(point[0])
                    points_h.append(point[1])
                xmin, xmax, ymin, ymax = min(points_w), max(points_w), min(points_h), max(points_h)
                xmin, xmax, ymin, ymax = int(xmin), int(xmax), int(ymin), int(ymax)
                xmin, xmax, ymin, ymax = max(0, xmin), min(w, xmax), max(0, ymin), min(h, ymax)
                if xmax - xmin <= 0 or ymax - ymin <= 0:
                    continue
                
                sub_img = image[ymin:ymax, xmin:xmax]
                if sub_img.size == 0:
                    continue
                cv2.imwrite(dest_file, sub_img, [cv2.IMWRITE_JPEG_QUALITY, 100])
            # label_index = classes.index(label)
            # classes.append(shape_dict['label'])
            # points = shape_dict['points']
 
            # points_nor_list = []
 
            # for point in points:
            #     points_nor_list.append(point[0]/w)
            #     points_nor_list.append(point[1]/h)
 
            # points_nor_list = list(map(lambda x:str(x),points_nor_list))
            # points_nor_str = ' '.join(points_nor_list)
            
            # label_str = str(label_index) + ' ' +points_nor_str + '\n'
            # txt_file.writelines(label_str)
    # count = Counter(classes)
    # for k,v in count.items():
    #     print(k, v)
 
if __name__ == "__main__":
    """
    python json2txt_nomalize.py --json-dir my_datasets/color_rings/jsons --save-dir my_datasets/color_rings/txts --classes "cat,dogs"
    """

    json_dir = "/data1/dataset_duangusangu_seg/annotations"
    imgs_dir = "/data1/dataset_duangusangu_seg/images"
    save_dir = "/data1/dataset_duangusangu_seg/roi"
    convert_label_json(json_dir, imgs_dir, save_dir, classes)