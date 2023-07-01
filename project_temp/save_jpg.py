import os
import cv2


def save_jpg(dir, dest):
    files = os.listdir(dir)
    for file in files:
        dest_file = os.path.join(dest, file.split(".")[0] + ".jpg")
        file = os.path.join(dir, file)

        image = cv2.imread(file, cv2.IMREAD_COLOR)
        print(file)
        cv2.imwrite(dest_file, image, [cv2.IMWRITE_JPEG_QUALITY, 100])
    return 


if __name__ == "__main__":
    dir = "./train/images/train2017"
    dest = "./train/images/train"
    save_jpg(dir, dest)


