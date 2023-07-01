import os
import shutil
import numpy as np
import glob


if __name__ == "__main__":
    src_img_dir = "/data1/dataset_jinjuxiushi/val/images/train2017"
    src_lbl_dir = "/data1/dataset_jinjuxiushi/val/labels/train2017"

    dst_img_dir = "/data1/dataset_jinjuxiushi/train/images/train2017"
    dst_lbl_dir = "/data1/dataset_jinjuxiushi/train/labels/train2017"

    rate = 0.75

    files = os.listdir(src_img_dir)
    num = int(rate * len(files))
    files = files[:num]
    for file in files:
        filename = file[:7]

        img_path = os.path.join(src_img_dir, file)
        shutil.move(img_path, dst_img_dir)

        label = glob.glob(os.path.join(src_lbl_dir, filename + "*"))[0]
        label_path = os.path.join(src_lbl_dir, label)
        shutil.move(label_path, dst_lbl_dir)

        print(img_path, label_path)