from time import sleep
from typing import TextIO, Generator

from colorama import Fore

import mcdatacollector.mojang as mcdcapi
from mcdatacollector import datafile, updateviauuid, updatevianickname, Data, getuuid, initializescript, __logger


def updatebynicknames():
    nicknames = input("Nicknames (split by space): ").split()
    count = len(nicknames)
    for nickname in nicknames:
        try:
            uuid: str = getuuid(nickname)

            updateviauuid(uuid)
            sleep(0.1)
        except mcdcapi.NotFoundException:
            count -= 1
            print(f"{Fore.RED}{nickname} doesn't exist.")
            continue
        sleep(0.25)
    print(f"Updated {count} players.")


returnupdatewithlist = False


def __follow(file: TextIO) -> Generator[str, None, None]:
    """follows selected file, used only in update with /list"""
    global returnupdatewithlist
    file.seek(0, 2)
    while True:
        try:
            li = file.readline()
            if not li:
                sleep(0.1)
                continue
            yield li
        except KeyboardInterrupt:
            returnupdatewithlist = True
            return


def updatewithlist() -> None:
    global returnupdatewithlist

    logfile = open(Data.LOGPATH, "r", encoding="UTF-8")
    loglines = __follow(logfile)
    print(f"{Fore.MAGENTA}Waiting for /list...\nDo CTRL+C do break updating.")
    for line in loglines:
        if returnupdatewithlist:
            return
        if "[CHAT]" in line:
            line_upd = line.split("[CHAT] ")[1]
            if line_upd.split()[0] == "Cubeville":
                nicknames = line_upd.split("): ")[1].split(", ")
                print(f"Updating: {', '.join(nicknames)}.".replace("\n", ""))
                count = len(nicknames)
                for nickname in nicknames:
                    nickname = nickname.strip()
                    try:
                        uuid: str = getuuid(nickname)
                        updateviauuid(uuid)
                    except mcdcapi.NotFoundException:
                        updatevianickname(nickname)
                        continue
                    sleep(0.25)
                print(f"Updated {count} players.")
                return


def updateeveryonesdata():
    data = datafile.load()
    datalen = len(data)
    for index, uuid in enumerate(data):
        if data[uuid]["id"] is not None:
            profile = mcdcapi.get_profile(uuid)
            data[uuid] = {
                "id": profile.id,
                "name": profile.name,
                "last_seen": data[uuid]["last_seen"],
                "first_time_seen": data[uuid]["first_time_seen"],
                "skin_variant": profile.skin_variant,
                "cape_url": None if profile.cape_url is None else profile.cape_url.replace("http://", "https://"),
                "skin_url": profile.skin_url.replace("http://", "https://"),
                "db_id": data[uuid]["db_id"],
                "does_exist": True,
            }
            print(f"{Fore.GREEN}Updated {profile.name} [{index + 1}/{datalen}]")
            print(datafile.dumps(uuid))
            sleep(0.25)
    datafile.dump(data)


def __httptohttps__():
    data = datafile.load()

    for uuid in data:
        if data[uuid]["id"] is not None:
            if data[uuid]["cape_url"] is not None:
                data[uuid]["cape_url"] = data[uuid]["cape_url"].replace("http://", "https://")
            data[uuid]["skin_url"] = data[uuid]["skin_url"].replace("http://", "https://")
            __logger.info(f"Updated {data[uuid]['name']} [{uuid}]")
    datafile.dump(data)
    __logger.info(f"Updated & Dumped to JSON {len(data)} players.")


__httptohttps__()

if __name__ == "__main__":
    initializescript(__file__)
    print(f"{Fore.GREEN}No errors found in {__file__}.")
