from logging import getLogger
from os import mkdir, listdir
from shutil import rmtree

import requests
from colorama import Fore

from mcdatacollector import __version__ as localversion, REPOURL, csvfolder, updateviauuid, updatevianickname
from mcdatacollector import getdata, saveskins, updatedata, stats, initializescript
from mcdatacollector import mcdcdumps
from mcdatacollector.mojang import get_uuid


def __csvfolderregen(subpath: str):
    tmp = csvfolder.joinpath(subpath)
    print(f"Deleting {len(listdir(tmp))} {subpath} dump{'' if abs(len(listdir(tmp))) == 1 else 's'}.")
    rmtree(tmp)
    mkdir(tmp)


logger = getLogger("mcdc.client")


def main():
    while True:
        inp = input(
            "1. Get data\n"
            "2. Save skins\n"
            "3. Update data\n"
            "4. Statistics\n"
            "5. Dumps\n"
            "6. Check for updates\n"
            "99. Quit\n"
            "-> "
        ).strip()
        if len(inp) == 0:
            continue
        match inp.split()[0]:
            case "1":
                while True:
                    inp = input(
                        "1. Get last seen time\n"
                        "2. Get first seen time\n"
                        "3. Get full data in JSON format\n"
                        "4. Get database id\n"
                        "5. Get all players' nicknames in the DB\n"
                        "6. Get all zombie accounts nicknames in the DB\n"
                        "7. Get all not-zombie accounts nicknames in the DB\n"
                        "99. Back to previous stage\n"
                        "-> "
                    ).strip()
                    match inp:
                        case "1":
                            arg = input(
                                "Lookup via [1] Nickname, [2] Mojang UUID, [3] DBID: "
                            ).strip()

                            getdata.getlastseentime(arg)

                        case "2":
                            arg = input(
                                "Lookup via [1] Nickname, [2] Mojang UUID, [3] DBID: "
                            ).strip()

                            getdata.getfirstseentime(arg)

                        case "3":
                            arg = input(
                                "Lookup via [1] Nickname, [2] Mojang UUID, [3] DBID: "
                            ).strip()

                            getdata.getdatajson(arg)
                        case "4":
                            arg = input(
                                "Lookup via [1] Nickname, [2] Mojang UUID: "
                            ).strip()

                            getdata.getdbid(arg)
                        case "5":

                            getdata.listallplayers()

                        case "6":

                            getdata.listallzombies()

                        case "7":

                            getdata.listallnonzombies()

                        case "99":
                            break

                        case _:
                            print(f"{Fore.RED}Unknown command.")

            case "2":
                while True:
                    mode = input(
                        "1. URL\n"
                        "2. Name\n"
                        "3. HTML model\n"
                        "4. Everything above\n"
                        "99. Back to previous stage\n"
                        "-> "
                    ).strip()
                    match mode:
                        case "1":

                            saveskins.saveurls()

                        case "2":

                            saveskins.savenames()

                        case "3":

                            saveskins.savehtml()

                        case "4":

                            saveskins.saveeverything()

                        case "99":

                            break

                        case _:
                            print(f"{Fore.RED}Unknown command.")

            case "3":
                while True:
                    a = input(
                        "1. By nicknames\n"
                        "2. With /list\n"
                        "3. Everyone's data (last time seen won't be touched)\n"
                        "99. Back to previous stage\n"
                        "-> "
                    ).strip()
                    match a:
                        case "1":

                            updatedata.updatebynicknames()

                        case "2":

                            updatedata.updatewithlist()

                        case "3":

                            updatedata.updateeveryonesdata()

                        case "99":
                            break
                        case _:
                            print(f"{Fore.RED}Unknown command.")

            case "4":
                while True:
                    a = input(
                        "1. Generate stats\n"
                        "2. Parse stats\n"
                        "3. Preview raw stats JSON\n"
                        "99. Back to previous stage\n"
                        "-> "
                    ).strip()
                    match a:

                        case "1":
                            stats.genstats()

                        case "2":
                            stats.parsestats()

                        case "3":
                            stats.parseraw()

                        case "99":
                            break
                        case _:
                            print(f"{Fore.RED}Unknown command.")

            case "5":
                while True:
                    a = input(
                        "1. Generate a full dump\n"
                        "2. Generate an id,name dump\n"
                        "3. Delete all dumps\n"
                        "4. Delete only full dumps\n"
                        "5. Delete only miscellaneous dumps\n"
                        "99. Back to previous stage\n"
                        "-> "
                    ).strip()
                    if a == "99":
                        break
                    if a in ["1", "2"]:
                        path = mcdcdumps.dumpfullcsv() if a == "1" else mcdcdumps.dumpplayerscsv()
                        print(f"The {path.name} dump generated.\n"
                              f"Access the file at {path}")

                    if a in ["3", "4"]:
                        __csvfolderregen("full")
                        print(f"{csvfolder.joinpath('full')} regenerated.")
                    if a in ["3", "5"]:
                        __csvfolderregen("misc")
                        print(f"{csvfolder.joinpath('misc')} regenerated.")
                    if a not in [str(i) for i in range(1, 6)]:
                        print(f"{Fore.RED}Unknown command.")

            case "6":

                isdevbuild = localversion[:3] == "dev"
                if isdevbuild:
                    logger.warning(
                        "please mind that you're currently using DEVELOPER build. update checking may work wrong.")
                githubversion = requests.get(
                    "https://raw.githubusercontent.com/blurry16/MCDataCollector/refs/heads/main/mcdatacollector/__init__.py").text.split(
                    "\n")[0].split(" ")[2].replace("\"", "")
                if githubversion[:3] == "dev":
                    print(
                        f"{Fore.RED}Update checking is unavailable. The main branch has 'dev' tag in its __version__.")
                    continue
                la, lb, lc = map(int, (localversion[3:] if isdevbuild else localversion).split("."))  # local a, ...
                a, b, c = map(int, githubversion.split("."))
                if a > la or (a == la and b > lb) or (a == la and b == lb and c > lc):
                    print(f"{Fore.GREEN}Good news! New version {githubversion} is available at "
                          f"{REPOURL}releases/latest!")


                else:
                    print(f"{Fore.RED}No updates found. {localversion} is up to date.")
            case "99":
                break

            case "--forceadd":
                if len(inp.split()) > 2:
                    m = inp.split()[1]
                    arg = inp.split()[2]
                    if m == "--uuid":
                        updateviauuid(arg)
                    elif m == "--username":
                        updatevianickname(arg)

            case "--getuuid" | "--uuid":
                if len(inp.split()) > 1:
                    arg = inp.split()[1]
                    print(get_uuid(arg))

            case _:
                print(f"{Fore.RED}Unknown command.")


# __csvfolderregen = lambda f: (rmtree(csvfolder.joinpath(f)), mkdir(csvfolder.joinpath(f)))

if __name__ == "__main__":
    initializescript("client")
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
