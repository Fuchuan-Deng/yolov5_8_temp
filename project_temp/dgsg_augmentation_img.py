import os
import cv2


def augment_img(src_dir, dest_dir):
    files = os.listdir(src_dir)
    move_pxl = 100
    for i, file in enumerate(files):
        print(i, len(files))
        
        file_or = file.split(".")[0] + ".jpg"
        # file_h = file.split(".")[0] + "_h.jpg"
        # file_w = file.split(".")[0] + "_w.jpg"
        # file_hw = file.split(".")[0] + "_hw.jpg"
        file_rl = file.split(".")[0] + "_rl.jpg"
        file_ud = file.split(".")[0] + "_ud.jpg"
        file_ct = file.split(".")[0] + "_ct.jpg"

        dest_fileor = os.path.join(dest_dir, file_or)
        # dest_fileh = os.path.join(dest_dir, file_h)
        # dest_filew = os.path.join(dest_dir, file_w)
        # dest_filehw = os.path.join(dest_dir, file_hw)
        dest_filerl = os.path.join(dest_dir, file_rl)
        dest_fileud = os.path.join(dest_dir, file_ud)
        dest_filect = os.path.join(dest_dir, file_ct)

        file = os.path.join(src_dir, file)
        image = cv2.imread(file, cv2.IMREAD_COLOR)
        # # 高度降低了move_pxl像素
        # image_h = image[move_pxl:, :]
        # # 宽度降低了move_pxl像素
        # image_w = image[:, move_pxl:]
        # # 高度和宽度都降低了move_pxl像素
        # image_hw = image[move_pxl:, move_pxl:]
        # 左右翻转
        image_rl = image[:, ::-1]
        # 上下翻转
        image_ud = image[::-1, :]
        # 中心翻转
        image_ct = image[::-1, ::-1]

        cv2.imwrite(dest_fileor, image, [cv2.IMWRITE_JPEG_QUALITY, 100])
        # cv2.imwrite(dest_fileh, image_h, [cv2.IMWRITE_JPEG_QUALITY, 100])
        # cv2.imwrite(dest_filew, image_w, [cv2.IMWRITE_JPEG_QUALITY, 100])
        # cv2.imwrite(dest_filehw, image_hw, [cv2.IMWRITE_JPEG_QUALITY, 100])
        cv2.imwrite(dest_filerl, image_rl, [cv2.IMWRITE_JPEG_QUALITY, 100])
        cv2.imwrite(dest_fileud, image_ud, [cv2.IMWRITE_JPEG_QUALITY, 100])
        cv2.imwrite(dest_filect, image_ct, [cv2.IMWRITE_JPEG_QUALITY, 100])


if __name__ == "__main__":
    src_dir = r"/data1/dataset_duangusuangu/shai/JPEGImages"
    dst_dir = r"/data1/dataset_duangusuangu/train1/images/train2017"
    # test_dir = r"./train/labels/train2017"

    augment_img(src_dir, dst_dir)
