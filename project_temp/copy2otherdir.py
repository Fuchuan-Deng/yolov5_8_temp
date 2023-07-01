import os
import shutil

src_dirs = ["/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/T型线夹锈蚀07010043/标注",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/塔材锈蚀04010005/1",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/塔材锈蚀04010005/2",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/塔材锈蚀04010005/3",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/塔材锈蚀04010005/4",
            "//data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/导线锈蚀01010008/导线锈蚀1",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/导线锈蚀01010008/导线锈蚀2",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/导线锈蚀01010008/导线锈蚀3",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/广州局-金具锈蚀20230111_V1.0/1",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/广州局-金具锈蚀20230111_V1.0/2",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/广州局-金具锈蚀20230111_V1.0/3",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/广州局-金具锈蚀20230111_V1.0/4",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/广州局-金具锈蚀20230111_V1.0/5",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/广州局-金具锈蚀20230111_V1.0/6",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/广州局-金具锈蚀20230111_V1.0/7",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/广州局-金具锈蚀20230111_V1.0/广州局-锈蚀1",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/广州局-金具锈蚀20230111_V1.0/广州局-锈蚀2",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/广州局-金具锈蚀20230111_V1.0/广州局-锈蚀3",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/拉线金具锈蚀03060011/标注",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/拉线锈蚀01020001/已复核",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/接地引下线锈蚀06020003/标注",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/玻璃绝缘子锈蚀损伤02010011/标注",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/耐张线夹锈蚀07010041/标注",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/金具锈蚀（原始数据）20230111_V1.0/已复核1",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/金具锈蚀（原始数据）20230111_V1.0/已复核2",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/金具锈蚀（原始数据）20230111_V1.0/已复核3",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/金具锈蚀（服务器搜集）20230111_V1.0",
            "/data3/20211217_wuhaiyue_data/20230320_shudianxiushishuju(74leixiushi&jinjuxiushi)/陶瓷绝缘子锈蚀02030006/已复核"
]



def move(src_dir, dest_dir):
    files = os.listdir(src_dir)
    for file in files:
        src_file = os.path.join(src_dir, file)
        shutil.copy(src_file, dest_dir)
    return


if __name__ == "__main__":
    dest_dir = r"/data1/dataset_jinjuxiushi/all"
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for src_dir in src_dirs:
        print(src_dir)
        move(src_dir, dest_dir)