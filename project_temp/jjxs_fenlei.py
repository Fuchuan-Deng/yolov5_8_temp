import os 
import tqdm
import shutil


if __name__ == "__main__":
    dir = "/data1/dataset_jinjuxiushi/yanzhongxiushi"
    save_dir = "/data1/dataset_jinjuxiushi/yanzhongxiushi"
    classes = []
    files = os.listdir(dir)
    for i, f in enumerate(files):
        cls = f[8:-8]
        
        if cls not in classes:
            classes.append(cls)
            os.makedirs(os.path.join(save_dir, cls))
        
        path = os.path.join(dir, f)
        print(i, len(files), path)
        shutil.move(path, os.path.join(save_dir, cls))
        
