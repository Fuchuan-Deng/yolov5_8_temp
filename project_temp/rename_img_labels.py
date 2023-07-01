import os


suffix = [".png", ".jpg", ".JPG", ".PNG"]


def rename_img_label(img_dir, lbl_dir):
    image_files = os.listdir(img_dir)
    label_files = os.listdir(lbl_dir)

    if len(image_files) == len(label_files):
        print("The length is right. And the length is ", len(image_files))
    else:
        print("The length is error.")
        return

    img_files = []
    lbl_files = []
    for i in range(len(image_files)):
        img_files.append(image_files[i][:-4])
        lbl_files.append(label_files[i][:-4])

    count = 0
    for i, img_file in enumerate(image_files):
        if img_file[:-4] in img_files and img_file[:-4] in lbl_files:
            count = count + 1

            new_img_file = "%06d" % (i)
            new_img_file = new_img_file + img_file[-4:]
            new_img_file = os.path.join(img_dir, new_img_file)
            old_img_file = os.path.join(img_dir, img_file)

            new_lbl_file = "%06d.txt" % i
            new_lbl_file = os.path.join(lbl_dir, new_lbl_file)
            old_lbl_file = img_file[:-4] + ".txt"
            old_lbl_file = os.path.join(lbl_dir, old_lbl_file)

            if os.path.exists(old_img_file) and os.path.exists(old_lbl_file):
                os.rename(old_img_file, new_img_file)
                os.rename(old_lbl_file, new_lbl_file)
                # print(old_img_file, "   to   ", new_img_file)
                # print(old_lbl_file, "   to   ", new_lbl_file)
    print("The same name in files are ", count)
    return


if __name__ == "__main__":
    img_dir = "./train/images/train2017"
    lbl_dir = "./train/labels/train2017"
    rename_img_label(img_dir, lbl_dir)