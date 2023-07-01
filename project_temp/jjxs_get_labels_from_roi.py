import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import numpy as np

sets = [('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = [
    '04010005', '02030006', '06020003', '01010008', '01020001',
    '03060011', '07010041', '07010043', '03030007', '03060004', 
    '03040026', '07010034', '07010035', '07010036', '07010037', 
    '07010048', '07010038', '07010039', '07010046', '07010045', 
    '07010050', '07010052', '07010054', '07010056', '07010057', 
    '07010058', '07010059', '07010060', '07010061', '07010062', 
    '07010063', '07010064', '07010065'
]
names = {
    '塔材锈蚀':	'04010005', 
    '陶瓷绝缘子锈蚀': '02030006',
    '接地引下线锈蚀':	'06020003', 
    '导线锈蚀':	'01010008', 
    '拉线锈蚀':	'01020001', 
    '拉线金具锈蚀': '03060011', 
    '耐张线夹锈蚀': '07010041', 
    'T型线夹锈蚀':	'07010043', 
    '防振锤锈蚀':	'03030007', 
    '悬垂直线夹锈蚀':'03060004'	, 
    '均压环锈蚀':	'03040026', 
    '链条锈蚀':	'07010034',
    '拉线夹锈蚀':	'07010035', 
    '长夹片锈蚀':	'07010036', 
    '短夹片锈蚀':	'07010037', 
    '管道夹片锈蚀':	'07010048', 
    '直角挂板锈蚀':	'07010038', 
    'U型挂环锈蚀':	'07010039', 
    '并沟线夹锈蚀':	'07010046', 
    '金具三角板锈蚀':	'07010045', 
    '金具四角板锈蚀':	'07010050', 
    '金具蝶板锈蚀':	'07010052', 
    '金具长板锈蚀':	'07010054', 
    '金具短板锈蚀':	'07010056', 
    '螺栓螺帽锈蚀':	'07010057', 
    '重锤挂点锈蚀':	'07010058', 
    '绝缘子串钢帽锈蚀':	'07010059', 
    '放电间隙锈蚀':	'07010060', 
    '屏蔽环圆环锈蚀':	'07010061', 
    '避雷针锈蚀':	'07010062', 
    '调整板锈蚀':	'07010063', 
    '长间隔棒锈蚀':	'07010064', 
    '其他U型环锈蚀':	 '07010065'
}


# 设置错误标签的log输出位置
write_path = open(r'/data1/dataset_jinjuxiushi/error.txt', 'w')

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


def convert_annotation(annotations, data, infos):
    for filename in list(infos.keys()):
        indexes = np.array(infos[filename], np.int16)

        clsss = indexes[:, 0].tolist()
        idxes = indexes[:, 1].tolist()
        print(idxes, clsss)

        in_file = open(os.path.join(annotations, '%s.xml' % filename), encoding="utf-8")
        path = os.path.join(data, "%s.txt" % filename)
        print(path)
        out_file = open(path, 'w')

        #这里根据自己的路径修改
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        if w == 0 or h == 0:
            return

        flag = True
        for i, obj in enumerate(root.iter('object')):
            # difficult = obj.find('difficult').text
            if i in idxes:
                cls_id = clsss[idxes.index(i)]
                flag = False
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text),
                     float(xmlbox.find('xmax').text),
                     float(xmlbox.find('ymin').text),
                     float(xmlbox.find('ymax').text))
                bb = convert((w, h), b)
                out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

        if flag is True:
            write_path.write('%s.xml' % filename + ' ' + '\n')


if __name__ == "__main__":
    annotations = '/data1/dataset_jinjuxiushi/dataset/Annotations'
    shaixuan = "/data1/dataset_jinjuxiushi/xiushi_all"
    data = "/data1/dataset_jinjuxiushi/data_revise/train/labels/train2017"

    if not os.path.exists(data):
        os.makedirs(data)
        print("build target data directory.")
    
    files = os.listdir(shaixuan)
    infos = {}
    for file in files:
        filename = file[:7]
        cl = names[file[8:-8]]
        index = int(file[-7:-4])

        if cl in classes:
            cls_id = classes.index(cl)
            if filename not in list(infos.keys()):
                infos[filename] = []
            infos[filename].append([cls_id, index])

    convert_annotation(annotations, data, infos)

    # dirs = os.listdir(shaixuan)
    # for i, dir in enumerate(dirs):
    #     file_indexes = []
    #     # print(i, len(dirs), dir)
    #     cls = dir
    #     if cls in classes:
    #         files = os.listdir(os.path.join(shaixuan, dir))

    #         for file in files:
    #             filename = file[:7]
    #             index = int(file.split(".")[0][-3:])
    #             file_indexes.append([filename, index])
            
    #         convert_annotation(annotations, data, cls, file_indexes)
