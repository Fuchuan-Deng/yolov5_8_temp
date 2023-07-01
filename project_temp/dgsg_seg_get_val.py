import os
import shutil
import numpy as np
import glob


if __name__ == "__main__":
    src_img_dir = "/data1/dataset_duangusangu_seg/data/train/images/train2017"
    src_lbl_dir = "/data1/dataset_duangusangu_seg/data/train/labels/train2017"

    dst_img_dir = "/data1/dataset_duangusangu_seg/data/val/images/train2017"
    dst_lbl_dir = "/data1/dataset_duangusangu_seg/data/val/labels/train2017"

    if not os.path.exists(dst_img_dir):
        os.makedirs(dst_img_dir)

    if not os.path.exists(dst_lbl_dir):
        os.makedirs(dst_lbl_dir)

    rate = 0.1

    files = os.listdir(src_img_dir)
    num = int(rate * len(files))
    indexes = np.arange(len(files))

    np.random.shuffle(indexes)
    files = [files[indexes[i]] for i in range(len(files))]
    files = files[:num]
    for i, file in enumerate(files):
        filename = file[:-4]

        img_path = os.path.join(src_img_dir, file)
        shutil.move(img_path, dst_img_dir)

        label = glob.glob(os.path.join(src_lbl_dir, filename + "*"))[0]
        label_path = os.path.join(src_lbl_dir, label)
        shutil.move(label_path, dst_lbl_dir)

        print(i, len(files), img_path, label_path)
