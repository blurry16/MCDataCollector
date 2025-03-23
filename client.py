import requests
from colorama import Fore

from mcdatacollector import __version__ as localversion
from mcdatacollector import getdata, saveskins, updatedata, Data, warn, datawarn, statswarn, stats, initializescript


def main():
    while True:
        inp = input(
            "1. Get data\n"
            "2. Save skins\n"
            "3. Update data\n"
            "4. Statistics\n"
            "5. Check for updates\n"
            "6. Quit\n"
            "> "
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
                        "7. Get all not-zombie accounts nicknames in the DB\n"
                        "8. Back to previous stage\n"
                        "> "
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

                        case "8":
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
                        "5. Back to previous stage\n"
                        "> "
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

                        case "5":

                            break

                        case _:
                            print(f"{Fore.RED}Unknown command.")

            case "3":
                while True:
                    a = input(
                        "1. By nicknames\n"
                        "2. With /list\n"
                        "3. Everyone's data (last time seen won't be touched)\n"
                        "4. Back to previous stage\n"
                        "> "
                    ).strip()
                    match a:
                        case "1":

                            updatedata.updatebynicknames()

                        case "2":

                            updatedata.updatewithlist()

                        case "3":

                            updatedata.updateeveryonesdata()

                        case "4":
                            break
                        case _:
                            print(f"{Fore.RED}Unknown command.")

            case "4":
                while True:
                    a = input(
                        "1. Add stats\n"
                        "2. Parse stats\n"
                        "3. Preview raw stats JSON\n"
                        "4. Back to previous stage\n"
                        "> "
                    ).strip()
                    match a:

                        case "1":
                            stats.savestats()

                        case "2":
                            stats.parsestats()

                        case "3":
                            stats.parseraw()

                        case "99":
                            break
                        case _:
                            print(f"{Fore.RED}Unknown command.")

            case "5":
                githubversion = requests.get(
                    "https://raw.githubusercontent.com/blurry16/MCDataCollector/refs/heads/main/mcdatacollector/__init__.py").text.split(
                    "\n")[0].split(" ")[2].replace("\"", "")
                if githubversion[:3] != "dev" and githubversion != localversion:
                    print(f"{Fore.GREEN}Good news! New version {githubversion} is available at "
                          f"https://github.com/blurry16/MCDataCollector/releases/latest!")


                else:
                    print(f"{Fore.RED}No updates found. {localversion} is up to date.")
            case "6":
                break

            case _:
                print(f"{Fore.RED}Unknown command.")


if __name__ == "__main__":
    warn(Data.__client__)
    datawarn()
    statswarn()
    initializescript("client")
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
