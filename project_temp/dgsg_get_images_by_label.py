import os
import shutil
import glob


def get_images_by_label(label_dir, src_img_dir, dst_img_dir):
    files = os.listdir(label_dir)
    for file in files:
        name = file.split(".")[0]
        path = glob.glob(os.path.join(src_img_dir, name + "*"))[0]
        shutil.copy(path, dst_img_dir)
    return


if __name__ == "__main__":
    label_dir = "/data1/dataset_duangusuangu/train/labels/train2017"
    src_img_dir = "/data1/dataset_duangusuangu/shai/JPEGImages"
    dst_img_dir = "/data1/dataset_duangusuangu/train/images/train2017"

    get_images_by_label(label_dir, src_img_dir, dst_img_dir)