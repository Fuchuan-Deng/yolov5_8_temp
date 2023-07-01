import os 

if __name__ == "__main__":
    root = "/data1/dataset_jinjuxiushi/yishaixuan"
    files = os.listdir(root)
    for file in files:
        print(file)