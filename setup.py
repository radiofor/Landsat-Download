# -*- coding: utf-8 -*-
from setuptools import setup


setup(name='Landsat',
      version=1.0,
      description='Very simple API to download Landsat data from Landsat 1 - 5, 7, and 8 from Google',
      author='Viktor Xu',
      author_email='x572722344@gmail.com',
      url='https://github.com/radiofor',
      packages=['Landsat'],
      include_package_data=True,
      entry_points={'console_scripts': ['landsat_update_list = Landsat.command_update_list:submit',
                                        'landsat_id = Landsat.command_scene_id:submit',
                                        'landsat_path_row = Landsat.command_path_row:submit',
                                        'landsat_lon_lat = Landsat.command_lon_lat:submit']},
      requires=['pandas', 'GDAL', 'requests', 'click'])
