from mojang import API, errors
from time import sleep
from __data__ import cvdbdata, LOGPATH, follow

mapi = API()

while True:
    a = input("1. by nicknames\n2. with /list\n")
    match a:
        case "1":
            nicknames = list(map(str, input("nicknams (splitted by space): ").split()))
            count = len(nicknames)
            for nickname in nicknames:
                try:
                    uuid = mapi.get_uuid(nickname)
                    profile = mapi.get_profile(uuid)
                    data = cvdbdata.load()
                    data[uuid] = {
                        "id": profile.id,
                        "name": profile.name,
                        "last_seen": round(float(profile.timestamp) / 1000),
                        "first_time_seen": (
                            round(float(profile.timestamp) / 1000)
                            if uuid not in data
                            else data[uuid]["first_time_seen"]
                        ),
                        "is_legacy_profile": profile.is_legacy_profile,
                        "skin_variant": profile.skin_variant,
                        "cape_url": profile.cape_url,
                        "skin_url": profile.skin_url,
                        "db_id": (
                            len(data) if uuid not in data else data[uuid]["db_id"]
                        ),
                        "does_exist": True,
                    }
                    cvdbdata.dump(data)
                    print(f"{profile.name}'s dictionary was updated/added.")
                    sleep(0.1)
                except errors.NotFound:
                    count -= 1
                    print(f"{nickname} doesn't exist.")
                    continue
            print(f"Updated {count} players.")
            exit(0)
        case "2":
            LOGFILE = open(
                LOGPATH,
                "r",
                encoding="UTF-8",
            )
            loglines = follow(LOGFILE)
            print("waiting for /list")
            for line in loglines:
                if "[CHAT]" in line:
                    line_upd = line.split("[CHAT] ")[1]
                    if line_upd.split()[0] == "Cubeville":
                        nicknames = line_upd.split("): ")[1].split(", ")
                        print(nicknames)
                        count = len(nicknames)
                        for nickname in nicknames:
                            nickname = nickname.strip()
                            try:
                                uuid = mapi.get_uuid(nickname)
                                profile = mapi.get_profile(uuid)
                                data = cvdbdata.load()
                                data[uuid] = {
                                    "id": profile.id,
                                    "name": profile.name,
                                    "last_seen": round(float(profile.timestamp) / 1000),
                                    "first_time_seen": (
                                        round(float(profile.timestamp) / 1000)
                                        if uuid not in data
                                        else data[uuid]["first_time_seen"]
                                    ),
                                    "is_legacy_profile": profile.is_legacy_profile,
                                    "skin_variant": profile.skin_variant,
                                    "cape_url": profile.cape_url,
                                    "skin_url": profile.skin_url,
                                    "db_id": (
                                        len(data)
                                        if uuid not in data
                                        else data[uuid]["db_id"]
                                    ),
                                    "does_exist": True,
                                }
                                cvdbdata.dump(data)
                                print(f"{profile.name}'s dictionary was updated/added.")
                                sleep(0.1)
                            except errors.NotFound:
                                data[nickname] = {
                                    "id": profile.id,
                                    "name": profile.name,
                                    "last_seen": round(float(profile.timestamp) / 1000),
                                    "first_time_seen": (
                                        round(float(profile.timestamp) / 1000)
                                        if uuid not in data
                                        else data[uuid]["first_time_seen"]
                                    ),
                                    "is_legacy_profile": profile.is_legacy_profile,
                                    "skin_variant": profile.skin_variant,
                                    "cape_url": profile.cape_url,
                                    "skin_url": profile.skin_url,
                                    "db_id": (
                                        len(data)
                                        if uuid not in data
                                        else data[uuid]["db_id"]
                                    ),
                                    "does_exist": False,
                                }
                                cvdbdata.dump(data)
                                print(f"{profile.name}'s dictionary was updated/added.")
                                sleep(0.1)
                                continue
                        print(f"Updated {count} players.")
                        exit(0)
