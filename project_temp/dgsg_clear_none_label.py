import os
import glob

def clear_none(dir):
    files = glob.glob(os.path.join(dir, "*"))
    for file in files:
        if os.path.getsize(file) == 0:
            os.remove(file)
    return 


if __name__ == "__main__":
     dir = "/data1/dataset_duangusuangu/train/labels/train2017"
     clear_none(dir)