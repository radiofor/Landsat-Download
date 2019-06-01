# -*- coding: utf-8 -*-
import os
import shutil
from requests import get
import gzip
import pandas as pd
from zipfile import ZipFile


os.chdir(os.path.dirname(__file__))
LANDSAT_LISTS_URL = 'http://storage.googleapis.com/gcp-public-data-landsat/index.csv.gz'
LISTS_ZIP = 'index.csv.gz'
LISTS_DIR = 'lists'
LISTS_CSV = LISTS_DIR + '.csv'
WRS_URL = ['https://landsat.usgs.gov/sites/default/files/documents/WRS1_descending.zip',
           'https://landsat.usgs.gov/sites/default/files/documents/WRS2_descending.zip']
WRS_ZIP = ['WRS1_descending.zip', 'WRS2_descending.zip']
WRS_DIR = 'wrs'


def update_list():
    print('\nUpdating the Landsat data list...')
    if os.path.isdir(LISTS_DIR):
        shutil.rmtree(LISTS_DIR)
    os.mkdir(LISTS_DIR)
    download_lists()
    split_lists()


def download_lists():
    if os.path.isfile(LISTS_ZIP):
        os.remove(LISTS_ZIP)
    print('Downloading {}'.format(LANDSAT_LISTS_URL))
    response = get(LANDSAT_LISTS_URL, stream=True)
    if response.status_code != 200:
        raise ValueError('Bad response {} from request.'.format(response.status_code))

    content_size = int(response.headers['content-length']) / pow(1024, 2)
    with open(LISTS_ZIP, 'wb') as f:
        chunk_now = 0
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                chunk_now = chunk_now + len(chunk) / pow(1024, 2)
                now_progress = (chunk_now / content_size) * 100
                print('\r {:.2f}% ({:.2f}/{:.2f})MB'.format(now_progress, chunk_now, content_size), end='')

    with gzip.open(LISTS_ZIP, 'rb') as infile:
        print('\nUnzipping {}'.format(LISTS_ZIP))
        with open(LISTS_CSV, 'wb') as outfile:
            for line in infile:
                outfile.write(line)

    os.remove(LISTS_ZIP)


def split_lists():
    print('Spliting {}'.format(LISTS_CSV))
    csv_data = pd.read_csv(LISTS_CSV, encoding='GBK', low_memory=False)
    spacecraft_ids = pd.unique(csv_data['SPACECRAFT_ID'])
    for spacecraft_id in spacecraft_ids:
        csv_filter = csv_data[csv_data['SPACECRAFT_ID'] == spacecraft_id]
        csv_filter.to_csv(os.path.join(LISTS_DIR, '{}.csv'.format(spacecraft_id)))
    os.remove(LISTS_CSV)


def download_wrs():
    print('\nConfiguring WRS reference data...')
    if os.path.isdir(WRS_DIR):
        shutil.rmtree(WRS_DIR)
    os.mkdir(WRS_DIR)

    for url, wzip in zip(WRS_URL, WRS_ZIP):
        if os.path.isfile(wzip):
            os.remove(wzip)
        print('Downloading {}'.format(url))
        response = get(url, stream=True)
        if response.status_code != 200:
            raise ValueError('Bad response {} from request.'.format(response.status_code))

        content_size = int(response.headers['content-length']) / pow(1024, 2)
        with open(wzip, 'wb') as f:
            chunk_now = 0
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    chunk_now = chunk_now + len(chunk) / pow(1024, 2)
                    now_progress = (chunk_now / content_size) * 100
                    print('\r {:.2f}% ({:.2f}/{:.2f})MB'.format(now_progress, chunk_now, content_size), end='')

        with ZipFile(wzip, 'r') as zip_file:
            print('\nUnzipping {}'.format(wzip))
            zip_file.extractall(WRS_DIR)

        os.remove(wzip)


if __name__ == '__main__':
    update_list()
    download_wrs()
    pass
