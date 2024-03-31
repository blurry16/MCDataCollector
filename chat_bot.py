import keyboard
from time import time, sleep
from __data__ import cvdbdata, LOGPATH, follow
from datetime import datetime
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

banned = []
for i in range(len(banned)):
    banned[i] = banned[i].lower()

while True:
    LOGFILE = open(
        LOGPATH,
        "r",
        encoding="UTF-8",
    )
    lines = follow(LOGFILE)
    for line in lines:
        if "[CHAT]" in line:
            if line[40] == "<":
                match line.lower().split()[5]:
                    case "#lastseen":
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        arg = (
                            line.replace("\n", "").split(f"{command} ", 1)[1].split()[0]
                        )
                        if username.lower() not in banned:
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
                        print(line)
                        command = line.split()[5]
                        username = line.split()[4].split("<")[1].split(">")[0]
                        arg = (
                            line.replace("\n", "").split(f"{command} ", 1)[1].split()[0]
                        )
                        if username.lower() not in banned:
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
                        print(line)
                        username = line.split()[4].split("<")[1].split(">")[0]
                        if username.lower() not in banned:
                            data = cvdbdata.load()
                            mcprint(f"{len(data)} players are currently in the db.")
                    case "#getdbid":
                        print(line)
                        username = line.split()[4].split("<")[1].split(">")[0]
                        arg = (
                            line.replace("\n", "").split(f"{command} ", 1)[1].split()[0]
                        )
                        if username.lower() not in banned:
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
                                        f"{nickname}'s database ID is {data[uuid]['db_id']}"
                                    )
