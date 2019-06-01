# -*- coding: utf-8 -*-


class FileName(object):
    def __init__(self, scene_id):
        self._scene_id = scene_id

    @property
    def id(self):
        return self._scene_id

    @property
    def category(self):
        return self._scene_id[:2] + '0' + self._scene_id[2]

    @property
    def path(self):
        return self._scene_id[3:6]

    @property
    def row(self):
        return self._scene_id[6:9]

    @property
    def suffixes(self):
        b = {'1': ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF', 'B6.TIF', 'B7.TIF', 'MTL.txt'],
             '2': ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF', 'B6.TIF', 'B7.TIF', 'MTL.txt'],
             '3': ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF', 'B6.TIF', 'B7.TIF', 'MTL.txt'],
             '4': ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF', 'B6.TIF', 'B7.TIF', 'MTL.txt'],
             '5': ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF', 'B6.TIF', 'B7.TIF', 'BQA.TIF', 'MTL.txt'],
             '7': ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF', 'B6_VCID_1.TIF', 'B6_VCID_2.TIF', 'B7.TIF', 'B8.TIF', 'BQA.TIF', 'MTL.txt'],
             '8': ['B1.TIF', 'B2.TIF', 'B3.TIF', 'B4.TIF', 'B5.TIF', 'B6.TIF', 'B7.TIF', 'B8.TIF', 'B9.TIF', 'B10.TIF', 'B11.TIF', 'BQA.TIF', 'MTL.txt']}
        return b[self._scene_id[2]]


if __name__ == '__main__':
    a = FileName('LC80180502013276LGN00')
    print(a.id)
    print(a.suffixes)
