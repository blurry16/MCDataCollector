import time
import json
import random
import keyboard
from datetime import datetime
from colorama import Fore
from mojang import API, errors
from __data__ import cvdbdata, LOGPATH, follow


def mcprint(text: str):
    """prints given text on the keyboard and sends it to minecraft chat"""
    keyboard.press_and_release("t")
    time.sleep(0.1)
    keyboard.write(text, delay=0)
    time.sleep(0.5)
    keyboard.press_and_release("enter")


def generatepasscode() -> str:
    __PASSCODE__ = str(random.randint(0, 9999))
    return "0" * (4 - len(__PASSCODE__)) + __PASSCODE__


mapi = API()

startday = datetime.now().day

CHATBOTACTIVE = False
HOST = "blurry16"
BANNED = []
PASSCODE = generatepasscode()
print(f"{Fore.MAGENTA}Chatbot passcode for this session is: {PASSCODE}")

while True:
    LOGFILE = open(
        LOGPATH,
        "r",
        encoding="UTF-8",
    )
    lines = follow(LOGFILE)
    for line in lines:
        if datetime.now().day != startday:
            raise Exception(
                f"{Fore.RED}The program may stop working properly. Please, restart it. (The problem is known and will be fixed once I get an idea of its fix)"
            )
        if "[CHAT]" in line:
            if line[40] == "<":
                if line.lower().split()[5] == "#activate":
                    command = line.split()[5]
                    username = line.split()[4].split("<")[1].split(">")[0]
                    try:
                        arg = (
                            line.replace("\n", "").split(f"{command} ", 1)[1].split()[0]
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
                                            f"{data[uuid]['name']} was seen for the last time at {datetime.fromtimestamp(data[uuid]['last_seen'])} UTC+3. ({datetime.fromtimestamp(round(time.time())) - datetime.fromtimestamp(data[uuid]['last_seen'])} ago)"
                                        )
                                except errors.NotFound:
                                    arg = arg.lower()
                                    if arg not in data:
                                        mcprint("This player doesn't exist.")
                                    else:
                                        mcprint(
                                            f"{data[arg]['name']} was seen for the last time at {datetime.fromtimestamp(data[arg]['last_seen'])} UTC+3. ({datetime.fromtimestamp(round(time.time())) - datetime.fromtimestamp(data[arg]['last_seen'])})"
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
                                            f"{data[uuid]['name']} was seen for the first time at {datetime.fromtimestamp(data[uuid]['first_time_seen'])} UTC+3. ({datetime.fromtimestamp(round(time.time())) - datetime.fromtimestamp(data[uuid]['first_time_seen'])} ago)"
                                        )
                                except errors.NotFound:
                                    arg = arg.lower()
                                    if arg not in data:
                                        mcprint("This player doesn't exist.")
                                    else:
                                        mcprint(
                                            f"{data[arg]['name']} was seen for the first time at {datetime.fromtimestamp(data[arg]['first_time_seen'])} UTC+3. ({datetime.fromtimestamp(round(time.time())) - datetime.fromtimestamp(data[arg]['first_time_seen'])} ago)"
                                        )

                        case "#count":
                            print(f"{Fore.MAGENTA}{line}".replace("\n", ""))
                            username = line.split()[4].split("<")[1].split(">")[0]
                            if username.lower() not in BANNED:
                                data = cvdbdata.load()
                                mcprint(f"{len(data)} players are currently in the db.")
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
                                        mcprint(f"{nickname} is not in the database.")
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
                                    "last_seen": int(time.time()),
                                    "first_time_seen": (
                                        int(time.time())
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
                                print(f"{Fore.GREEN}{nickname}'s dictionary updated.")
                                print(json.dumps(data[nickname.lower()], indent=2))
                        except Exception as e:
                            print(f"Exception {e} occurred at {int(time.time())}.")
                        print("\n")
