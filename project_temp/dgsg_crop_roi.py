import os
import cv2
import glob
import xml.etree.ElementTree as ET
import pickle
from os import listdir, getcwd
from os.path import join
import numpy as np
from PIL import Image, ImageDraw, ImageFont


classes = ["01010001", "01010002", "01010005", "01010006", "01010007", "01010011"]
labels = ["散股", "断股", "悬垂线夹散股", "保护线散股", "保护线断股", "保护线"]


def cv2ImgAddText(img, text, left, top, textColor, textSize):
    if isinstance(img, np.ndarray):
        # import pdb;pdb.set_trace()
        img=Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    ttf = "./simhei.ttf"
    fontStyle = ImageFont.truetype(ttf, textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)


def draw_img(img_id, src_dir, dest_dir, xmin=0, xmax=0, ymin=0,ymax=0, crop=False, boxes=None, cls_ids=None):
    if boxes is not None and cls_ids is not None:
        path = glob.glob(os.path.join(src_dir, img_id + "*"))[0]
        image = cv2.imread(path, cv2.IMREAD_COLOR)
        textColor = (0, 0, 255)
        textSize = 30
        
        SrcImg = image[int(ymin):int(ymax), int(xmin):int(xmax)]
        
        for cls, box in zip(cls_ids, boxes):
            cv2.rectangle(SrcImg, (box[0], box[2]), (box[1], box[3]), (255, 0, 0), 2)
            text = labels[cls]
            left = int(box[0] + box[1]) / 2
            top = int(box[2] + box[3]) / 2
            SrcImg = cv2ImgAddText(SrcImg, text, left, top, textColor, textSize)
        dest_file = os.path.join(dest_dir, img_id + ".jpg")
        print(dest_file)
        cv2.imwrite(dest_file, SrcImg, [cv2.IMWRITE_JPEG_QUALITY, 100])



def augment_img(img_id, src_dir, dest_dir, xmin=0, xmax=0, ymin=0,ymax=0, mode=0, crop=False):
    path = glob.glob(os.path.join(src_dir, img_id + "*"))[0]
    image = cv2.imread(path, cv2.IMREAD_COLOR)

    if crop is True:
        image = image[int(ymin):int(ymax), int(xmin):int(xmax)]

    if mode == 0:
        # 原图
        file = img_id + ".jpg"
    elif mode == 1:
        # 左右翻转
        file = img_id + "_rl.jpg"
        image = image[:, ::-1]
    elif mode == 2:
        # 上下翻转
        file = img_id + "_ud.jpg"
        image = image[::-1, :]
    elif mode == 3:
        # 中心翻转
        file = img_id + "_ct.jpg"
        image = image[::-1, ::-1]

    w, h = image.shape[:2]
    if w > 2560 or h > 2560:
        image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    w, h = image.shape[:2]
    if w > 2560 or h > 2560:
        image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    
    dest_file = os.path.join(dest_dir, file)
    cv2.imwrite(dest_file, image, [cv2.IMWRITE_JPEG_QUALITY, 100])


def check(box):
    if (box[1] - box[0] == 0) or (box[3] - box[2] == 0):
        return False
    return True


def convert_boxes(size, boxes):

    def cx(box, dw):
        return ((box[0] + box[1]) / 2.0 - 1) * dw

    def cy(box, dh):
        return ((box[2] + box[3]) / 2.0 - 1) * dh
    
    def cw(box, dw):
        return (box[1] - box[0]) * dw

    def ch(box, dh):
        return (box[3] - box[2]) * dh

    dw = 1. / (size[0])
    dh = 1. / (size[1])
    new_boxes = [[cx(box, dw), cy(box, dh), cw(box, dw), ch(box, dh)] for box in boxes]
    return boxes


def compute(w, h, xmin, xmax, ymin, ymax):
    "compute new xmin, xmax, ymin, ymax"

    rate = 0.2

    nxmin = int((1 - rate) * xmin)
    nxmax = int((1 + rate) * xmax)
    nymin = int((1 - rate) * ymin)
    nymax = int((1 + rate) * ymax)

    if nxmax > h :
        nxmax = w
    
    if nymax > h:
        nymax = h
        
    nw = nxmax - nxmin
    nh = nymax - nymin

    if nw > nh:
        if nymin + nw > h:
            nymin = max(h - nw, 0)
            nymax = h
            nh = ymax - ymin
    else:
        if nxmin + nh > w:
            nxmin = max(w - nh, 0)
            nxmax = w
            nw = xmax - xmin

    return nw, nh, nxmin, nxmax, nymin, nymax
        

def convert_annotation(image_id, src_xml_path, dest_txt_path, src_img_dir, dst_img_dir, 
                       indexes, augment=[0,1,2,3], crop=False):

    in_file = open(os.path.join(src_xml_path, '%s.xml' % (image_id)), encoding="utf-8")

    # 这里根据自己的路径修改
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')

    w = int(size.find('width').text)
    h = int(size.find('height').text)
    if w == 0 or h == 0:
        return

    flag = True
    xmin = 1100000
    ymin = 1111111
    xmax = 0
    ymax = 0
    cls_ids = []
    boxes = []
    for i, obj in enumerate(root.iter('object')):
        cls = obj.find('name').text
        if cls not in classes:
            print(in_file, cls)
            continue
        elif cls in classes and i in indexes:
            flag = False
            cls_ids.append(classes.index(cls))
            xmlbox = obj.find('bndbox')
            boxes.append([float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), 
                          float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text)])

            if xmin > float(xmlbox.find('xmin').text):
                xmin = float(xmlbox.find('xmin').text)
            
            if xmax < float(xmlbox.find('xmax').text):
                xmax = float(xmlbox.find('xmax').text)

            if ymin > float(xmlbox.find('ymin').text):
                ymin = float(xmlbox.find('ymin').text)
                 
            if ymax < float(xmlbox.find('ymax').text):
                ymax = float(xmlbox.find('ymax').text)
            
    if flag is False:
        cls_ids = np.array(cls_ids, np.int16)
        boxes = np.array(boxes, np.float32)

        if crop is True:
            w, h, xmin, xmax, ymin, ymax = compute(w, h, xmin, xmax, ymin, ymax)
            boxes[:, :2] = boxes[:, :2] - xmin
            boxes[:, 2:] = boxes[:, 2:] - ymin
        
        draw_img(image_id, src_img_dir, dst_img_dir, xmin, xmax, ymin, ymax, crop=True, boxes=boxes, cls_ids=cls_ids)

        # 原始
        # out_file = open(os.path.join(dest_txt_path, '%s.txt' % image_id), 'w')
        # new_boxes = convert_boxes((w,h), boxes)
        # for cls_id, box in zip(cls_ids, new_boxes):
        #     out_file.write(str(cls_id) + " " + " ".join([str(a) for a in box]) + '\n')
        # augment_img(image_id, src_img_dir, dst_img_dir, xmin, xmax, ymin, ymax, 0, crop, new_boxes)


        # if augment is not None:
        #     if 1 in augment:
        #         out_file = open(os.path.join(dest_txt_path, '%s_rl.txt' % image_id), 'w')
        #         new_boxes = boxes

            #     new_boxes[:,:2] = new_boxes[:, :2] - w
            #     new_boxes = np.abs(new_boxes)
            #     new_boxes = [[box[1], box[0], box[2], box[3]] for box in new_boxes]
            #     new_boxes = np.array(new_boxes)
            #     new_boxes = convert_boxes((w,h), new_boxes)

            #     for cls_id, box in zip(cls_ids, new_boxes):
            #         out_file.write(str(cls_id) + " " + " ".join([str(a) for a in box]) + '\n')
            #     augment_img(image_id, src_img_dir, dst_img_dir, xmin, xmax, ymin, ymax, 1, crop)

            # if 2 in augment:
            #     out_file = open(os.path.join(dest_txt_path, '%s_ud.txt' % image_id), 'w')
            #     new_boxes = boxes

            #     new_boxes[:,2:] = new_boxes[:, 2:] - h
            #     new_boxes = np.abs(new_boxes)
            #     new_boxes = [[box[0], box[1], box[3], box[2]] for box in new_boxes]
            #     new_boxes = np.array(new_boxes)
            #     new_boxes = convert_boxes((w,h), new_boxes)

            #     for cls_id, box in zip(cls_ids, new_boxes):
            #         out_file.write(str(cls_id) + " " + " ".join([str(a) for a in box]) + '\n')
            #     augment_img(image_id, src_img_dir, dst_img_dir, xmin, xmax, ymin, ymax, 2, crop)

            # if 3 in augment:
            #     out_file = open(os.path.join(dest_txt_path, '%s_ct.txt' % image_id), 'w')
            #     new_boxes = boxes

            #     new_boxes[:,:2] = new_boxes[:, :2] - w
            #     new_boxes[:,2:] = new_boxes[:, 2:] - h
            #     new_boxes = np.abs(new_boxes)
            #     new_boxes = [[box[1], box[0], box[3], box[2]] for box in new_boxes]
            #     new_boxes = np.array(new_boxes)
            #     new_boxes = convert_boxes((w,h), new_boxes)

            #     for cls_id, box in zip(cls_ids, new_boxes):
            #         out_file.write(str(cls_id) + " " + " ".join([str(a) for a in box]) + '\n')
            #     augment_img(image_id, src_img_dir, dst_img_dir, xmin, xmax, ymin, ymax, 3, crop)



def get_name_index(shaixuan_path):
    names = {}
    files = os.listdir(shaixuan_path)
    for file in files:
        if file.split('.')[0][:10] not in list(names.keys()):
            names[file.split('.')[0][:10]] = []
        names[file.split('.')[0][:10]].append(int(file.split('.')[0][-3:]))
    return names


if __name__ == "__main__":
    src_img_dir = r"/data1/dataset_duangusuangu/shai/JPEGImages"
    dst_img_dir = r"/data1/dataset_duangusuangu/dataset/train/images/train2017"

    src_xml_path = r'/data1/dataset_duangusuangu/shai/Annotations'
    dst_txt_path = r'/data1/dataset_duangusuangu/dataset/train/labels/train2017'
    shaixuan_path = r"/data1/dataset_duangusuangu/shaixuan/shaixuan"

    if not os.path.join(dst_img_dir):
        os.makedirs(dst_img_dir)
    if not os.path.join(dst_txt_path):
        os.makedirs(dst_txt_path)

    names = get_name_index(shaixuan_path)

    xml_list = os.listdir(src_xml_path)
    for i, xml_file in enumerate(xml_list):
        # print('xml_file[:-4]', xml_file)
        print(i, len(xml_list), xml_file)
        convert_annotation(xml_file[:-4], 
                           src_xml_path, dst_txt_path, src_img_dir, dst_img_dir, 
                           names[xml_file[:-4]], crop=False)