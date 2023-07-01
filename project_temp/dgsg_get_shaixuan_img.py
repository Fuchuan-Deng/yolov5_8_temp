import os
import shutil
import glob
import cv2


def get_shaixuan(src_img_path, dst_img_path, dst_txt_path):
    files = os.listdir(dst_txt_path)
    names = []
    for file in files:
        name = file[:10]
        if name not in names:
            names.append(name)
            
    for i, name in enumerate(names):
        path = glob.glob(os.path.join(src_img_path, name + "*"))[0]
        image = cv2.imread(path, cv2.IMREAD_COLOR)
        wh = min(image.shape[:2])
        if wh > 2560 :
            image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

        wh = min(image.shape[:2])
        if wh > 2560 :
            image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

        path = os.path.join(dst_img_path, name + ".jpg")
        cv2.imwrite(path, image, [cv2.IMWRITE_JPEG_QUALITY, 100])
        print(i, len(names), path)
    return


if __name__ == "__main__":
    src_img_path = "/data1/dataset_duangusuangu/JPEGImages"
    dst_img_path = "/data1/dataset_duangusuangu/dataset/train/images/train2017"
    dst_txt_path = "/data1/dataset_duangusuangu/dataset/train/labels/train2017"

    if not os.path.exists(dst_img_path):
        os.makedirs(dst_img_path)

    get_shaixuan(src_img_path, dst_img_path, dst_txt_path)