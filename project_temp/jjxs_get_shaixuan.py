import os
import shutil


if __name__ == "__main__":
    shaixuan = "/data1/dataset_jinjuxiushi/yishaixuan"
    fenlei = "/data1/dataset_jinjuxiushi/fenlei"
    dest = "/data1/dataset_jinjuxiushi/weishaixuan"
    fenlei_dirs = os.listdir(fenlei)
    
    for dir in fenlei_dirs:
        fenlei_dir = os.path.join(fenlei, dir)
        shaixuan_dir = os.path.join(shaixuan, dir)
        dest_dir = os.path.join(dest, dir)

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        files = os.listdir(fenlei_dir)
        shaixuan_files = os.listdir(shaixuan_dir)
        for file in files:

            if file not in shaixuan_files:
                fenlei_path = os.path.join(fenlei_dir, file)
                print(fenlei_path)
                shutil.copy(fenlei_path, dest_dir)
