import os


def rename_img_label(img_dir, lbl_dir):
    image_files = os.listdir(img_dir)
    label_files = os.listdir(lbl_dir)

    if len(image_files) == len(label_files):
        print("The length is right. And the length is ", len(image_files))

    img_files = []
    lbl_files = []
    for i in range(len(image_files)):
        img_files.append(image_files[i][:-4])
        lbl_files.append(label_files[i][:-4])

    count = 0
    for img_fie in img_files:
        if img_fie not in lbl_files:
            count = count + 1
            print(img_fie)
    print("The file which does not have the same name is ", count)
    return


if __name__ == "__main__":
    img_dir = "/data1/jinjuxiushi/train/images/train2017"
    lbl_dir = "/data1/jinjuxiushi/train/labels/train2017"
    rename_img_label(img_dir, lbl_dir)