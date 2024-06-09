from mojang import API, errors
from time import sleep, time
from __data__ import cvdbdata, LOGPATH, follow, UKNOWNVALUEEXCEPTION
from json import dumps

mapi = API()

a = input(
    "1. By nicknames\n2. With /list\n3. Everyone's data (last time seen won't be touched)\n"
)
if a not in ["1", "2", "3"]:
    raise UKNOWNVALUEEXCEPTION

match a:
    case "1":
        nicknames = list(map(str, input("Nicknames (splitted by space): ").split()))
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
                    "db_id": (len(data) if uuid not in data else data[uuid]["db_id"]),
                    "does_exist": True,
                }
                cvdbdata.dump(data)
                print(f"{profile.name}'s dictionary was updated/added.")
                sleep(0.1)
            except errors.NotFound:
                count -= 1
                print(f"{nickname} doesn't exist.")
                continue
            sleep(0.25)
        print(f"Updated {count} players.")
        exit(0)

    case "2":
        LOGFILE = open(
            LOGPATH,
            "r",
            encoding="UTF-8",
        )
        loglines = follow(LOGFILE)
        print("Waiting for /list...")
        for line in loglines:
            if "[CHAT]" in line:
                line_upd = line.split("[CHAT] ")[1]
                if line_upd.split()[0] == "Cubeville":
                    nicknames = line_upd.split("): ")[1].split(", ")
                    print(nicknames)
                    count = len(nicknames)
                    for nickname in nicknames:
                        nickname = nickname.strip()
                        data = cvdbdata.load()
                        try:
                            uuid = mapi.get_uuid(nickname)
                            profile = mapi.get_profile(uuid)
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
                            print(dumps(data[uuid], indent=2))
                        except errors.NotFound:
                            data[nickname.lower()] = {
                                "id": None,
                                "name": nickname,
                                "last_seen": int(time()),
                                "first_time_seen": (
                                    int(time())
                                    if nickname not in data
                                    else data[nickname]["first_time_seen"]
                                ),
                                "is_legacy_profile": None,
                                "skin_variant": None,
                                "cape_url": None,
                                "skin_url": None,
                                "db_id": (
                                    len(data)
                                    if nickname not in data
                                    else data[nickname]["db_id"]
                                ),
                                "does_exist": False,
                            }
                            cvdbdata.dump(data)
                            print(f"{nickname}'s dictionary was updated/added.")
                            print(dumps(data[nickname.lower()], indent=2))
                            continue
                        sleep(0.25)
                    print(f"Updated {count} players.")
                    exit(0)

    case "3":
        data = cvdbdata.load()
        for uuid in data:
            if data[uuid]["id"] != None:
                profile = mapi.get_profile(uuid)
                data[uuid] = {
                    "id": profile.id,
                    "name": profile.name,
                    "last_seen": data[uuid]["last_seen"],
                    "first_time_seen": data[uuid]["first_time_seen"],
                    "is_legacy_profile": profile.is_legacy_profile,
                    "skin_variant": profile.skin_variant,
                    "cape_url": profile.cape_url,
                    "skin_url": profile.skin_url,
                    "db_id": data[uuid]["db_id"],
                    "does_exist": True,
                }
                print(f"Updated {profile.name}")
                print(dumps(data[uuid], indent=2))
                sleep(0.25)
        exit(0)