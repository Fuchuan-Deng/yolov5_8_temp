import os
import shutil
import numpy as np


def move(src_image_dir, dest_image_dir, src_label_dir, dest_label_dir):
    image_files = os.listdir(src_image_dir)
    label_files = os.listdir(src_label_dir)

    if len(image_files) == len(label_files):
        print("The length is right. And the length is ", len(image_files))

    img_files = []
    lbl_files = []
    for i in range(len(image_files)):
        img_files.append(image_files[i][:-4])
        lbl_files.append(label_files[i][:-4])

    imageFileLen = np.arange(len(image_files))
    np.random.shuffle(imageFileLen)

    image_files = [image_files[i] for i in imageFileLen]
    # label_files = [label_files[i] for i in imageFileLen]

    split = 0.9
    split_len = int(len(image_files) * split)
    img_test_files = image_files[split_len:]
    # lbl_files = label_files[split_len:]

    count = 0
    for img_file in img_test_files:
        if img_file[:-4] in img_files and img_file[:-4] in lbl_files:
            count = count + 1
            print("count: ", count)
            txt_file = img_file[:-4] + ".txt"
            src_image_file = os.path.join(src_image_dir, img_file)
            src_label_file = os.path.join(src_label_dir, txt_file)
            if os.path.exists(src_image_file) and os.path.exists(src_label_file):
                # print(src_image_file, "   to   ", dest_image_dir)
                # print(src_label_file, "   to   ", dest_label_dir)
                shutil.move(src_image_file, dest_image_dir)
                shutil.move(src_label_file, dest_label_dir)
    return


if __name__ == "__main__":
    src_image_dir = r"/data1/jinjuxiushi/train/images/train2017"
    dest_image_dir = r"/data1/jinjuxiushi/val/images/train2017"
    src_label_dir = r"/data1/jinjuxiushi/train/labels/train2017"
    dest_label_dir = r"/data1/jinjuxiushi/val/labels/train2017"
    move(src_image_dir, dest_image_dir, src_label_dir, dest_label_dir)
