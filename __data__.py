import json
from colorama import init, Back
from os.path import exists, isfile, splitext
from os import system
from typing import Union
from time import sleep

LOGPATH = r"C:\MultiMC\instances\1.20.2 copy 1\.minecraft\logs\latest.log"
DATAPATH = r"C:\Users\Blurry\PycharmProjects\playersData\data\data.json"
STATSPATH = r"C:\Users\Blurry\PycharmProjects\playersData\stats.json"
MODELSPATH = r"C:\Users\Blurry\PycharmProjects\playersData\models"
SKINSPATH = r"C:\Users\Blurry\PycharmProjects\playersData\skins"
SKINSURLPATH = r"C:\Users\Blurry\PycharmProjects\playersData\skins_url"


# LOGPATH = ""
# DATAPATH = ""
# STATSPATH = ""
# MODELSPATH = ""
# SKINSPATH = ""
# SKINSURLPATH = ""

init(autoreset=True)
paths = [LOGPATH, DATAPATH, STATSPATH, MODELSPATH, SKINSURLPATH]
files = [LOGPATH, DATAPATH, STATSPATH]

for i in paths:
    if i == "":
        print(f"{Back.RED}Empty string was given as path. Exceptions may be raised.")
        print(f"{Back.RED}Please change the value at __data__.py file")
        system("pause")
    elif not exists(i):
        print(f"{Back.RED}{i} doesn't exist. Exceptions may be raised.")
        print(f"{Back.RED}Please change the value at __data__.py file")
        system("pause")
    elif i not in files and isfile(i):
        print(f"{Back.RED}{i} is a file, while it has to be a directory.")
        system("pause")
    elif i in files and not isfile(i):
        print(f"{Back.RED}{i} is a directory, while it has to be a file.")
        system("pause")
if splitext(DATAPATH)[1] != ".json" and exists(DATAPATH):
    print(f"{Back.RED}{DATAPATH} has not .json extension.")
    system("pause")
if splitext(STATSPATH)[1] != ".json" and exists(STATSPATH):
    print(f"{Back.RED}{STATSPATH} has not .json extension.")
    system("pause")


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


cvdbdata = __data__(DATAPATH)
statsdataobj = __data__(STATSPATH)
