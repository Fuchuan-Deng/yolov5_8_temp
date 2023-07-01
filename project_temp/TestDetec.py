# -*- coding: utf-8 -*-

import numpy as np
import sys
import os
import cv2
import time
import random
#from Common import XmlReadWrite
from dxai_detector import DxaiDetector
import glob
from PIL import Image, ImageDraw, ImageFont


def cv2ImgAddText(img, text, left, top, textColor, textSize):
    if isinstance(img, np.ndarray):
        # import pdb;pdb.set_trace()
        img=Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    ttf = "./simhei.ttf"
    fontStyle = ImageFont.truetype(ttf, textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)


if __name__ == "__main__":
    save_path = r'runs/test/results/'
    # save_path = r'result_dongfangzhan_kaiguan/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    # label_mark = ["zhen", 'other']

    det = DxaiDetector(0, 0)
    # model = det.network
    # #print(model)
    # for k, v in model.named_parameters():
    #    print(k,v.shape)

    labels = ["散股", "断股", "悬垂线夹散股", "保护线散股", "保护线断股"]

    files = glob.glob(r'/data1/dataset_duangusuangu/val1/images/train2017/*')

    c = 1
    for file in files:
        print(c, len(files))
        # print(file)
        SrcImg = cv2.imdecode(np.fromfile(file, dtype=np.uint8), 1)
        t1 = time.time()
        result = det.detect(SrcImg, 0)
        # print(result)
        # if result == []:
        #     c+=1
        #     continue
        if len(result) == 0:
            c += 1
            continue

        flag = False
        for item in result:
            # label = label_mark[int(item[-1])]
            label = labels[int(item[0])]
            xmin = int(round(item[1]))
            ymin = int(round(item[2]))
            xmax = int(round(item[3]))
            ymax = int(round(item[4]))
            conf = float(item[5])
            if conf < 0.3:
                continue
            else:
                flag = True
                print(xmin, ymin, xmax, ymax, label, conf)
        #        import pdb;pdb.set_trace()
                cv2.rectangle(SrcImg, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
                textColor = (0, 0, 255)
                textSize = 30
                text = label + str(conf)[:4]
                left = xmin
                top = ymin
                SrcImg = cv2ImgAddText(SrcImg, text, left, top, textColor, textSize)

            # cv2.putText(SrcImg, label+' '+str(conf)[:4], (xmin, ymin+70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        # cv2.imwrite(save_path + file.split('\\')[-1], SrcImg)
        if flag is True:
            cv2.imencode('.jpg', SrcImg)[1].tofile(save_path + file.split('/')[-1])
        c += 1

    





