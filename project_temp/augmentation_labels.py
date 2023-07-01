import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["32040006",
           "32040012",
           "32040014",
           "32040016",
           "32040011",
           "32040005",
           "32040013",
           "32040015"]
names = ["混合色硅胶",
         "金属锈蚀",
         "带铁壳的呼吸器-变色",
         "不带铁壳的呼吸器-变色",
         "呼吸器有裂纹",
         "纯色硅胶",
         "带铁壳的呼吸器-正常",
         "不带铁壳的呼吸器-正常"]

# 设置错误标签的log输出位置
write_path = open(r'./error.txt', 'w')


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


def convert_annotation(image_id, dir, dest_path):
    in_file = open(os.path.join(dir, '%s.xml' % (image_id)), encoding="utf-8")

    out_file = open(os.path.join(dest_path, '%s.txt' % image_id), 'w')
    out_file_h = open(os.path.join(dest_path, '%s_h.txt' % image_id), 'w')
    out_file_w = open(os.path.join(dest_path, '%s_w.txt' % image_id), 'w')
    out_file_hw = open(os.path.join(dest_path, '%s_hw.txt' % image_id), 'w')
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

    h_h = h - 50
    w_w = w - 50

    flag = True
    for obj in root.iter('object'):
        # difficult = obj.find('difficult').text
        cls = obj.find('name').text
        # if cls not in classes or int(difficult) == 1:
        #     continue
        # print(in_file)
        # 标签自查
        if cls not in classes:
            print(in_file, cls)
            continue
        else:
            flag = False
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text),
                 float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

            # 高度降低了50像素
            # image_right = image[50:, :]
            b_h = (float(xmlbox.find('xmin').text),
                 float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text) - 50,
                 float(xmlbox.find('ymax').text) - 50)
            bb = convert((w, h_h), b_h)
            out_file_h.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

            # 宽度降低了50像素
            b_w = (float(xmlbox.find('xmin').text) - 50,
                 float(xmlbox.find('xmax').text) - 50,
                 float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            bb = convert((w_w, h), b_w)
            out_file_w.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

            # 高度和宽度都降低了50像素
            b_hw = (float(xmlbox.find('xmin').text) - 50,
                 float(xmlbox.find('xmax').text) - 50,
                 float(xmlbox.find('ymin').text) - 50,
                 float(xmlbox.find('ymax').text) - 50)
            bb = convert((w_w, h_h), b_hw)
            out_file_hw.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

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


if __name__ == "__main__":
    file_path = r'./Annotations'
    dest_path = r'./train/labels/train2017'

    xml_list = os.listdir(file_path)
    for xml_file in xml_list:
        print('xml_file[:-4]', xml_file)
        convert_annotation(xml_file[:-4], file_path, dest_path)
