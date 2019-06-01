# -*- coding: utf-8 -*-
import os
import pandas as pd
from datetime import datetime
import ogr


os.chdir(os.path.dirname(__file__))
LISTS_DIR = 'lists'
WRS_DIR = 'wrs'


def by_scene_ids_file(scene_ids_file):
    query_results = []
    with open(scene_ids_file) as f:
        scene_id = f.readline()
        while scene_id:
            csv_file = os.path.join(LISTS_DIR, 'LANDSAT_{}.csv'.format(scene_id[2]))
            csv_data = pd.read_csv(csv_file, encoding='gbk', low_memory=False)
            if scene_id in csv_data['SCENE_ID']:
                query_results.append(scene_id)
            scene_id = f.readline()
    return query_results


def by_time_path_row(spacecraft_id, sensing_time, wrs_paths, wrs_rows, cloud_cover):
    query_results = []
    for wrs_path in range(wrs_paths[0], wrs_paths[1] + 1):
        for wrs_row in range(wrs_rows[0], wrs_rows[1] + 1):
            query_results += __by_time_apath_arow(spacecraft_id, sensing_time, (wrs_path, wrs_row), cloud_cover)
    return query_results


def by_time_lon_lat(spacecraft_id, sensing_time,  longitude, latitude, cloud_cover):
    if spacecraft_id in ['1', '2', '3']:
        wrs_shp = 'WRS1_descending.shp'
    else:  # in ['4', '5', '7', '8']
        wrs_shp = 'WRS2_descending.shp'

    wrs_path_rows = __lonlat_to_pathrow(wrs_shp, longitude, latitude)
    query_results = []
    for wrs_path_row in wrs_path_rows:
        query_results += __by_time_apath_arow(spacecraft_id, sensing_time, wrs_path_row, cloud_cover)

    return query_results


def __by_time_apath_arow(spacecraft_id, sensing_time, wrs_path_row, cloud_cover):
    sensing_time = [datetime.strptime(sensing_time[0], "%Y-%m-%d"), datetime.strptime(sensing_time[1], "%Y-%m-%d")]
    csv_file = os.path.join(LISTS_DIR, 'LANDSAT_{}.csv'.format(spacecraft_id))
    csv_data = pd.read_csv(csv_file, encoding='gbk', low_memory=False)
    csv_filter = csv_data[(csv_data['WRS_PATH'] == wrs_path_row[0]) &
                          (csv_data['WRS_ROW'] == wrs_path_row[1]) &
                          (csv_data['CLOUD_COVER'] <= cloud_cover)]

    query_results = []
    for scene_id, data_time in zip(csv_filter['SCENE_ID'], csv_filter['SENSING_TIME']):
        data_time = datetime.strptime(data_time[:10], "%Y-%m-%d")
        if ((data_time - sensing_time[0]).days >= 0) and ((data_time - sensing_time[1]).days <= 0):
            query_results.append(scene_id)

    return query_results


def __lonlat_to_pathrow(wrs_shp, longitude, latitude):
    shape_file = os.path.join(WRS_DIR, wrs_shp)
    coordinates = '{} {},{} {},{} {},{} {},{} {}'.format(longitude[0], latitude[0], longitude[0], latitude[1],
                                                         longitude[1], latitude[1], longitude[1], latitude[0],
                                                         longitude[0], latitude[0])
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_source = driver.Open(shape_file, 0)
    layer = data_source.GetLayer()
    wkt = 'POLYGON ((' + coordinates + '))'
    layer.SetSpatialFilter(ogr.CreateGeometryFromWkt(wkt))
    wrs_path_rows = []
    for feature in layer:
        wrs_path_rows.append((feature.GetField('path'), feature.GetField('row')))
    return wrs_path_rows


if __name__ == '__main__':
    pass
