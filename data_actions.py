import json
import os
import threading
from datetime import datetime, timedelta
from time import time

import keyboard
import requests
from mojang import errors

from mcdatacollector import *


def followupdatewithlist(file: TextIO) -> Generator[str, None, None]:
    global return_updatewithlist
    """follows selected file, used only in update with /list"""
    file.seek(0, 2)
    while True:
        if return_updatewithlist:
            return
        li = file.readline()
        if not li:
            sleep(0.1)
            continue
        yield li


def updatewithlist() -> None:
    global return_updatewithlist

    logfile = open(
        LOGPATH,
        "r",
        encoding="UTF-8",
    )
    loglines = followupdatewithlist(logfile)
    print(f"{Fore.MAGENTA}Waiting for /list...")
    for line in loglines:
        if "[CHAT]" in line:
            line_upd = line.split("[CHAT] ")[1]
            if line_upd.split()[0] == "Cubeville":
                nicknames = line_upd.split("): ")[1].split(", ")
                print(f"Updating: {', '.join(nicknames)}.".replace("\n", ""))
                count = len(nicknames)
                for nickname in nicknames:
                    nickname = nickname.strip()
                    data = cvdbdata.load()
                    try:
                        uuid: str = mapi.get_uuid(nickname)
                        updateviauuid(uuid)
                    except errors.NotFound:
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
                        cvdbdata.dump(data)
                        print(f"{Fore.GREEN}{nickname}'s dictionary was updated/added.")
                        print(
                            json.dumps(
                                data[nickname.lower()],
                                indent=2,
                            )
                        )
                        continue
                    sleep(0.25)
                print(f"Updated {count} players.")
                return_updatewithlist = True
                return


while True:
    inp = input(
        "1. Get data.\n"
        "2. Save skins.\n"
        "3. Update data.\n"
        "4. Add stats\n"
        "5. Quit\n"
    ).strip()
    match inp:
        case "1":
            while True:
                inp = input(
                    "1. Get last seen time\n"
                    "2. Get first seen time\n"
                    "3. Get full data in JSON format\n"
                    "4. Get database id\n"
                    "5. Get all players' nicknames in the DB\n"
                    "6. Get all zombie accounts nicknames in the DB\n"
                    "7. Get back to previous stage\n"
                ).strip()
                try:
                    match inp:
                        case "1":
                            arg = input(
                                "Lookup via [1] Nickname, [2] Mojang UUID, [3] DBID: "
                            ).strip()
                            data = cvdbdata.load()
                            try:
                                if arg == "1":
                                    nickname = input("Nickname: ").strip().split()[0]
                                    try:
                                        local_uuid = mapi.get_uuid(nickname)
                                        if local_uuid in data:
                                            local_data = data[local_uuid]
                                            dt_obj = datetime.fromtimestamp(
                                                local_data["last_seen"]
                                            )
                                            print(
                                                f"{local_data['name']} was seen at {dt_obj}. "
                                                f"({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
                                            )
                                        else:
                                            print(f"The bot has never seen {nickname}.")
                                    except errors.NotFound:
                                        if nickname in data:
                                            local_data = data[nickname]
                                            dt_obj = datetime.fromtimestamp(
                                                local_data["last_seen"]
                                            )
                                            print(
                                                f"{local_data['name']} was seen at {dt_obj}. "
                                                f"({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
                                            )
                                        else:
                                            print("This player doesn't exist.")
                                elif arg == "2":
                                    local_uuid = (
                                        input("UUID: ")
                                        .strip()
                                        .replace("-", "")
                                        .split()[0]
                                    )
                                    if local_uuid in data:
                                        local_data = data[local_uuid]
                                        dt_obj = datetime.fromtimestamp(
                                            local_data["last_seen"]
                                        )
                                        print(
                                            f"{local_data['name']} ({local_data['id']}) was seen at {dt_obj}. "
                                            f"({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
                                        )
                                    else:
                                        print(f"The bot has never seen {local_uuid}.")
                                elif arg == "3":
                                    try:
                                        db_id = int(input("DBID: ").strip().split()[0])
                                        local_data = data[list(data)[db_id]]
                                        dt_obj = datetime.fromtimestamp(
                                            local_data["last_seen"]
                                        )
                                        print(
                                            f"{local_data['name']} ({local_data['db_id']}) was seen at {dt_obj}. "
                                            f"({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
                                        )

                                    except ValueError:
                                        print(f"{Fore.RED}Wrong value!")
                                    except IndexError:
                                        print(
                                            f"{Fore.RED}DB has no player with this DBID."
                                        )
                                else:
                                    print(f"{Fore.RED}Unknown command!")
                            except IndexError:
                                print(f"{Fore.RED}Not enough arguments!")
                        case "2":
                            arg = input(
                                "Lookup via [1] Nickname, [2] Mojang UUID, [3] DBID: "
                            ).strip()
                            data = cvdbdata.load()
                            try:
                                if arg == "1":
                                    nickname = input("Nickname: ").strip().split()[0]
                                    try:
                                        local_uuid = mapi.get_uuid(nickname)
                                        if local_uuid in data:
                                            local_data = data[local_uuid]
                                            timestamp = local_data["first_time_seen"]
                                            print(
                                                f"{local_data['name']} was seen for the first time at "
                                                f"{datetime.fromtimestamp(timestamp)}. "
                                                f"({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(local_data['first_time_seen'])} ago)"
                                            )
                                        else:
                                            print(f"The bot has never seen {nickname}.")
                                    except errors.NotFound:
                                        if nickname in data:
                                            local_data = data[nickname]
                                            timestamp = local_data["first_time_seen"]
                                            print(
                                                f"{local_data['name']} was seen for the first time at "
                                                f"{datetime.fromtimestamp(timestamp)}. "
                                                f"({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(local_data['first_time_seen'])} ago)"
                                            )
                                        else:
                                            print("This player doesn't exist.")
                                elif arg == "2":
                                    local_uuid = (
                                        input("UUID: ")
                                        .strip()
                                        .split()[0]
                                        .replace("-", "")
                                    )
                                    if local_uuid in data:
                                        local_data = data[local_uuid]
                                        dt_obj = datetime.fromtimestamp(
                                            local_data["first_time_seen"]
                                        )
                                        print(
                                            f"{local_data['name']} ({local_data['id']}) was seen at {dt_obj}. "
                                            f"({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
                                        )
                                    else:
                                        print(f"The bot has never seen {local_uuid}.")
                                elif arg == "3":
                                    try:
                                        db_id = int(input("DBID: ").strip().split()[0])
                                        local_data = data[list(data)[db_id]]
                                        dt_obj = datetime.fromtimestamp(
                                            local_data["first_time_seen"]
                                        )
                                        print(
                                            f"{local_data['name']} ({local_data['db_id']}) was seen at {dt_obj}. "
                                            f"({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
                                        )

                                    except ValueError:
                                        print(f"{Fore.RED}Wrong value!")
                                    except IndexError:
                                        print(
                                            f"{Fore.RED}DB has no player with this DBID."
                                        )
                                else:
                                    print(f"{Fore.RED}Unknown command!")
                            except IndexError:
                                print(f"{Fore.RED}Not enough arguments!")
                        case "3":
                            arg = input(
                                "Lookup via [1] Nickname, [2] Mojang UUID, [3] DBID: "
                            ).strip()
                            indent = 2
                            data = cvdbdata.load()
                            try:
                                if arg == "1":
                                    inp = input("Nickname: ").strip().split()[0]
                                    nickname = inp.split()[0]
                                    try:
                                        if "--indent" in inp.split():
                                            try:
                                                indent = int(
                                                    inp.split()[
                                                        inp.split().index("--indent")
                                                        + 1
                                                        ]
                                                )
                                            except IndexError:
                                                indent = None
                                            except ValueError:
                                                pass
                                        local_uuid = mapi.get_uuid(nickname)
                                        if local_uuid in data:
                                            print(
                                                json.dumps(
                                                    data[local_uuid], indent=indent
                                                )
                                            )
                                        else:
                                            print(f"The bot has never seen {nickname}.")
                                    except errors.NotFound:
                                        if nickname in data:
                                            print(
                                                json.dumps(
                                                    data[nickname], indent=indent
                                                )
                                            )
                                        else:
                                            print("This player doesn't exist.")
                                elif arg == "2":
                                    inp = input("UUID: ").strip()
                                    uuid = inp.split()[0].replace("-", "")
                                    if "--indent" in inp.split():
                                        try:
                                            indent = int(
                                                inp.split()[
                                                    inp.split().index("--indent") + 1
                                                    ]
                                            )
                                        except IndexError:
                                            indent = None
                                        except ValueError:
                                            pass
                                    if uuid in data:
                                        print(json.dumps(data[uuid], indent=indent))
                                    else:
                                        print(f"The bot has never seen {uuid}.")
                                elif arg == "3":
                                    try:
                                        inp = input("DBID: ")
                                        if "--indent" in inp.split():
                                            try:
                                                indent = int(
                                                    inp.split()[
                                                        inp.split().index("--indent")
                                                        + 1
                                                        ]
                                                )
                                            except IndexError:
                                                indent = None
                                            except ValueError:
                                                pass
                                        db_id = int(inp.split()[0])

                                        print(
                                            json.dumps(
                                                data[list(data)[db_id]], indent=indent
                                            )
                                        )
                                    except ValueError:
                                        print(f"{Fore.RED}Wrong value!")
                                    except IndexError:
                                        print(
                                            f"{Fore.RED}DB has no player with this DBID."
                                        )
                                else:
                                    print(
                                        f"{Fore.RED}DB has no player with {db_id} DBID."
                                    )
                            except IndexError:
                                print(f"{Fore.RED}Not enough arguments!")
                        case "4":
                            arg = input(
                                "Lookup via [1] Nickname, [2] Mojang UUID: "
                            ).strip()
                            data = cvdbdata.load()
                            try:
                                if arg == "1":
                                    inp = input("Nickname: ").lower().strip().split()[0]
                                    try:
                                        uuid = mapi.get_uuid(inp)
                                        nickname = data[uuid]["name"]
                                        if uuid in data:
                                            print(
                                                f"{nickname}'s database id is {data[uuid]['db_id']}."
                                            )
                                        else:
                                            print(f"The bot has never seen {nickname}.")
                                    except errors.NotFound:
                                        if inp.lower() in data:
                                            local_data = data[inp]
                                            print(
                                                f"{local_data['name']}'s database id is {local_data['db_id']}"
                                            )
                                elif arg == "2":
                                    local_uuid = (
                                        input("UUID: ")
                                        .strip()
                                        .split()[0]
                                        .replace("-", "")
                                    )
                                    if local_uuid in data:
                                        print(
                                            f"{local_uuid}'s ({data[local_uuid]['name']}) database id is "
                                            f"{data[local_uuid]['db_id']}"
                                        )
                                    else:
                                        print(f"The bot has never seen {nickname}.")
                            except IndexError:
                                print(f"{Fore.RED}Not enough arguments!")

                        case "5":
                            data = cvdbdata.load()
                            for i in data:
                                print(data[i]["name"])
                            print(f"{len(data)} players in DB")

                        case "6":
                            data = cvdbdata.load()
                            count = 0
                            for i in data:
                                if i == data[i]["name"].lower():
                                    count += 1
                                    print(data[i]["name"])
                            print(f"{count} zombies in the DB")

                        case "7":
                            break

                        case _:
                            print(f"{Fore.RED}Unknown command.")
                except KeyError:
                    print("The bot has never seen this player.")

        case "2":
            while True:
                mode = input(
                    "1. URL\n"
                    "2. Name\n"
                    "3. HTML model\n"
                    "4. Get back to previous stage.\n"
                )
                data = cvdbdata.load()
                if mode == "1":
                    foldername = rf"{SKINSURLPATH}\{datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')}"
                    print(f"{Fore.GREEN}Creating new folder... ({foldername})")
                    os.mkdir(foldername)
                    print(f"{Fore.GREEN}Folder {foldername} created successfully.")
                    print(f"{Fore.GREEN}Saving new files...")
                    for i in data:
                        url = data[i]["skin_url"]
                        if url is not None:
                            response = requests.get(url=url)
                            with open(rf"{SKINSURLPATH}\{url[38:]}.png", "wb") as file:
                                file.write(response.content)
                            print(f"{Fore.GREEN}Saved {url[38:]}.png")
                        sleep(0.5)
                elif mode == "2":
                    foldername = rf"{SKINSPATH}\{datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')}"
                    print(f"{Fore.GREEN}Creating new folder... ({foldername})")
                    os.mkdir(foldername)
                    print(f"{Fore.GREEN}Folder {foldername} created successfully.")
                    print(f"{Fore.GREEN}Saving new files...")
                    for i in data:
                        url = data[i]["skin_url"]
                        if url is not None:
                            response = requests.get(url=url)
                            name = data[i]["name"]
                            with open(
                                    rf"{foldername}\{name}.png",
                                    "wb",
                            ) as file:
                                file.write(response.content)
                            print(f"{Fore.GREEN}Saved {name}.png")
                        sleep(0.5)
                    del foldername

                elif mode == "3":
                    foldername = rf"{MODELSPATH}\{datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')}"
                    print(f"{Fore.GREEN}Creating new folder... ({foldername})")
                    os.mkdir(foldername)
                    print(f"{Fore.GREEN}Folder {foldername} created successfully.")
                    print(f"{Fore.GREEN}Saving new files...")
                    for i in data:
                        if data[i]["does_exist"]:
                            name = data[i]["name"]
                            to_save = rf'<iframe src="https://minerender.org/embed/skin/?skin={name}&shadow=true" \
                            frameborder="0" width="1920px" height="972px"></iframe>'
                            with open(rf"{foldername}\{name}.html", "x") as file:
                                file.write(to_save)
                            print(f"{Fore.GREEN}Saved {name}.html")
                    del foldername
                elif mode == "4":
                    break
                else:
                    print(f"{Fore.RED}Unknown command.")
        case "3":
            while True:
                a = input(
                    "1. By nicknames\n"
                    "2. With /list\n"
                    "3. Everyone's data (last time seen won't be touched)\n"
                    "4. Get back to previous stage.\n"
                )
                match a:
                    case "1":
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
                                profile = mapi.get_profile(uuid)
                                data: dict = cvdbdata.load()
                                updateviauuid(uuid)
                                sleep(0.1)
                            except errors.NotFound:
                                count -= 1
                                print(f"{Fore.RED}{nickname} doesn't exist.")
                                continue
                            sleep(0.25)
                        print(f"Updated {count} players.")

                    case "2":
                        return_updatewithlist = False
                        updatewithlistthread = threading.Thread(target=updatewithlist)
                        updatewithlistthread.start()
                        sleep(0.01)
                        print(f"{Fore.MAGENTA}Press escape to break updating")
                        while True:
                            if keyboard.is_pressed("escape"):
                                return_updatewithlist = True
                                updatewithlistthread.join()
                                break
                            if return_updatewithlist:
                                break

                    case "3":
                        data = cvdbdata.load()
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
                                print(json.dumps(data[uuid], indent=2))
                                sleep(0.25)

                    case "4":
                        break
                    case _:
                        print(f"{Fore.RED}Unknown command.")

        case "4":
            data_len = len(cvdbdata.load())
            statsdata = statsdataobj.load()
            # prev_date = (datetime.now().date() - timedelta(days=2)).strftime("%Y-%m-%d")
            last_date = list(statsdata)[-1]
            now_date = (datetime.now().date() - timedelta(days=1)).strftime("%Y-%m-%d")
            statsdata[now_date] = {
                "count": data_len,
                "delta": data_len - int(statsdata[last_date]["count"]),
            }

            print(json.dumps(statsdata, indent=4))
            a = input(f"{Fore.MAGENTA}Proceed? y/n: ")
            if a.lower() == "y" or a == "":
                statsdataobj.dump(statsdata)
            print(Fore.RESET)

        case "5":
            break

        case _:
            print(f"{Fore.RED}Unknown command.")
