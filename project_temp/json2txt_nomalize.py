import json
import os
import argparse
from tqdm import tqdm

###当前脚本能自动创建save-dir

def convert_label_json(json_dir, save_dir, classes):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    classes = classes.split(',')

    json_file_list=[]
    file_list = os.listdir(json_dir)
    for fl in file_list:
        if os.path.splitext(fl)[1]==".json":
            json_file_list.append(fl)
    #print("json_file_list",json_file_list)
            
    for json_path in tqdm(json_file_list):
    # for json_path in json_paths:
        
        path = os.path.join(json_dir,json_path)
        # print("path",path)
        with open(path,'r',encoding="utf-8") as load_f:
            json_dict = json.load(load_f)
        h, w = json_dict['imageHeight'], json_dict['imageWidth']
 
        # save txt path
        txt_path = os.path.join(save_dir, json_path.replace('json', 'txt'))
        txt_file = open(txt_path, 'w')
 
        for shape_dict in json_dict['shapes']:
            label = shape_dict['label']
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
    """
    python json2txt_nomalize.py --json-dir my_datasets/color_rings/jsons --save-dir my_datasets/color_rings/txts --classes "cat,dogs"
    """
    # parser = argparse.ArgumentParser(description='json convert to txt params')
    # parser.add_argument('--json-dir', type=str, help='json path dir')
    # parser.add_argument('--save-dir', type=str, help='txt save dir')
    # parser.add_argument('--classes', type=str, help='classes')
    # args = parser.parse_args()
    json_dir = args.json_dir
    save_dir = args.save_dir
    classes = args.classes
    convert_label_json(json_dir, save_dir, classes)