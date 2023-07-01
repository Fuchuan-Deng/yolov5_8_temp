import os
import shutil
import glob
import cv2


def get_images_by_label(dir):
    files = os.listdir(dir)
    for i, file in enumerate(files):
        path = os.path.join(dir, file)
        print(path)
        image = cv2.imread(path, cv2.IMREAD_COLOR)
        wh = min(image.shape[:2])
        if wh > 2560 * 2:
            image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

        wh = min(image.shape[:2])
        if wh > 2560 * 2:
            image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

        cv2.imwrite(path, image, [cv2.IMWRITE_JPEG_QUALITY, 100])
    return


if __name__ == "__main__":

    dir = "/data1/dataset_duangusuangu/train1/images/train2017"

    get_images_by_label(dir)