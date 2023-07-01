# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import numpy as np
import os
import cv2
import glob
import xml.etree.ElementTree as ET
import pickle
from os import listdir, getcwd
from os.path import join
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import copy

sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["01010001", "01010002", "01010005", "01010006", "01010007", "01010011"]
class_names = {"01010001":"散股",
         "01010002":"断股", 
         "01010005":"悬垂线夹散股", 
         "01010006":"保护线散股",
         "01010007":"保护线断股",
         "01010011":"保护线"}

# 设置错误标签的log输出位置
write_path = open(r'./error.txt', 'w')


def cv2ImgAddText(img, text, left, top, textColor, textSize):
    if isinstance(img, np.ndarray):
        # import pdb;pdb.set_trace()
        img=Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    ttf = "./simhei.ttf"
    fontStyle = ImageFont.truetype(ttf, textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)


def draw_roi(img, dest_file, boxes, cls_ids):
    aug_img = copy.deepcopy(img)

    textColor = (0, 0, 255)
    textSize = 30
    boxes = np.array(boxes, np.int16)
    for cls, box in zip(cls_ids, boxes):
        cv2.rectangle(aug_img, (box[0], box[2]), (box[1], box[3]), (255, 0, 0), 3)
        text = cls
        left = int(box[0])
        top = int(box[2])
        aug_img = cv2ImgAddText(aug_img, text, left, top, textColor, textSize)
    print(dest_file)
    cv2.imwrite(dest_file, aug_img, [cv2.IMWRITE_JPEG_QUALITY, 100])


def augment(img, boxes, size, mode):
    w = size[0]
    h = size[1]
    crop_size = [w, h]

    # nw, nh 均由上面提供不更改
    aug_boxes = copy.deepcopy(boxes)
    aug_img = copy.deepcopy(img)

    if 0 == mode:
        # 上下翻转
        aug_img = cv2.flip(aug_img, 0)
        aug_boxes = [[box[0], box[1], crop_size[1] - box[3], crop_size[1] - box[2]] for box in aug_boxes]
    elif 1 == mode:
        # 左右翻转
        aug_img = cv2.flip(aug_img, 1)
        aug_boxes = [[crop_size[0] - box[1], crop_size[0] - box[0], box[2], box[3]] for box in aug_boxes]
    elif 2 == mode:
        # 对称翻转
        aug_img = cv2.flip(aug_img, -1)
        aug_boxes = [[crop_size[0] - box[1], crop_size[0] - box[0], crop_size[1] - box[3], crop_size[1] - box[2]] for box in aug_boxes]
    else:
        return None, None

    aug_boxes = np.array(aug_boxes)
    return aug_img, aug_boxes


# def change_hsv(img, value=0.2):
#     image = copy.deepcopy(img)
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     v = hsv[:, :, 2]
#     max_v = max(v)
#     if 255. / max_v < value + 1:
#         value =  255. / max_v - 1
    
#     rate = np.random.uniform(1 - value, 1 + value)
#     hsv[:, :, 2] = hsv[:, :, 2] * rate
#     hsv = np.array(hsv, np.uint8)
#     image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
#     return image


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


def get_name_index(shaixuan_path):
    names = {}
    files = os.listdir(shaixuan_path)
    for file in files:
        if file.split('.')[0][:10] not in list(names.keys()):
            names[file.split('.')[0][:10]] = []
        names[file.split('.')[0][:10]].append(int(file.split('.')[0][-3:]))
    return names


def compute_box_wh(new_boxes, crop_size, size, ranxy=200):
    w, h = size

    boxes = copy.deepcopy(new_boxes)

    xmin = min(boxes[:, 0])
    xmax = max(boxes[:, 1])
    ymin = min(boxes[:, 2])
    ymax = max(boxes[:, 3])

    center = [(xmax + xmin) / 2, (ymax + ymin) / 2]
    ran_x = np.random.randint(-ranxy, ranxy)
    ran_y = np.random.randint(-ranxy, ranxy)
    center[0] = center[0] + ran_x
    center[1] = center[1] + ran_y

    if center[0] - crop_size[0] / 2 < 0:
        xmin = 0
        xmax = crop_size[0]
    elif center[0] + crop_size[0] / 2 > w:
        xmin = w - crop_size[0]
        xmax = w - 1
    else:
        xmin = center[0] - crop_size[0] / 2
        xmax = center[0] + crop_size[0] / 2

    if center[1] - crop_size[1] / 2 < 0:
        ymin = 0
        ymax = crop_size[1]
    elif center[1] + crop_size[1] / 2 > h:
        ymin = h - crop_size[1]
        ymax = h - 1
    else:
        ymin = center[1] - crop_size[1] / 2
        ymax = center[1] + crop_size[1] / 2
            
    boxes = np.array(boxes, np.float32)
    for i in range(len(boxes)):
        if boxes[i, 1] > xmax:
            boxes[i, 1] = xmax
                    
        if boxes[i, 3] > ymax:
            boxes[i, 3] = ymax

    boxes[:, :2] = boxes[:, :2] - xmin
    boxes[:, 2:] = boxes[:, 2:] - ymin

    return boxes, xmin, xmax, ymin, ymax


def save_img_boxes(dst_txt_file, dst_img_file, img, box, cls_indexes):
    out_file = open(dst_txt_file, 'w')

    image = copy.deepcopy(img)
    boxes = copy.deepcopy(box)

    h, w = image.shape[:2]

    for b, cls_index in zip(boxes, cls_indexes):
        bb = convert((w, h), b)
        out_file.write(str(cls_index) + " " + " ".join([str(a) for a in bb]) + '\n')
    
    for i in range(3):
        wh = min(image.shape[:2])
        if wh > 2560:
            image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        else:
            break

    cv2.imwrite(dst_img_file, image, [cv2.IMWRITE_JPEG_QUALITY, 100])


def convert_annotation(src_xml_dir, dst_txt_dir, src_img_dir, dst_img_dir, names, epoches):
    xml_list = os.listdir(src_xml_dir)
    crop_size = [2000, 2000]
    count = 0
    
    for num, xml_file in enumerate(xml_list):
        print(num, len(xml_list), xml_file[:-4])
        image_id = xml_file[:-4]
        indexes = names[xml_file[:-4]]

        in_file = open(os.path.join(src_xml_dir, '%s.xml' % image_id), encoding="utf-8")
        # out_file = open(os.path.join(dst_txt_dir, '%s.txt' % image_id), 'w')
        #这里根据自己的路径修改
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        if w == 0 or h == 0:
            return

        flag = True
        boxes = []
        cls_ids = []
        cls_indexes = []
        for i, obj in enumerate(root.iter('object')):
            # difficult = obj.find('difficult').text
            flag = True
            if i in indexes:
                flag = False
                cls = obj.find('name').text
                cls_ids.append(class_names[cls])        # 汉字名称
                cls_indexes.append(classes.index(cls))  # 类序号
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text),
                     float(xmlbox.find('xmax').text),
                     float(xmlbox.find('ymin').text),
                     float(xmlbox.find('ymax').text))

                boxes.append(b)
        boxes = np.array(boxes, np.float32)
        xmin = min(boxes[:, 0])
        xmax = max(boxes[:, 1])
        ymin = min(boxes[:, 2])
        ymax = max(boxes[:, 3])

        path = glob.glob(os.path.join(src_img_dir, image_id + "*"))[0]
        image = cv2.imread(path, cv2.IMREAD_COLOR)

        # 原图
        # print("save image")
        dst_txt_file = os.path.join(dst_txt_dir, "%s.txt" % image_id)
        dst_img_file = os.path.join(dst_img_dir, "%s.jpg" % image_id)
        save_img_boxes(dst_txt_file, dst_img_file, image, boxes, cls_indexes)
        # draw_roi(image, dst_img_file, boxes, cls_ids)

        # print("save augment image")
        # 在原图的基础上加强
        for j in range(3):
            aug_img, aug_boxes = augment(image, boxes, (w, h), j)
            if aug_img is not None and aug_boxes is not None:
                dst_txt_file = os.path.join(dst_txt_dir, '%s_aug_%03d.txt' % (image_id, j))
                dst_img_file = os.path.join(dst_img_dir, "%s_aug_%03d.jpg" % (image_id, j))
                save_img_boxes(dst_txt_file, dst_img_file, aug_img, aug_boxes, cls_indexes)
                # draw_roi(aug_img, dst_img_file, aug_boxes, cls_ids)

        # 在原图的基础上调整亮度
        # for j in range(3):
        #     hsv_img = change_hsv(image)
        #     dst_txt_file = os.path.join(dst_txt_dir, '%s_hsv_%03d.txt' % (image_id, j))
        #     dst_img_file = os.path.join(dst_img_dir, "%s_hsv_%03d.jpg" % (image_id, j))
        #     save_img_boxes(dst_txt_file, dst_img_file, hsv_img, boxes, cls_indexes)
        
        # print("save roi")
        # 选择roi加强
        if max(xmax - xmin, ymax - ymin) < crop_size[0] and min(w,h) > crop_size[0]:
            # 计算roi内的新box和新长宽
            new_boxes, xmin, xmax, ymin, ymax = compute_box_wh(boxes, crop_size, (w, h))

            SrcImg = image[int(ymin):int(ymax), int(xmin):int(xmax)]

            dst_txt_file = os.path.join(dst_txt_dir, '%s_roi.txt' % image_id)
            dst_img_file = os.path.join(dst_img_dir, '%s_roi.jpg' % image_id)
            save_img_boxes(dst_txt_file, dst_img_file, SrcImg, new_boxes, cls_indexes)
            # draw_roi(SrcImg, dst_img_file, new_boxes, cls_ids)

             # 在roi上的基础上增强
            # print("save augment roi")
            for k in range(3):
                # nw, nh 均由上面提供不更改
                aug_img, aug_boxes = augment(SrcImg, new_boxes, crop_size, k)
                if aug_img is not None and aug_boxes is not None:
                    dst_txt_file = os.path.join(dst_txt_dir, '%s_roi_%02d.txt' % (image_id, k))
                    dst_img_file = os.path.join(dst_img_dir, "%s_roi_%02d.jpg" % (image_id, k))
                    save_img_boxes(dst_txt_file, dst_img_file, aug_img, aug_boxes, cls_indexes)
                    # draw_roi(aug_img, dst_img_file, aug_boxes, cls_ids)
        if flag is True:
            write_path.write('%s.xml' % image_id + ' ' + '\n')
        


if __name__ == "__main__":
    src_xml_dir = '/data1/dataset_duangusuangu/shai/Annotations'
    src_img_dir = "/data1/dataset_duangusuangu/JPEGImages"
    dst_img_dir = "/data1/dataset_duangusuangu/dataset/train/images/train2017"
    dst_txt_dir = "/data1/dataset_duangusuangu/dataset/train/labels/train2017"
    shaixuan_dir = "/data1/dataset_duangusuangu/shaixuan/shaixuan"

    epoches = 4

    if not os.path.exists(dst_txt_dir):
        os.makedirs(dst_txt_dir)

    if not os.path.exists(dst_img_dir):
        os.makedirs(dst_img_dir)

    names = get_name_index(shaixuan_dir)
    convert_annotation(src_xml_dir, dst_txt_dir, src_img_dir, dst_img_dir, names, epoches)

