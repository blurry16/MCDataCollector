__version__ = "dev1.4.0"  # MCDC version


class Config:
    custom_data_folder = None
    custom_main_data_path = None
    custom_stats_path = None


# Designed, developed & made by blurry16 & ...
# Contributions are welcome.
# I'll add you into the contributors list and I won't be a jerk.

# Licensed under MIT, Copyright (c) blurry16 2024-2025

# Small mark - MCDC stands for MCDataCollector or MinecraftDataCollector. All these names are equal.

from json import load, dump, dumps
from logging import getLogger, basicConfig
from math import ceil
from os import name as osname, system, listdir, mkdir
from pathlib import Path
from time import sleep, time
from typing import Generator, TextIO, Callable

from colorama import init, Fore
from dotenv import dotenv_values
from mojang import API

__logo = rf"""{Fore.MAGENTA} ____    ____   ______  ______           _            ______         __   __                _                   
|_   \  /   _|.' ___  ||_   _ `.        / |_        .' ___  |       [  | [  |              / |_                 
  |   \/   | / .'   \_|  | | `. \ ,--. `| |-',--.  / .'   \_|  .--.  | |  | | .---.  .---.`| |-' .--.   _ .--.  
  | |\  /| | | |         | |  | |`'_\ : | | `'_\ : | |       / .'`\ \| |  | |/ /__\\/ /'`\]| | / .'`\ \[ `/'`\] 
 _| |_\/_| |_\ `.___.'\ _| |_.' /// | |,| |,// | |,\ `.___.'\| \__. || |  | || \__.,| \__. | |,| \__. | | |     
|_____||_____|`.____ .'|______.' \'-;__/\__/\'-;__/ `.____ .' '.__.'[___][___]'.__.''.___.'\__/ '.__.' [___]    """

REPOURL = "https://github.com/blurry16/MCDataCollector"

__mcdc = Path(__file__).parent
__dir = __mcdc.parent

init(autoreset=True)  # Colorama init

__logger = getLogger("mcdatacollector")
basicConfig()

if ".env" not in listdir(__dir):
    __logger.warning(f".env file not found! Exceptions WILL be raised.")

DOTENV = dotenv_values(f"{__dir}/.env")

datafolder = Config.custom_data_folder if Config.custom_data_folder is not None else __dir.joinpath("data/")

dumpsfolder = datafolder.joinpath("dumps/")
csvfolder = dumpsfolder.joinpath("csv/")


class Data:
    __raw__ = DOTENV

    LOGPATH = Path(DOTENV["LOG_PATH"])
    DATAPATH = Path(Config.custom_main_data_path) if Config.custom_data_folder else datafolder.joinpath("data.json")
    STATSPATH = Path(Config.custom_stats_path) if Config.custom_stats_path else datafolder.joinpath("stats.json")

    picsfolder = datafolder.joinpath("pics/")

    # Directories
    HTMLPATH = picsfolder.joinpath("models/")
    SKINSPATH = picsfolder.joinpath("skins/")
    SKINSURLPATH = picsfolder.joinpath("skinsurl/")

    __files__: list = [DATAPATH, STATSPATH]  # Only files' paths
    __dirs__: list = [datafolder, dumpsfolder, csvfolder, csvfolder.joinpath("full"), csvfolder.joinpath("misc"),
                      picsfolder, HTMLPATH, SKINSURLPATH, SKINSPATH]  # Only directories' paths
    __paths__ = __files__ + __dirs__

    __tracker__: list = [LOGPATH, DATAPATH]
    __client__: list = [STATSPATH, HTMLPATH, SKINSPATH, SKINSURLPATH]


if not Data.LOGPATH.exists():
    raise Exception("Logpath doesn't exist.")

for i in Data.__dirs__:
    if not i.exists():
        mkdir(i)
for i in Data.__files__:
    if not i.exists():
        i.touch()
        with open(i, "w") as f:
            f.write("{}")

if not Data.DATAPATH.exists():
    Data.DATAPATH.touch()

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


def initializescript(script_name: str):
    print(f"Currently running {__mcdc.name} {__version__}.\n"
          f"{__logo}\n" +
          Fore.MAGENTA + f"{Fore.RESET + ' ' + script_name + ' ' + Fore.MAGENTA:=^121}\n")


if __name__ == "__main__":
    initializescript(__file__)
    print(f"{Fore.GREEN}No errors found in {__file__}.")
