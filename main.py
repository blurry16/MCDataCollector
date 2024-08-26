import random

from mojang import API

from mcdatacollector import LOGPATH, follow, updateviauuid, updatevianickname
from mcdatacollector.chatbot import *


def generatepasscode() -> str:
    __PASSCODE__ = str(random.randint(0, 9999))
    return "0" * (4 - len(__PASSCODE__)) + __PASSCODE__


mapi = API()

CHATBOTACTIVE = False
HOST = "blurry16"
BANNED = []
PASSCODE = generatepasscode()
print(f"{Fore.MAGENTA}Chatbot passcode for this session is: {PASSCODE}")

if __name__ == "__main__":
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

                                lastseen(line)

                            case "#firsttimeseen":

                                firsttimeseen(line)

                            case "#count":

                                count(line)

                            case "#getdbid":

                                getdbid(line)

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
