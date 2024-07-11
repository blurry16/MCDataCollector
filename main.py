import requests
import os
import keyboard
import random
import threading
from time import time, sleep
from colorama import Fore
from __data__ import *
from datetime import datetime, timedelta
from mojang import API, errors

mapi = API()


def mcprint(text: str):
    """prints given text on the keyboard and sends it to minecraft chat"""
    keyboard.press("T")
    sleep(0.001)
    keyboard.release("T")
    sleep(0.1)
    keyboard.write(text, delay=0)
    sleep(0.5)
    keyboard.press_and_release("enter")


def generatepasscode() -> str:
    __PASSCODE__ = str(random.randint(0, 9999))
    return "0" * (4 - len(__PASSCODE__)) + __PASSCODE__


is_collecting_active = False


def follow(file):
    """follows selected file, used in data collecting not updating via /list"""
    global is_collecting_active
    file.seek(0, 2)
    while True:
        if not is_collecting_active:
            break
        li = file.readline()
        if not li:
            sleep(0.1)
            continue
        yield li


def followupdatewithlist(file):
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


def updatewithlist():
    global return_updatewithlist

    LOGFILE = open(
        LOGPATH,
        "r",
        encoding="UTF-8",
    )
    loglines = followupdatewithlist(LOGFILE)
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
                        uuid = mapi.get_uuid(nickname)
                        profile = mapi.get_profile(uuid)
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
                                len(data) if uuid not in data else data[uuid]["db_id"]
                            ),
                            "does_exist": True,
                        }
                        cvdbdata.dump(data)
                        print(
                            f"{Fore.GREEN}{profile.name}'s dictionary was updated/added."
                        )
                        print(json.dumps(data[uuid], indent=2))
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


def collectdata():
    PASSCODE = generatepasscode()
    CHATBOTACTIVE = False
    HOST = "blurry16"
    BANNED = []
    global is_collecting_active
    print(f"{Fore.MAGENTA}Chatbot passcode for this session is: {PASSCODE}")
    while True:
        LOGFILE = open(
            LOGPATH,
            "r",
            encoding="UTF-8",
        )
        lines = follow(LOGFILE)
        if not is_collecting_active:
            return
        for line in lines:
            if "[CHAT]" in line:
                if line[40] == "<":
                    if line.lower().split()[5] == "#activate":
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        try:
                            arg = (
                                line.replace("\n", "")
                                .split(f"{command} ", 1)[1]
                                .split()[0]
                            )
                            if username == HOST and arg == PASSCODE:
                                CHATBOTACTIVE = not CHATBOTACTIVE
                                print(
                                    f"{Fore.GREEN}Chatbot activated."
                                    if CHATBOTACTIVE
                                    else f"{Fore.RED}Chatbot unactivated."
                                )
                        except IndexError:
                            if username == HOST:
                                print(f"{Fore.MAGENTA}Not enough arguments!")
                    elif CHATBOTACTIVE:
                        match line.lower().split()[5]:
                            case "#lastseen":
                                print(f"{Fore.MAGENTA}{line}".replace("\n", ""))
                                command = line.split()[5]
                                username = line.split()[4].split("<")[1].split(">")[0]
                                arg = (
                                    line.replace("\n", "")
                                    .split(f"{command} ", 1)[1]
                                    .split()[0]
                                )
                                if username.lower() not in BANNED:
                                    data = cvdbdata.load()
                                    try:
                                        uuid = mapi.get_uuid(arg)
                                        if uuid not in data:
                                            mcprint(f"The bot has never seen {arg}.")
                                        else:
                                            mcprint(
                                                f"{data[uuid]['name']} was seen for the last time at {datetime.fromtimestamp(data[uuid]['last_seen'])} UTC+3. ({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(data[uuid]['last_seen'])} ago)"
                                            )
                                    except errors.NotFound:
                                        arg = arg.lower()
                                        if arg not in data:
                                            mcprint("This player doesn't exist.")
                                        else:
                                            mcprint(
                                                f"{data[arg]['name']} was seen for the last time at {datetime.fromtimestamp(data[arg]['last_seen'])} UTC+3. ({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(data[arg]['last_seen'])})"
                                            )
                            case "#firsttimeseen":
                                print(f"{Fore.MAGENTA}{line}".replace("\n", ""))
                                command = line.split()[5]
                                username = line.split()[4].split("<")[1].split(">")[0]
                                arg = (
                                    line.replace("\n", "")
                                    .split(f"{command} ", 1)[1]
                                    .split()[0]
                                )
                                if username.lower() not in BANNED:
                                    data = cvdbdata.load()
                                    try:
                                        uuid = mapi.get_uuid(arg)
                                        if uuid not in data:
                                            mcprint(f"The bot has never seen {arg}.")
                                        else:
                                            mcprint(
                                                f"{data[uuid]['name']} was seen for the first time at {datetime.fromtimestamp(data[uuid]['first_time_seen'])} UTC+3. ({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(data[uuid]['first_time_seen'])} ago)"
                                            )
                                    except errors.NotFound:
                                        arg = arg.lower()
                                        if arg not in data:
                                            mcprint("This player doesn't exist.")
                                        else:
                                            mcprint(
                                                f"{data[arg]['name']} was seen for the first time at {datetime.fromtimestamp(data[arg]['first_time_seen'])} UTC+3. ({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(data[arg]['first_time_seen'])} ago)"
                                            )

                            case "#count":
                                print(f"{Fore.MAGENTA}{line}".replace("\n", ""))
                                username = line.split()[4].split("<")[1].split(">")[0]
                                if username.lower() not in BANNED:
                                    data = cvdbdata.load()
                                    mcprint(
                                        f"{len(data)} players are currently in the db."
                                    )
                            case "#getdbid":
                                print(f"{Fore.MAGENTA}{line}".replace("\n", ""))
                                username = line.split()[4].split("<")[1].split(">")[0]
                                command = line.split()[5]
                                arg = (
                                    line.replace("\n", "")
                                    .split(f"{command} ")[1]
                                    .split()[0]
                                )
                                if username.lower() not in BANNED:
                                    data = cvdbdata.load()
                                    try:
                                        uuid = mapi.get_uuid(arg)
                                        nickname = data[uuid]["name"]
                                        if uuid not in data:
                                            mcprint(
                                                f"{nickname} is not in the database."
                                            )
                                        else:
                                            mcprint(
                                                f"{nickname}'s database ID is {data[uuid]['db_id']}"
                                            )
                                    except errors.NotFound:
                                        arg = arg.lower()
                                        if arg not in data:
                                            mcprint("This player doesn't exist.")
                                        else:
                                            nickname = data[arg]["name"]
                                            mcprint(
                                                f"{nickname}'s database ID is {data[arg]['db_id']}"
                                            )

                else:
                    line_upd = line.split("CHAT")[1]
                    split = line_upd.split()
                    if len(split) > 2:
                        if (
                            "<" not in line_upd
                            and "[" not in line_upd
                            and ("joined" == split[2] or "left" == split[2])
                            and "the" == split[3]
                            and "game." == split[4]
                        ):
                            data = cvdbdata.load()
                            nickname = line.split("[CHAT]")[1].split()[0]
                            try:
                                uuid = mapi.get_uuid(nickname)
                                profile = mapi.get_profile(uuid)
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
                                print(f"{Fore.GREEN}{nickname}'s dictionary updated.")
                                print(json.dumps(data[uuid], indent=2))
                            except errors.NotFound:
                                if nickname != "*":
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
                                    print(
                                        f"{Fore.GREEN}{nickname}'s dictionary updated."
                                    )
                                    print(json.dumps(data[nickname.lower()], indent=2))
                            except Exception as e:
                                print(f"Exception {e} occurred at {int(time())}.")
                            print("\n")


while True:
    inp = input(
        f"1. Get data.\n2. Save skins.\n3. Update data.\n4. Add stats\n5. {'Start' if not is_collecting_active else 'Stop'} collecting data & chatbot\n6. Quit\n"
    )
    match inp:
        case "1":
            while True:
                inp = input(
                    "1. Get last seen time\n2. Get first seen time\n3. Get full data in JSON format\n4. Get database id\n5. Get all players' nicknames in the DB\n6. Get all zombie accounts nicknames in the DB\n7. Get back to previous stage\n"
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
                                                f"{local_data['name']} was seen at {dt_obj} UTC+3. ({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
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
                                                f"{local_data['name']} was seen at {dt_obj} UTC+3. ({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
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
                                            f"{local_data['name']} ({local_data['id']}) was seen at {dt_obj} UTC+3. ({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
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
                                            f"{local_data['name']} ({local_data['db_id']}) was seen at {dt_obj} UTC+3. ({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
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
                                                f"{local_data['name']} was seen for the first time at {datetime.fromtimestamp(timestamp)} UTC+3. ({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(local_data['first_time_seen'])} ago)"
                                            )
                                        else:
                                            print(f"The bot has never seen {nickname}.")
                                    except errors.NotFound:
                                        if nickname in data:
                                            local_data = data[nickname]
                                            timestamp = local_data["first_time_seen"]
                                            print(
                                                f"{local_data['name']} was seen for the first time at {datetime.fromtimestamp(timestamp)} UTC+3. ({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(local_data['first_time_seen'])} ago)"
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
                                            f"{local_data['name']} ({local_data['id']}) was seen at {dt_obj} UTC+3. ({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
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
                                            f"{local_data['name']} ({local_data['db_id']}) was seen at {dt_obj} UTC+3. ({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
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
                                            f"{local_uuid}'s ({data[local_uuid]['name']}) database id is {data[local_uuid]['db_id']}"
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
                    "1. URL\n2. Name\n3. HTML model\n4. Get back to previous stage.\n"
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
                                (rf"{foldername}\{name}.png"),
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
                        name = data[i]["name"]
                        to_save = rf'<iframe src="https://minerender.org/embed/skin/?skin={name}&shadow=true" frameborder="0" width="1920px" height="972px"></iframe>'
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
                    "1. By nicknames\n2. With /list\n3. Everyone's data (last time seen won't be touched)\n4. Get back to previous stage.\n"
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
                                uuid = mapi.get_uuid(nickname)
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
            is_collecting_active = not is_collecting_active
            if is_collecting_active:
                print(f"{Fore.GREEN}Starting collecting data...")
                collectdatathread = threading.Thread(target=collectdata)
                collectdatathread.start()
            else:
                print(f"{Fore.RED}Stopping collecting data...")
                collectdatathread.join()
        case "6":
            break

        case _:
            print(f"{Fore.RED}Unknown command.")
