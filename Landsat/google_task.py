# -*- coding: utf-8 -*-
import os
import shutil
from Landsat import update_metadata
from Landsat import query_scene_id
from Landsat.file_name import FileName
from requests import get


os.chdir(os.path.dirname(__file__))
LISTS_DIR = 'lists'
WRS_DIR = 'wrs'


class GoogleTask(object):
    def __init__(self, spacecraft_id=None, sensing_time=None, longitudes=None, latitudes=None, wrs_paths=None,
                 wrs_rows=None, cloud_cover=None, scene_ids_file=None, out_path=None):
        self.__check_metadata()
        self.spacecraft_id = spacecraft_id
        self.sensing_time = sensing_time
        self.longitudes = longitudes
        self.latitudes = latitudes
        self.wrs_paths = wrs_paths
        self.wrs_rows = wrs_rows
        self.cloud_cover = cloud_cover
        self.scene_ids_file = scene_ids_file
        self.out_path = out_path

    def start(self):
        scene_ids = []
        if self.scene_ids_file is not None:
            scene_ids = self.__get_scene_ids()
        elif (self.longitudes is not None) and (self.latitudes is not None):
            scene_ids = query_scene_id.by_time_lon_lat(self.spacecraft_id, self.sensing_time,  self.longitudes,
                                                       self.latitudes, self.cloud_cover)
        elif (self.wrs_paths is not None) and (self.wrs_rows is not None):
            scene_ids = query_scene_id.by_time_path_row(self.spacecraft_id, self.sensing_time, self.wrs_paths,
                                                        self.wrs_rows, self.cloud_cover)
        else:
            exit(0)

        if not scene_ids:
            print('No suitable data be found!')
            exit(0)
        download_info = {}
        for scene_id in scene_ids:
            download_info[scene_id] = self.__get_urls(scene_id)
        self.__list(download_info)
        print('Download Now? [y/n]:', end='')
        if input() is 'y':
            self.__download(download_info)

    @staticmethod
    def __list(download_info):
        print('The following data was searched:')
        for key in download_info.keys():
            print(key)

    def __download(self, download_info):
        for key in download_info.keys():
            print('\n<-*->{}<-*->'.format(key))
            out_path = os.path.join(self.out_path, key)
            if os.path.isdir(out_path):
                shutil.rmtree(out_path)
            os.mkdir(out_path)
            for url in download_info[key]:
                print('\nDownloading {}'.format(url))
                file_name = os.path.basename(url)
                response = get(url, stream=True)
                if response.status_code != 200:
                    print('Bad response {} from request.'.format(response.status_code))
                    continue

                content_size = int(response.headers['content-length']) / pow(1024, 2)
                with open(file_name, 'wb') as f:
                    chunk_now = 0
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            chunk_now = chunk_now + len(chunk) / pow(1024, 2)
                            now_progress = (chunk_now / content_size) * 100
                            print('\r {:.2f}% ({:.2f}/{:.2f})MB'.format(now_progress, chunk_now, content_size), end='')

    @staticmethod
    def __get_urls(scene_id):
        url_header = 'http:\\\\storage.googleapis.com\\gcp-public-data-landsat'
        file_name = FileName(scene_id)
        urls = []
        for suffix in file_name.suffixes:
            url = os.path.join(url_header, file_name.category, 'PRE', file_name.path, file_name.row, file_name.id,
                               file_name.id + '_' + suffix)
            url = url.replace('\\', '/')
            urls.append(url)
        return urls

    @staticmethod
    def __check_metadata():
        if not os.path.isdir(LISTS_DIR):
            update_metadata.update_list()

        if not os.path.isdir(WRS_DIR):
            update_metadata.download_wrs()

    def __get_scene_ids(self):
        scene_ids = []
        with open(self.scene_ids_file) as f:
            scene_id = f.readline()
            while scene_id:
                scene_ids.append(scene_id)
                scene_id = f.readline()
        return scene_ids


if __name__ == '__main__':
    pass

