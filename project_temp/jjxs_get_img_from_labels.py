import os
import shutil
import glob
import cv2


def get_images_by_label(label_dir, src_img_dir, dst_img_dir):
    files = os.listdir(label_dir)
    dst_files = os.listdir(dst_img_dir)

    now_files = []
    for d in dst_files:
        now_files.append(d.split(".")[0])

    for i, file in enumerate(files):
        name = file.split(".")[0]
        
        if name in now_files:
            continue
        print(i , len(files) - len(now_files), file)

        path = glob.glob(os.path.join(src_img_dir, name + "*"))[0]

        image = cv2.imread(path, cv2.IMREAD_COLOR)
        wh = max(image.shape[:2])
        if wh > 3840 :
            image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

        wh = max(image.shape[:2])
        if wh > 3840 :
            image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        dest_file = os.path.join(dst_img_dir, name + ".jpg")
        cv2.imwrite(dest_file, image, [cv2.IMWRITE_JPEG_QUALITY, 100])
    return


if __name__ == "__main__":
    label_dir = "/data1/dataset_jinjuxiushi/data_revise/train/labels/train2017"
    src_img_dir = "/data1/dataset_jinjuxiushi/dataset/images"
    dst_img_dir = "/data1/dataset_jinjuxiushi/data_revise/train/images/train2017"

    if not os.path.exists(dst_img_dir):
        os.makedirs(dst_img_dir)

    get_images_by_label(label_dir, src_img_dir, dst_img_dir)