#
#  ___       ___
# (   )     (   )
#  | |.-.    | |   ___  ___   ___ .-.     ___ .-.     ___  ___   .--.    .--.
#  | /   \   | |  (   )(   ) (   )   \   (   )   \   (   )(   ) (_  |   / ,  ;
#  |  .-. |  | |   | |  | |   | ' .-. ;   | ' .-. ;   | |  | |    | |  | .(___)
#  | |  | |  | |   | |  | |   |  / (___)  |  / (___)  | |  | |    | |  | | _
#  | |  | |  | |   | |  | |   | |         | |         | '  | |    | |  | '` `.
#  | |  | |  | |   | |  | |   | |         | |         '  `-' |    | |  | .-,  .
#  | '  | |  | |   | |  ; '   | |         | |          `.__. |    | |  | |  | |
#  ' `-' ;   | |   ' `-'  /   | |         | |          ___ | |    | |  . `-'  ;
#   `.__.   (___)   '.__.'   (___)       (___)        (   )' |   (___)  '.__.'
#                                                      ; `-' '
#                                                       .__.'

if __name__ == "__main__":
    raise Exception("Please don't run mcdatacollector package files.")

from datetime import datetime, timedelta
from json import load, dump, dumps
from os import system
from os.path import exists, isfile, isdir, splitext
from pathlib import Path
from time import sleep, time
from typing import Generator, TextIO

from colorama import init, Back, Fore
from mojang import API

__version__ = "1.2.0"

# Files
LOGPATH = Path(r"C:\MultiMC\instances\1.20.2 copy 1\.minecraft\logs\latest.log")
DATAPATH = Path(r"C:\Users\Blurry\PycharmProjects\playersData\data\data.json")
STATSPATH = Path(r"C:\Users\Blurry\PycharmProjects\playersData\stats.json")

# Directories
MODELSPATH = Path(r"C:\Users\Blurry\PycharmProjects\playersData\models")
SKINSPATH = Path(r"C:\Users\Blurry\PycharmProjects\playersData\skins")
SKINSURLPATH = Path(r"C:\Users\Blurry\PycharmProjects\playersData\skins_url")

init(autoreset=True)  # Colorama init

mapi = API()  # Mojang API init

__paths__: list = [LOGPATH, DATAPATH, STATSPATH, MODELSPATH, SKINSPATH, SKINSURLPATH]  # All paths
__files__: list = [LOGPATH, DATAPATH, STATSPATH]  # Only files' paths
__dirs__: list = [MODELSPATH, SKINSURLPATH, SKINSPATH]  # Only directories' paths

# warnings
for i in __paths__:
    if i == Path(""):
        print(f"{Back.RED}Empty string was given as path. Exceptions may be raised.")
        print(f"{Back.RED}Please change the value at {__file__} file")
        system("pause")
    elif not exists(i):
        print(f"{Back.RED}{i} doesn't exist. Exceptions may be raised.")
        print(f"{Back.RED}Please change the value at {__file__} file")
        system("pause")
    elif i in __dirs__ and isfile(i):
        print(f"{Back.RED}{i} is a file, while it has to be a directory. Exceptions may be raised.")
        system("pause")
    elif i in __files__ and isdir(i):
        print(f"{Back.RED}{i} is a directory, while it has to be a file. Exceptions may be raised.")
        system("pause")
if splitext(DATAPATH)[1] != ".json" and exists(DATAPATH) and DATAPATH != Path(""):
    print(f"{Back.RED}{DATAPATH} has not .json extension.")
    system("pause")
if splitext(STATSPATH)[1] != ".json" and exists(STATSPATH) and STATSPATH != Path(""):
    print(f"{Back.RED}{STATSPATH} has not .json extension.")
    system("pause")

del i


class JsonFile:
    """JsonFile class contains required methods to work with .json files"""

    def __init__(self, file_path: Path | str) -> None:
        self.file_path: Path = Path(file_path)

    def load(self) -> dict | list:
        """loads data from json file"""
        with open(self.file_path, "r", encoding="UTF-8") as data_file:
            return load(data_file)

    def dump(self, data: dict | list, indent: int = 2) -> None:
        """dumps selected data to the file"""
        with open(self.file_path, "w", encoding="UTF-8") as data_file:
            dump(data, data_file, indent=indent)


def follow(file: TextIO) -> Generator[str, None, None]:
    """follows selected file"""
    file.seek(0, 2)
    while True:
        li = file.readline()
        if not li:
            sleep(0.1)
            continue
        yield li


def updateviauuid(uuid: str) -> None:
    global datafile
    profile = mapi.get_profile(uuid)
    data = datafile.load()
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
        "cape_url": profile.cape_url.replace("http://", "https://"),
        "skin_url": profile.skin_url.replace("http://", "https://"),
        "db_id": (
            len(data)
            if uuid not in data
            else data[uuid]["db_id"]
        ),
        "does_exist": True,
    }
    datafile.dump(data)
    print(f"{Fore.GREEN}{profile.name}'s dictionary was updated/added.")
    print(dumps(data[uuid], indent=2))


def updatevianickname(nickname: str) -> None:
    if nickname != "*":
        data = datafile.load()
        data[nickname.lower()] = {
            "id": None,
            "name": nickname,
            "last_seen": int(time()),
            "first_time_seen": (
                int(time())
                if nickname not in data
                else data[nickname]["first_time_seen"]
            ),
            "skin_variant": None,
            "cape_url": None,
            "skin_url": None,
            "db_id": (
                len(data)
                if nickname not in data
                else data[nickname]["db_id"]
            ),
            "does_exist": False,
        }
        datafile.dump(data)
        print(f"{Fore.GREEN}{nickname}'s dictionary updated.")
        print(dumps(data[nickname.lower()], indent=2))


def savestats():
    data_len = len(datafile.load())
    statsdata: dict = statsdataobj.load()
    # prev_date = (datetime.now().date() - timedelta(days=2)).strftime("%Y-%m-%d")
    last_date = list(statsdata)[-1]
    now_date = (datetime.now().date() - timedelta(days=1)).strftime("%Y-%m-%d")
    statsdata[now_date] = {
        "count": data_len,
        "delta": data_len - int(statsdata[last_date]["count"]),
    }

    print(dumps(statsdata, indent=4))
    a = input(f"{Fore.MAGENTA}Proceed? y/n: ")
    if a.lower() == "y" or a == "":
        statsdataobj.dump(statsdata)
    print(Fore.RESET)


datafile = JsonFile(DATAPATH)
statsdataobj = JsonFile(STATSPATH)
