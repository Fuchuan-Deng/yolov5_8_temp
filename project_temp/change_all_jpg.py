import os
import cv2


def change_all_jpg(dir):
    files = os.listdir(dir)
    i = 0
    error_count = 0
    print("THE LENGTH OF FILES: ", len(files))
    for file in files:
        file = os.path.join(dir, file)
        if os.path.exists(file):
            try:
                img = cv2.imread(file)
                cv2.imwrite(file, img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            except:
                error_count = error_count + 1
                print(file)
    print(error_count)
    return


if __name__ == "__main__":
    root = r"./images/train2017"
    change_all_jpg(root)