import os


suffix = [".png", ".jpg", ".JPG", ".PNG"]


def rename_img_label(img_dir, xml_dir):
    image_files = os.listdir(img_dir)
    label_files = os.listdir(xml_dir)

    if len(image_files) == len(label_files):
        print("The length is right. And the length is ", len(image_files))

    img_files = []
    xml_files = []
    for i in range(len(image_files)):
        img_files.append(image_files[i].split('.')[0])
    
    for i in range(len(label_files)):
        xml_files.append(label_files[i].split('.')[0])

    count = 0
    for i, img_file in enumerate(image_files):
        if img_file.split('.')[0] in img_files and img_file.split('.')[0] in xml_files:
            pass
        else:
            print(img_file)
    print("The same name in files are ", count)
    return


if __name__ == "__main__":
    img_dir = "/data1/dataset_jinjuxiushi/dataset/images"            # 55464
    xml_dir = "/data1/dataset_jinjuxiushi/dataset/Annotations"    # 27732
    rename_img_label(img_dir, xml_dir)
