import os
import shutil
import glob


def get_shaixuan(sx_path, src_jpg_path, dst_jpg_path):
    files = os.listdir(sx_path)
    # dirs = [src_jpg_path, src_xml_path]
    names = []
    for file in files:
        name = file[:-4]
        path = os.path.join(src_jpg_path, name + "*")
        path = glob.glob(path)
        shutil.copy(path[0], dst_jpg_path)
    return


if __name__ == "__main__":
    txt_path = "/data1/dataset_duangusuangu/val/labels/train2017"
    src_jpg_path = "/data1/dataset_jinjuxiushi/JPEGImages"
    dst_jpg_path = "/data1/dataset_duangusuangu/val/images/train2017"

    get_shaixuan(txt_path, src_jpg_path, dst_jpg_path)