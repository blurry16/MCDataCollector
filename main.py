import time
from mojang import API, errors
from __data__ import cvdbdata, LOGPATH, follow

mapi = API()

while True:
    LOGFILE = open(
        LOGPATH,
        "r",
        encoding="UTF-8",
    )
    lines = follow(LOGFILE)
    for line in lines:
        if "[CHAT]" in line:
            line_upd = line.split("CHAT")[1]
            if (
                "<" not in line_upd
                and "[" not in line_upd
                and ("joined" == line_upd.split()[2] or "left" == line_upd.split()[2])
            ):
                try:
                    nickname = line.split("[CHAT]")[1].split()[0]
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
                    print(f"{nickname}'s dictionary updated.")
                    time.sleep(0.1)
                except errors.NotFound:
                    if nickname != "*":
                        data[nickname.lower()] = {
                            "id": None,
                            "name": nickname,
                            "last_seen": round(float(profile.timestamp) / 1000),
                            "first_time_seen": (
                                round(float(profile.timestamp) / 1000)
                                if uuid not in data
                                else data[uuid]["first_time_seen"]
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
                        print(f"{nickname}'s dictionary updated.")
                except Exception as e:
                    print(f"Exception {e} occurred at {int(time.time())}.")
