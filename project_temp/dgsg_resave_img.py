import cv2
import os
import glob


if __name__ == "__main__":
    dir =     "/data1/dataset_duangusangu_seg/data/train/images/images"
    dst_dir = "/data1/dataset_duangusangu_seg/data/train/images/train2017"

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # files = os.listdir(dir)
    files = glob.glob(os.path.join(dir, "*"))
    for i, file in enumerate(files):
        # path = os.path.join(dir, file)
        dst_path = os.path.join(dst_dir, file.split("/")[-1].split(".")[0] + ".jpg")
        print(i, len(files), dst_path)
        
        image = cv2.imread(file, cv2.IMREAD_COLOR)
        if image is not None:
            w, h = image.shape[:2]
            if w > 4000 or h > 4000:
                image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

            w, h = image.shape[:2]
            if w > 4000 or h > 4000:
                image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imwrite(dst_path, image, [cv2.IMWRITE_JPEG_QUALITY, 100])