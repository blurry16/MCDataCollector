import time
from datetime import datetime

import keyboard
from colorama import Fore
from mojang import errors

from mcdatacollector import datafile, getuuid, initializescript, __logger

CHATBOTBANNED = []


def mcprint(text: str) -> None:
    """prints given text on the keyboard and sends it to minecraft chat"""
    keyboard.press_and_release("t")
    time.sleep(0.1)
    keyboard.write(text, delay=0)
    time.sleep(0.5)
    keyboard.press_and_release("enter")


def getusernamearg(__line: str) -> tuple[str, str]:
    print(f"{Fore.MAGENTA}{__line}".replace("\n", ""))
    __command = __line.split()[5]
    __username = __line.split()[4].split("<")[1].split(">")[0]
    __arg = (
        __line.replace("\n", "")
        .split(f"{__command} ", 1)[1]
        .split()[0]
    )
    return __username, __arg


def lastseen(line: str):
    username, arg = getusernamearg(line)
    if username.lower() not in CHATBOTBANNED:
        data = datafile.load()
        try:
            uuid = getuuid(arg)
            if uuid not in data:
                mcprint(f"The bot has never seen {arg}.")
            else:
                mcprint(
                    f"{data[uuid]['name']} was seen for the last time at "
                    f"{datetime.fromtimestamp(data[uuid]['last_seen'])} UTC+3. "
                    f"({datetime.fromtimestamp(round(time.time())) -
                        datetime.fromtimestamp(data[uuid]['last_seen'])} ago)"
                )
        except errors.NotFound:
            arg = arg.lower()
            if arg not in data:
                mcprint("This player doesn't exist.")
            else:
                mcprint(
                    f"{data[arg]['name']} was seen for the last time at "
                    f"{datetime.fromtimestamp(data[arg]['last_seen'])} UTC+3. "
                    f"({datetime.fromtimestamp(round(time.time())) -
                        datetime.fromtimestamp(data[arg]['last_seen'])})"
                )


def firsttimeseen(line: str):
    username, arg = getusernamearg(line)
    if username.lower() not in CHATBOTBANNED:
        data = datafile.load()
        try:
            uuid = getuuid(arg)
            if uuid not in data:
                mcprint(f"The bot has never seen {arg}.")
            else:
                mcprint(
                    f"{data[uuid]['name']} was seen for the first time at "
                    f"{datetime.fromtimestamp(data[uuid]['first_time_seen'])} UTC+3. "
                    f"({datetime.fromtimestamp(round(time.time())) -
                        datetime.fromtimestamp(data[uuid]['first_time_seen'])} ago)"
                )
        except errors.NotFound:
            arg = arg.lower()
            if arg not in data:
                mcprint("This player doesn't exist.")
            else:
                mcprint(
                    f"{data[arg]['name']} was seen for the first time at "
                    f"{datetime.fromtimestamp(data[arg]['first_time_seen'])} UTC+3. "
                    f"({datetime.fromtimestamp(round(time.time())) -
                        datetime.fromtimestamp(data[arg]['first_time_seen'])} ago)"
                )


def count(line: str):
    print(f"{Fore.MAGENTA}{line}".replace("\n", ""))
    username = line.split()[4].split("<")[1].split(">")[0]
    if username.lower() not in CHATBOTBANNED:
        data = datafile.load()
        mcprint(f"{len(data)} players are currently in the db.")


def getdbid(line: str):
    print(f"{Fore.MAGENTA}{line}".replace("\n", ""))
    username = line.split()[4].split("<")[1].split(">")[0]
    command = line.split()[5]
    arg = (
        line.replace("\n", "")
        .split(f"{command} ")[1]
        .split()[0]
    )
    if username.lower() not in CHATBOTBANNED:
        data = datafile.load()
        try:
            uuid = getuuid(arg)
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


if __name__ == "__main__":
    initializescript(__file__)
    __logger.info(f"{Fore.GREEN}No errors found in {__file__}.")
