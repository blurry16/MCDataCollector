# Imports
import random

from colorama import Fore
from mojang import API, errors

from mcdatacollector import Data, follow, updateviauuid, updatevianickname, chatbot, datawarn, warn, logo, getuuid


def generatepasscode() -> str:
    """Generates and returns a random passcode"""

    __PASSCODE__ = str(random.randint(0, 9999))
    # Pretty simple, right?
    return "0" * (4 - len(__PASSCODE__)) + __PASSCODE__


def main():
    chatbotflag = False  # Init chatbot activity flag
    HOST = "blurry16"  # Host player name

    # print(f"Chatbot passcode for this session is: {PASSCODE}")  # logging

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
                                chatbotflag = not chatbotflag
                                print(
                                    f"{Fore.GREEN}Chatbot activated."
                                    if chatbotflag
                                    else f"{Fore.RED}Chatbot unactivated."
                                )
                        except IndexError:
                            if username == HOST:
                                print(f"{Fore.MAGENTA}Not enough arguments!")
                    elif chatbotflag:
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
                                and "game" == split[4]
                        ):
                            nickname = line.split("[CHAT]")[1].split()[0]
                            try:
                                uuid = getuuid(nickname)
                                updateviauuid(uuid)
                            except errors.NotFound:
                                updatevianickname(nickname)
                            print("\n")


if __name__ == "__main__":

    warn(Data.__tracker__)
    datawarn()

    PASSCODE = generatepasscode()  # generating passcode
    print(logo)
    print(Fore.MAGENTA + f"{Fore.RESET + ' tracker ' + PASSCODE + ' ' + Fore.MAGENTA:=^121}\n")

    mapi = API()  # Init Mojang API

    try:
        main()
    except KeyboardInterrupt:
        exit(0)
