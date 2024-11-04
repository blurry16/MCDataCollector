from colorama import Fore

from mcdatacollector import getdata, saveskins, updatedata, Data, warn, datawarn, statswarn, stats, logo


def main():
    while True:
        inp = input(
            "1. Get data.\n"
            "2. Save skins.\n"
            "3. Update data.\n"
            "4. Statistics\n"
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
                        "7. Get all not-zombie accounts nicknames in the DB\n"
                        "8. Get back to previous stage\n"
                    ).strip()
                    try:
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
                    except KeyError:
                        print("The bot has never seen this player.")

            case "2":
                while True:
                    mode = input(
                        "1. URL\n"
                        "2. Name\n"
                        "3. HTML model\n"
                        "4. Everything above\n"
                        "5. Get back to previous stage.\n"
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
                        "4. Get back to previous stage.\n"
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
                    ).strip()
                    match a:
                        case "1":
                            stats.savestats()
                        case "2":
                            stats.parsestats()
                        case _:
                            print(f"{Fore.RED}Unknown command.")

            case "5":
                break

            case _:
                print(f"{Fore.RED}Unknown command.")


if __name__ == "__main__":
    warn(Data.__client__)
    datawarn()
    statswarn()

    print(logo)

    try:
        main()
    except KeyboardInterrupt:
        exit(0)
