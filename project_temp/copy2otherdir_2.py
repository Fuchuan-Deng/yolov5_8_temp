import os
import shutil
import cv2


def move(src_dir, dest_dir):
    files = os.listdir(src_dir)
    for file in files:
        src_file = os.path.join(src_dir, file)
        # image = cv2.imread(src_file, cv2.IMREAD_COLOR)
        # dest_file = os.path.join(dest_dir, file.split('.')[0] + '.jpg')
        # cv2.imwrite(dest_file, image, [cv2.IMWRITE_JPEG_QUALITY, 100])
        shutil.copy(src_file, dest_dir)
    return


if __name__ == "__main__":

    # save image into .jpg file
    src_dir = r"/data1/dataset_duangusuangu/JPEGImages"
    dest_dir = r"/data1/dataset_duangusuangu/train/images/train2017"
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    move(src_dir, dest_dir)