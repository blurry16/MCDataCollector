# Imports
import random

from colorama import Fore
from mojang import API, errors

from mcdatacollector import Data, follow, updateviauuid, updatevianickname, datafile, chatbot, datawarn, warn


def generatepasscode() -> str:
    """Generates and returns a random passcode"""

    __PASSCODE__ = str(random.randint(0, 9999))
    # Pretty simple, right?
    return "0" * (4 - len(__PASSCODE__)) + __PASSCODE__


warn(Data.__tracker__)
datawarn()

mapi = API()  # Init Mojang API

CHATBOTACTIVE = False  # Init chatbot activity flag
HOST = "blurry16"  # Host player name
PASSCODE = generatepasscode()  # generating passcode
print(f"{Fore.MAGENTA}Chatbot passcode for this session is: {PASSCODE}")  # logging

if __name__ == "__main__":
    while True:
        LOGFILE = open(
            Data.LOGPATH,
            "r",
            encoding="UTF-8",
        )
        lines = follow(LOGFILE)
        for line in lines:
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

                                chatbot.lastseen(line)

                            case "#firsttimeseen":

                                chatbot.firsttimeseen(line)

                            case "#count":

                                chatbot.count(line)

                            case "#getdbid":

                                chatbot.getdbid(line)

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
                            data = datafile.load()
                            nickname = line.split("[CHAT]")[1].split()[0]
                            try:
                                uuid = mapi.get_uuid(nickname)
                                updateviauuid(uuid)
                            except errors.NotFound:
                                updatevianickname(nickname)
                            print("\n")