if __name__ == "__main__":
    raise Exception("Please don't run mcdatacollector package files.")

from time import sleep
from typing import TextIO, Generator

from colorama import Fore
from mojang import errors

from mcdatacollector import datafile, mapi, updateviauuid, updatevianickname, LOGPATH


def updatebynicknames():
    nicknames = list(
        map(
            str,
            input("Nicknames (split by space): ").split(),
        )
    )
    count = len(nicknames)
    for nickname in nicknames:
        try:
            uuid: str = mapi.get_uuid(nickname)

            updateviauuid(uuid)
            sleep(0.1)
        except errors.NotFound:
            count -= 1
            print(f"{Fore.RED}{nickname} doesn't exist.")
            continue
        sleep(0.25)
    print(f"Updated {count} players.")


returnupdatewithlist = False


def followupdatewithlist(file: TextIO) -> Generator[str, None, None]:
    global returnupdatewithlist
    """follows selected file, used only in update with /list"""
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

    logfile = open(
        LOGPATH,
        "r",
        encoding="UTF-8",
    )
    loglines = followupdatewithlist(logfile)
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
                        uuid: str = mapi.get_uuid(nickname)
                        updateviauuid(uuid)
                    except errors.NotFound:
                        updatevianickname(nickname)
                        continue
                    sleep(0.25)
                print(f"Updated {count} players.")
                return


def updateeveryonesdata():
    data = datafile.load()
    for uuid in data:
        if data[uuid]["id"] is not None:
            profile = mapi.get_profile(uuid)
            data[uuid] = {
                "id": profile.id,
                "name": profile.name,
                "last_seen": data[uuid]["last_seen"],
                "first_time_seen": data[uuid]["first_time_seen"],
                "skin_variant": profile.skin_variant,
                "cape_url": profile.cape_url,
                "skin_url": profile.skin_url,
                "db_id": data[uuid]["db_id"],
                "does_exist": True,
            }
            print(f"{Fore.GREEN}Updated {profile.name}")
            print(datafile.dumps(uuid))
            sleep(0.25)


def __httptohttps__():
    data = datafile.load()

    for uuid in data:
        if data[uuid]["id"] is not None:
            if data[uuid]["cape_url"] is not None:
                data[uuid]["cape_url"] = data[uuid]["cape_url"].replace("http://", "https://")
            data[uuid]["skin_url"] = data[uuid]["skin_url"].replace("http://", "https://")

    datafile.dump(data)
