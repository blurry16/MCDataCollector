__version__ = "1.4.0"

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

from json import load, dump, dumps
from math import ceil
from os import name as osname
from os import system
from os.path import exists, isfile, isdir, splitext
from pathlib import Path
from time import sleep, time
from typing import Generator, TextIO, Callable

from colorama import init, Back, Fore
from dotenv import dotenv_values
from mojang import API

__dotenv__ = dotenv_values(".env")


class Data:
    # Files
    try:
        LOGPATH = Path(__dotenv__["LOGPATH"])
        DATAPATH = Path(__dotenv__["DATAPATH"])
        STATSPATH = Path(__dotenv__["STATSPATH"])

        # Directories
        MODELSPATH = Path(__dotenv__["MODELSPATH"])
        SKINSPATH = Path(__dotenv__["SKINSPATH"])
        SKINSURLPATH = Path(__dotenv__["SKINSURLPATH"])
    except KeyError:
        LOGPATH = Path()
        DATAPATH = Path()
        STATSPATH = Path()

        # Directories
        MODELSPATH = Path()
        SKINSPATH = Path()
        SKINSURLPATH = Path()
    __paths__: list = [LOGPATH, DATAPATH, STATSPATH, MODELSPATH, SKINSPATH,
                       SKINSURLPATH]  # All paths
    __files__: list = [LOGPATH, DATAPATH, STATSPATH]  # Only files' paths
    __dirs__: list = [MODELSPATH, SKINSURLPATH, SKINSPATH]  # Only directories' paths
    __tracker__: list = [LOGPATH, DATAPATH]
    __client__: list = [STATSPATH, MODELSPATH, SKINSPATH, SKINSURLPATH]


def warn(paths: list[Path]):
    for i in paths:
        if i == Path(""):
            print(f"{Back.RED}Empty string was given as path. Exceptions may be raised.")
            print(f"{Back.RED}Please change the value at {__file__} file")
            pause()
        elif not exists(i):
            print(f"{Back.RED}{i} doesn't exist. Exceptions may be raised.")
            print(f"{Back.RED}Please change the value at {__file__} file")
            pause()
        elif i in Data.__dirs__ and isfile(i):
            print(f"{Back.RED}{i} is a file, while it has to be a directory. Exceptions may be raised.")
            pause()
        elif i in Data.__files__ and isdir(i):
            print(f"{Back.RED}{i} is a directory, while it has to be a file. Exceptions may be raised.")
            pause()


def datawarn():
    if splitext(Data.DATAPATH)[1] != ".json" and exists(Data.DATAPATH) and Data.DATAPATH != Path(""):
        print(f"{Back.RED}{Data.DATAPATH} has not .json extension.")
        pause()


def statswarn():
    if splitext(Data.STATSPATH)[1] != ".json" and exists(Data.STATSPATH) and Data.STATSPATH != Path(""):
        print(f"{Back.RED}{Data.STATSPATH} has not .json extension.")
        pause()


init(autoreset=True)  # Colorama init

mapi = API()  # Mojang API init

pause: Callable[[], int] = lambda: system("pause" if osname == "nt" else "")


class JsonFile:
    """JsonFile class contains required methods to work with .json files"""

    def __init__(self, file_path: Path | str) -> None:
        self.file_path: Path = Path(file_path)

    def load(self) -> dict | list:
        """Loads data from the file.

        Returns:
            dict | list: _JSONable_
        """
        with open(self.file_path, "r", encoding="UTF-8") as data_file:
            return load(data_file)

    def dump(self, data: dict | list, indent: int = 2) -> None:
        """Saves (dumps) data into file.

        Args:
            data (dict | list): _JSONable_
            indent (int, optional): _indent for whole file_. Defaults to 2.
        """
        with open(self.file_path, "w", encoding="UTF-8") as data_file:
            dump(data, data_file, indent=indent)

    def dumps(self, key: str | int | None = None, indent: int = 2) -> str:
        """Loads data from file and returns it as string.

        Args:
            key (str | int | None, optional): _Simply file[key]; if key is None, the string of whole file will be returned_. Defaults to None.
            indent (int, optional): _indent of json string_. Defaults to 2.

        Returns:
            str: _json string_
        """
        data = self.load()
        return dumps(data, indent=indent) if key is None else dumps(data[key], indent=indent)


def follow(file: TextIO) -> Generator[str, None, None]:
    """_summary_

    Args:
        file (TextIO): _description_

    Yields:
        Generator[str, None, None]: _description_
    """
    file.seek(0, 2)
    while True:
        li = file.readline()
        if not li:
            sleep(0.1)
            continue
        yield li


datafile = JsonFile(Data.DATAPATH)
statsdataobj = JsonFile(Data.STATSPATH)


def updateviauuid(uuid: str) -> None:
    global datafile
    profile = mapi.get_profile(uuid)
    data = datafile.load()
    data[uuid] = {
        "id": profile.id,
        "name": profile.name,
        "last_seen": ceil(float(profile.timestamp) / 1000),
        "first_time_seen": (
            ceil(float(profile.timestamp) / 1000)
            if uuid not in data
            else data[uuid]["first_time_seen"]
        ),
        "skin_variant": profile.skin_variant,
        "cape_url": None if profile.cape_url is None else profile.cape_url.replace("http://", "https://"),
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
    print(datafile.dumps(uuid))


def updatevianickname(nickname: str) -> None:
    if nickname != "*":
        data = datafile.load()
        data[nickname.lower()] = {
            "id": None,
            "name": nickname,
            "last_seen": ceil(time()),
            "first_time_seen": (
                ceil(time())
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
        print(datafile.dumps(nickname.lower()))


logo = rf"""{Fore.MAGENTA}____    ____   ______  ______           _            ______         __   __                _                   
{Fore.MAGENTA}|_   \  /   _|.' ___  ||_   _ `.        / |_        .' ___  |       [  | [  |              / |_                 
{Fore.MAGENTA}  |   \/   | / .'   \_|  | | `. \ ,--. `| |-',--.  / .'   \_|  .--.  | |  | | .---.  .---.`| |-' .--.   _ .--.  
{Fore.MAGENTA}  | |\  /| | | |         | |  | |`'_\ : | | `'_\ : | |       / .'`\ \| |  | |/ /__\\/ /'`\]| | / .'`\ \[ `/'`\] 
{Fore.MAGENTA} _| |_\/_| |_\ `.___.'\ _| |_.' /// | |,| |,// | |,\ `.___.'\| \__. || |  | || \__.,| \__. | |,| \__. | | |     
{Fore.MAGENTA}|_____||_____|`.____ .'|______.' \'-;__/\__/\'-;__/ `.____ .' '.__.'[___][___]'.__.''.___.'\__/ '.__.' [___]    """

if __name__ == "__main__":
    print(f"{Fore.GREEN}No errors found in {__file__}.")
