import json
from pathlib import Path
from mojang import API
from colorama import init, Back, Fore
from os.path import exists, isfile, isdir, splitext
from os import system
from typing import Union
from time import sleep

LOGPATH = Path("")
DATAPATH = Path("")
STATSPATH = Path("")
MODELSPATH = Path("")
SKINSPATH = Path("")
SKINSURLPATH = Path("")

init(autoreset=True)

mapi = API()

__paths__: list = [LOGPATH, DATAPATH, STATSPATH, MODELSPATH, SKINSPATH, SKINSURLPATH]  # All paths
__files__: list = [LOGPATH, DATAPATH, STATSPATH]  # Only files paths
__dirs__: list = [MODELSPATH, SKINSURLPATH, SKINSPATH]  # Only directories paths

for i in __paths__:
    if i == "":
        print(f"{Back.RED}Empty string was given as path. Exceptions may be raised.")
        print(f"{Back.RED}Please change the value at __data__.py file")
        system("pause")
    elif not exists(i):
        print(f"{Back.RED}{i} doesn't exist. Exceptions may be raised.")
        print(f"{Back.RED}Please change the value at __data__.py file")
        system("pause")
    elif i in __dirs__ and isfile(i):
        print(f"{Back.RED}{i} is a file, while it has to be a directory.")
        system("pause")
    elif i in __files__ and isdir(i):
        print(f"{Back.RED}{i} is a directory, while it has to be a file.")
        system("pause")
if splitext(DATAPATH)[1] != ".json" and exists(DATAPATH):
    print(f"{Back.RED}{DATAPATH} has not .json extension.")
    system("pause")
if splitext(STATSPATH)[1] != ".json" and exists(STATSPATH):
    print(f"{Back.RED}{STATSPATH} has not .json extension.")
    system("pause")


class JsonFile:
    """JsonFile class contains required methods to work with .json files"""

    def __init__(self, file_path: Path) -> None:
        self.file_path: Path = file_path

    def load(self) -> Union[dict, list]:
        """loads data from json file"""
        with open(self.file_path, "r", encoding="UTF-8") as data_file:
            return json.load(data_file)

    def dump(self, data: Union[dict, list], indent: int = 4) -> None:
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


cvdbdata = JsonFile(DATAPATH)
statsdataobj = JsonFile(STATSPATH)


def updateviauuid(uuid: str) -> None:
    profile = mapi.get_profile(uuid)
    data = cvdbdata.load()
    data[uuid] = {
        "id": profile.id,
        "name": profile.name,
        "last_seen": round(float(profile.timestamp) / 1000),
        "first_time_seen": (
            round(float(profile.timestamp) / 1000)
            if uuid not in data
            else data[uuid]["first_time_seen"]
        ),
        "skin_variant": profile.skin_variant,
        "cape_url": profile.cape_url,
        "skin_url": profile.skin_url,
        "db_id": (
            len(data)
            if uuid not in data
            else data[uuid]["db_id"]
        ),
        "does_exist": True,
    }
    cvdbdata.dump(data)
    print(
        f"{Fore.GREEN}{profile.name}'s dictionary was updated/added."
    )
