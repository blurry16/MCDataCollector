from datetime import datetime
from time import time

from colorama import Fore
from mojang import errors

from mcdatacollector import datafile, getuuid, initializescript


def getlastseentime(arg: str):
    data = datafile.load()

    try:
        if arg == "1":
            nickname = input("Nickname: ").strip().split()[0]
            try:
                local_uuid = getuuid(nickname)
                if local_uuid in data:
                    local_data = data[local_uuid]
                    dt_obj = datetime.fromtimestamp(
                        local_data["last_seen"]
                    )
                    print(
                        f"{local_data['name']} was seen at {dt_obj}. "
                        f"({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
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
                        f"{local_data['name']} was seen at {dt_obj}. "
                        f"({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
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
                    f"{local_data['name']} ({local_data['id']}) was seen at {dt_obj}. "
                    f"({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
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
                    f"{local_data['name']} ({local_data['db_id']}) was seen at {dt_obj}. "
                    f"({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
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


def getfirstseentime(arg: str):
    data = datafile.load()
    try:
        if arg == "1":
            nickname = input("Nickname: ").strip().split()[0]
            try:
                local_uuid = getuuid(nickname)
                if local_uuid in data:
                    local_data = data[local_uuid]
                    timestamp = local_data["first_time_seen"]
                    print(
                        f"{local_data['name']} was seen for the first time at "
                        f"{datetime.fromtimestamp(timestamp)}. "
                        f"({datetime.fromtimestamp(round(time())) -
                            datetime.fromtimestamp(local_data['first_time_seen'])} ago)"
                    )
                else:
                    print(f"The bot has never seen {nickname}.")
            except errors.NotFound:
                if nickname in data:
                    local_data = data[nickname]
                    timestamp = local_data["first_time_seen"]
                    print(
                        f"{local_data['name']} was seen for the first time at "
                        f"{datetime.fromtimestamp(timestamp)}. "
                        f"({datetime.fromtimestamp(round(time())) -
                            datetime.fromtimestamp(local_data['first_time_seen'])} ago)"
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
                    f"{local_data['name']} ({local_data['id']}) was seen at {dt_obj}. "
                    f"({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
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
                    f"{local_data['name']} ({local_data['db_id']}) was seen at {dt_obj}. "
                    f"({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
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


def getdatajson(arg: str):
    indent = 2
    data = datafile.load()
    try:
        if arg == "1":
            inp = input("Nickname: ").strip()
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
                local_uuid = getuuid(nickname)
                if local_uuid in data:
                    print(datafile.dumps(local_uuid, indent))
                else:
                    print(f"The bot has never seen {nickname}.")
            except errors.NotFound:
                if nickname in data:

                    print(datafile.dumps(nickname, indent))

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
                print(datafile.dumps(uuid, indent))
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

                print(datafile.dumps(list(data)[db_id], indent))

            except ValueError:
                print(f"{Fore.RED}Wrong value!")
            except IndexError:
                print(
                    f"{Fore.RED}DB has no player with this DBID."
                )
        else:
            print(
                f"{Fore.RED}Unknown command."
            )
    except IndexError:
        print(f"{Fore.RED}Not enough arguments!")


def getdbid(arg: str):
    data = datafile.load()
    try:
        if arg == "1":
            inp = input("Nickname: ").lower().strip().split()[0]
            try:
                uuid = getuuid(inp)
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
                    f"{local_uuid}'s ({data[local_uuid]['name']}) database id is "
                    f"{data[local_uuid]['db_id']}"
                )
            else:
                print(f"The bot has never seen {local_uuid}.")
    except IndexError:
        print(f"{Fore.RED}Not enough arguments!")


def listallplayers():
    data = datafile.load()

    for profile in data:
        print(data[profile]["name"])
    print(f"{len(data)} players in DB.")


def listallzombies():
    data = datafile.load()

    count = 0
    for profile in data:
        if not data[profile]["does_exist"]:
            count += 1
            print(data[profile]["name"])
    print(f"{count} zombies in the DB.")


def listallnonzombies():
    data = datafile.load()

    not_zombies = 0
    for profile in data:
        if data[profile]["does_exist"]:
            not_zombies += 1
            print(data[profile]["name"])

    print(f"{not_zombies} not zombies in the DB.")


if __name__ == "__main__":
    initializescript(__file__)
    print(f"{Fore.GREEN}No errors found in {__file__}.")
