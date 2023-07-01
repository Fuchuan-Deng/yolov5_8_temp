import os
import shutil


def move(src_dir, dest_dir):
    files = os.listdir(src_dir)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for file in files:
        src_file = os.path.join(src_dir, file)
        # dest_file = os.path.join(dest_dir, file)
        print(src_file)
        shutil.move(src_file, dest_dir)
    return


if __name__ == "__main__":
    src_dir = r"/data4/jyzzb_nc/images"
    dest_dir = r"/data4/jyzzb_nc/images/train2017"
    move(src_dir, dest_dir)

    src_dir = r"/data4/jyzzb_nc/labels/"
    dest_dir = r"/data4/jyzzb_nc/labels/train2017"
    move(src_dir, dest_dir)
