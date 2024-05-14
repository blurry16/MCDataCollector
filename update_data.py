from __data__ import cvdbdata
from json import dumps
from time import sleep
from mojang import API

mapi = API()

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


cvdbdata.dump(data)
