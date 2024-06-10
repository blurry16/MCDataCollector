import json
from typing import Union
from time import sleep

LOGPATH = r"C:\MultiMC\instances\1.20.2 copy 1\.minecraft\logs\latest.log"
DATAPATH = r"C:\Users\Blurry\PycharmProjects\playersData\data\data.json"
STATSPATH = r"C:\Users\Blurry\PycharmProjects\playersData\stats.json"
MODELSPATH = r"C:\Users\Blurry\PycharmProjects\playersData\models"
SKINSPATH = r"C:\Users\Blurry\PycharmProjects\playersData\skins"
SKINSURLPATH = r"C:\Users\Blurry\PycharmProjects\playersData\skins_url"

UKNOWNVALUEEXCEPTION = Exception("Unknown value")


class __data__:
    """__data__ class contained load and dump methods to work with JSON files more comfy"""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> Union[dict, list]:
        """loads data from json file"""
        with open(self.file_path, "r", encoding="UTF-8") as data_file:
            return json.load(data_file)

    def dump(self, data: Union[dict, list], indent=4):
        """dumps selected data to the file"""
        with open(self.file_path, "w", encoding="UTF-8") as data_file:
            json.dump(data, data_file, indent=indent)


def follow(file):
    """follows selected file"""
    file.seek(0, 2)
    while True:
        li = file.readline()
        if not li:
            sleep(0.1)
            continue
        yield li


cvdbdata = __data__(DATAPATH)
statsdataobj = __data__(STATSPATH)
