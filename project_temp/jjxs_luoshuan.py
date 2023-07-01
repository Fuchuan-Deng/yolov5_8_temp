import os
import cv2


if __name__ == "__main__":
    root = "/data1/dataset_jinjuxiushi/fenlei/07010057"
    files = os.listdir(root)

    for file in files:
        image = cv2.imread(os.path.join(root, file), cv2.IMREAD_COLOR)
        w, h = image.shape[:2]
        if w / h > 4 or h / w > 4:
            print(file)