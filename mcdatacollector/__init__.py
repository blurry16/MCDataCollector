__version__ = "dev1.4.0"

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
from logging import getLogger, basicConfig
from math import ceil
from os import name as osname, system, listdir, mkdir
from os.path import exists, isfile, isdir, splitext
from pathlib import Path
from time import sleep, time
from typing import Generator, TextIO, Callable

from colorama import init, Back, Fore
from dotenv import dotenv_values
from mojang import API

__dir = Path(__file__).parent.parent

init(autoreset=True)  # Colorama init

__logger = getLogger("mcdatacollector")
basicConfig()

if ".env" not in listdir("/".join(__file__.split("\\" if osname == "nt" else "/")[:-2])):
    __logger.warning(f".env file not found! Exceptions WILL be raised.")

__datafolder = __dir.joinpath("data/")
__dumpsfolder = __datafolder.joinpath("dumps/")
__csvfolder = __dumpsfolder.joinpath("csv/")

for i in [__datafolder, __dumpsfolder, __csvfolder, __csvfolder.joinpath("full"), __csvfolder.joinpath("misc")]:
    print(i)
    if not i.exists():
        mkdir(i)

DOTENV = dotenv_values(".env")


class Data:
    # Files
    try:
        LOGPATH = Path(DOTENV["LOG_PATH"])
        DATAPATH = Path(DOTENV["DATA_PATH"])
        STATSPATH = Path(DOTENV["STATS_PATH"])

        # Directories
        MODELSPATH = Path(DOTENV["MODELS_PATH"])
        SKINSPATH = Path(DOTENV["SKINS_PATH"])
        SKINSURLPATH = Path(DOTENV["SKINSURL_PATH"])
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
        if i != Path():
            if not exists(i):
                print(f"{Back.RED}{i} doesn't exist. Exceptions may be raised.")
                print(f"{Back.RED}Please change the value at .env")
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


mapi = API()  # Mojang API init

pause: Callable[[], int] = lambda: system("pause" if osname == "nt" else "")


class __JsonFile:
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


datafile = __JsonFile(Data.DATAPATH)
statsdataobj = __JsonFile(Data.STATSPATH)

__uuids = {}


def getuuid(nickname: str) -> str:
    """Stores UUIDs in a cache dictionary.\n
    Raises the 'mojang.errors.NotFound' exception if uuid wasn't found."""
    global __uuids
    if nickname not in __uuids:
        __uuids[nickname] = mapi.get_uuid(nickname)
    return __uuids[nickname]


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


__logo = rf"""{Fore.MAGENTA} ____    ____   ______  ______           _            ______         __   __                _                   
|_   \  /   _|.' ___  ||_   _ `.        / |_        .' ___  |       [  | [  |              / |_                 
  |   \/   | / .'   \_|  | | `. \ ,--. `| |-',--.  / .'   \_|  .--.  | |  | | .---.  .---.`| |-' .--.   _ .--.  
  | |\  /| | | |         | |  | |`'_\ : | | `'_\ : | |       / .'`\ \| |  | |/ /__\\/ /'`\]| | / .'`\ \[ `/'`\] 
 _| |_\/_| |_\ `.___.'\ _| |_.' /// | |,| |,// | |,\ `.___.'\| \__. || |  | || \__.,| \__. | |,| \__. | | |     
|_____||_____|`.____ .'|______.' \'-;__/\__/\'-;__/ `.____ .' '.__.'[___][___]'.__.''.___.'\__/ '.__.' [___]    """


def initializescript(script_name: str):
    print(f"Currently running mcdatacollector {__version__}.\n"
          f"{__logo}\n" +
          Fore.MAGENTA + f"{Fore.RESET + ' ' + script_name + ' ' + Fore.MAGENTA:=^121}\n")


if __name__ == "__main__":
    initializescript(__file__)
    print(f"{Fore.GREEN}No errors found in {__file__}.")
