# Landsat-Download
A simple tool for download Landsat data from Google Cloud Platform.

示例：

# 更新Landsat数据列表
landsat_update_list

# 根据保存Landsat数据id的txt文件下载
landsat_id --scene_ids_file E:\Projects\Landsat\id.txt --out_path E:\Projects\Landsat\test_data

# 根据时间、条带号、行编号、云量下载
landsat_path_row --spacecraft_id 8 --sensing_time 2017-01-23 2017-02-19 --wrs_paths 37 37 --wrs_rows 41 41 --cloud_cover 50 --out_path E:\Projects\Landsat\test_data

# 根据时间、经纬度、云量下载
landsat_lon_lat --spacecraft_id 8 --sensing_time 2017-01-23 2017-02-19 --longitudes 106.5 107.5 --latitudes 34 35 --cloud_cover 50 --out_path E:\Projects\Landsat\test_data
