import os
import tqdm


suffix = [".png", ".jpg", ".JPG", ".PNG"]


def rename_img_label(img_dir, xml_dir):
    image_files = os.listdir(img_dir)
    label_files = os.listdir(xml_dir)

    if len(image_files) == len(label_files):
        print("The length is right. And the length is ", len(image_files))

    img_files = []
    xml_files = []
    for i in range(len(image_files)):
        img_files.append(image_files[i][.split('.')[0]])
        xml_files.append(label_files[i].split('.')[0])

    count = 0
    for i, img_file in enumerate(image_files):
        print(i, len(image_files))
        if img_file.split('.')[0] in img_files and img_file.split('.')[0] in xml_files:
            count = count + 1

            new_img_file = "%06d" % (i+1)
            new_img_file = new_img_file + '.' + img_file.split('.')[-1]
            new_img_file = os.path.join(img_dir, new_img_file)

            old_img_file = os.path.join(img_dir, img_file)

            new_xml_file = "%06d.json" % (i+1)
            new_xml_file = os.path.join(xml_dir, new_xml_file)

            old_xml_file = img_file.split('.')[0] + ".json"
            old_xml_file = os.path.join(xml_dir, old_xml_file)
            
            if os.path.exists(old_img_file) and os.path.exists(old_xml_file):
                os.rename(old_img_file, new_img_file)
                os.rename(old_xml_file, new_xml_file)
    print("The same name in files are ", count)
    return


if __name__ == "__main__":
    img_dir = "/data1/dataset_duangusangu_seg/seg/images"            # 55464
    xml_dir = "/data1/dataset_duangusangu_seg/seg/json"    # 27732
    rename_img_label(img_dir, xml_dir)