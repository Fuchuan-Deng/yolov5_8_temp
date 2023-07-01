import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

# classes = ["01010001", "01010002", "01010005", "01010006", "01010007"]
# names = ["散股", "断股", "悬垂线夹散股", "保护线散股", "保护线断股"]
classes = ["01010001", "01010002", "01010005", "01010006", "01010007", "01010011"]
# names = ["散股",      "断股",   "悬垂线夹散股", "保护线散股", "保护线断股", "保护线", "无效"]
names = {"01010001":"散股",
         "01010002":"断股", 
         "01010005":"悬垂线夹散股", 
         "01010006":"保护线散股",
         "01010007":"保护线断股",
         "01010011":"保护线"}

# 设置错误标签的log输出位置
write_path = open(r'./error.txt', 'w')


def check(box):
    if (box[1] - box[0] == 0) or (box[3] - box[2] == 0):
        return False
    return True


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id, dir, dest_path, indexes):
    in_file = open(os.path.join(dir, '%s.xml' % (image_id)), encoding="utf-8")

    move_pixel = 100

    out_file = open(os.path.join(dest_path, '%s.txt' % image_id), 'w')
    # out_file_h = open(os.path.join(dest_path, '%s_h.txt' % image_id), 'w')
    # out_file_w = open(os.path.join(dest_path, '%s_w.txt' % image_id), 'w')
    # out_file_hw = open(os.path.join(dest_path, '%s_hw.txt' % image_id), 'w')
    out_file_rl = open(os.path.join(dest_path, '%s_rl.txt' % image_id), 'w')
    out_file_ud = open(os.path.join(dest_path, '%s_ud.txt' % image_id), 'w')
    out_file_ct = open(os.path.join(dest_path, '%s_ct.txt' % image_id), 'w')

    # 这里根据自己的路径修改
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')

    w = int(size.find('width').text)
    h = int(size.find('height').text)
    if w == 0 or h == 0:
        return

    flag = True
    for i, obj in enumerate(root.iter('object')):
        cls = obj.find('name').text
        if cls not in classes:
            print(in_file, cls)
            continue
        elif cls in classes and i in indexes:
            flag = False
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text),
                 float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

            # 左右翻转
            b_rl = (w - float(xmlbox.find('xmax').text),
                    w - float(xmlbox.find('xmin').text),
                    float(xmlbox.find('ymin').text),
                    float(xmlbox.find('ymax').text))
            bb = convert((w, h), b_rl)
            out_file_rl.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

            # 上下翻转
            b_ud = (float(xmlbox.find('xmin').text),
                    float(xmlbox.find('xmax').text),
                    h - float(xmlbox.find('ymax').text),
                    h - float(xmlbox.find('ymin').text))
            bb = convert((w, h), b_ud)
            out_file_ud.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

            # 中心翻转
            b_ct = (w - float(xmlbox.find('xmax').text),
                    w - float(xmlbox.find('xmin').text),
                    h - float(xmlbox.find('ymax').text),
                    h - float(xmlbox.find('ymin').text))
            bb = convert((w, h), b_ct)
            out_file_ct.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    if flag is True:
        write_path.write('%s.xml' % image_id + ' ' + '\n')


def get_name_index(shaixuan_path):
    names = {}
    files = os.listdir(shaixuan_path)
    for file in files:
        if file.split('.')[0][:10] not in list(names.keys()):
            names[file.split('.')[0][:10]] = []
        names[file.split('.')[0][:10]].append(int(file.split('.')[0][-3:]))
    return names


if __name__ == "__main__":
    file_path = r'/data1/dataset_duangusuangu/shai/Annotations'
    dest_path = r'/data1/dataset_duangusuangu/train1/labels/train2017'
    shaixuan_path = r"/data1/dataset_duangusuangu/shaixuan/shaixuan"

    names = get_name_index(shaixuan_path)

    xml_list = os.listdir(file_path)
    for xml_file in xml_list:
        print('xml_file[:-4]', xml_file)
        convert_annotation(xml_file[:-4], file_path, dest_path, names[xml_file[:-4]])
