from __data__ import cvdbdata
from datetime import datetime
from time import time
from mojang import API, errors

mapi = API()

while True:
    print(
        "1. Get last seen data by nickname\n2. Get first seen data by nickname\n3. Get full data by nickname\n4. Get database id by nickname\n5. Get all players' nicknames in the DB\n6. Get all zombie accounts nicknames in the DB\n7. Quit"
    )
    inp = input()
    try:
        match inp:
            case "1":
                try:
                    nickname = input("Nickname: ").lower()
                    data = cvdbdata.load()
                    local_uuid = mapi.get_uuid(nickname)
                    if local_uuid in data:
                        local_data = data[local_uuid]
                        dt_obj = datetime.fromtimestamp(local_data["last_seen"])
                        print(
                            f"{local_data['name']} was seen at {dt_obj} UTC+3. ({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
                        )
                    else:
                        print(f"The bot has never seen {nickname}")
                except errors.NotFound:
                    if nickname in data:
                        local_data = data[nickname]
                        dt_obj = datetime.fromtimestamp(local_data["last_seen"])
                        print(
                            f"{local_data['name']} was seen at {dt_obj} UTC+3. ({datetime.fromtimestamp(round(time())) - dt_obj} ago)"
                        )
                    else:
                        print("This player doesn't exist.")
            case "2":
                try:
                    nickname = input("Nickname: ").lower()
                    data = cvdbdata.load()
                    local_uuid = mapi.get_uuid(nickname)
                    if local_uuid in data:
                        local_data = data[local_uuid]
                        timestamp = local_data["first_time_seen"]
                        print(
                            f"{local_data['name']} was seen for the first time at {datetime.fromtimestamp(timestamp)} UTC+3. ({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(local_data['first_time_seen'])} ago)"
                        )
                    else:
                        print(f"The bot has never seen {nickname}")
                except errors.NotFound:
                    if nickname in data:
                        local_data = data[nickname]
                        timestamp = local_data["first_time_seen"]
                        print(
                            f"{local_data['name']} was seen for the first time at {datetime.fromtimestamp(timestamp)} UTC+3. ({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(local_data['first_time_seen'])} ago)"
                        )
                    else:
                        print("This player doesn't exist.")
            case "3":
                try:
                    nickname = input("Nickname: ").lower()
                    data = cvdbdata.load()
                    local_uuid = mapi.get_uuid(nickname)
                    if local_uuid in data:
                        print(data[local_uuid])
                    else:
                        print(f"The bot has never seen {nickname}")
                except errors.NotFound:
                    if nickname in data:
                        print(data[nickname])
                    else:
                        print("This player doesn't exist.")
            case "4":
                try:
                    inp = input("Nickname: ").lower()
                    data = cvdbdata.load()
                    uuid = mapi.get_uuid(inp)
                    nickname = data[uuid]["name"]
                    if uuid in data:
                        print(f"{nickname}'s database id is {data[uuid]['db_id']}.")
                    else:
                        print(f"The bot has never seen {nickname}")
                except errors.NotFound:
                    if inp.lower() in data:
                        local_data = data[inp]
                        print(
                            f"{local_data['name']}'s database id is {local_data['db_id']}"
                        )

            case "5":
                data = cvdbdata.load()
                for i in data:
                    print(data[i]["name"])
                print(f"{len(data)} players in DB")

            case "6":
                data = cvdbdata.load()
                count = 0
                for i in data:
                    if i == data[i]["name"].lower():
                        count += 1
                        print(data[i]["name"])
                print(f"{count} zombies in the DB")

            case "7":
                exit(0)

            case _:
                print("Unknown command.")
    except KeyError:
        print("The bot has never seen this player.")
