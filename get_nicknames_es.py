"""
Let it just be here. Okay?
I made it at the time I was making the sorted list of ES nicknames. Last updated version of the list can be obtained at pins of #general in ES discord

This is some kind of scratch so don't mind lol.
"""

from mojang import API, errors
from __data__ import cvdbdata, __data__
from colorama import Back, Fore
import json
import time

players = [
    "blurry16",
    "cagedFALC0N",
    "DaKittiQueenOfSK",
    "Dr_Aves",
    "fredlime",
    "Goaticecream",
    "_kittyxx",
    "MamaCheckers",
    "rxyc",
    "WallyDonkey",
    "BandNerdMama",
    "BooBearCrafter",
    "caught_n_candy",
    "Cora216",
    "FITJ2564",
    "JinKiJoo",
    "_M1nnow",
    "PookieCrafter",
    "SammyTheElf",
    "Syrynn",
    "daddybearcrafter",
    "Joshiek",
    "LissaLaine",
    "PositiveTherapy1",
    "_Sammiee_",
    "SleepyBean",
    "Tisjstme",
    "TT_McQueen",
    "vic_torus",
    "vip2kea",
    "DripstoneCrafter",
    "hyliangrits",
    "jstautumn",
    "Lumeriana",
    "MCG8",
    "redstone_nub",
    "SunnyDemon202",
    "SuperAlexstar",
    "TiredSoul5",
    "WeatherCats",
    "101Wolves",
    "boinor",
    "Cherilee",
    "KessieRose",
    "ParadisesTurtles",
    "RacingBeam6502",
    "samthescientist",
    "SooprJ",
    "SpeedyG123",
    "Bluebear1858",
    "CheetahGhost92",
    "Firesnuke",
    "LoganDaNinja",
    "OverDhill",
    "PartyGreyson",
    "_Rt11",
    "TindurLikesCats",
    "TsoMein",
    "whamWHAMmooMOO",
    "ChowTime",
    "Erwut",
    "MarxTheGamer",
    "IW_Hisl",
    "less_more",
    "pterr",
    "PuppyFancier",
    "SpaceFox884",
    "SkyButNo",
    "VictoryMan123",
    "CastleMiner64",
    "DADFISH",
    "EmmaKR",
    "ItsMeNeon",
    "mariomilkm",
    "MiaMiaMiana",
    "shoppingcartt",
    "slef69",
    "StrmtrooprMB9910",
    "xxmn",
    "AidanEJ",
    "Clanky_Minecraft",
    "Creator_Bob",
    "EagleKneagle",
    "Ethanlues",
    "HalZurkit",
    "_Moza",
    "Pizza4001",
    "RenFurnael",
    "ThatCrazyManiac",
    "AwhDennis",
    "Heidsy",
    "Itss01diesyl",
    "Majest0",
    "MrSmall8",
]

uuids = {
    "blurry16": "ef2b9013f4ca4749b3bfaf83146c538e",
    "cagedFALC0N": "e2cc4960bead4748baa7b25c86ab736d",
    "DaKittiQueenOfSK": "afcdd440b5cb457490ebaf3ec54f1cff",
    "Dr_Aves": "e9fd6719be254ac88f0b1ee23e2bcbd6",
    "fredlime": "8eba079e7e9448aa96c06ec4998ab8c3",
    "Goaticecream": "d3288805405d48959423ca25ed532f0c",
    "_kittyxx": "306467712f314e3facb6afde37b33032",
    "MamaCheckers": "39646a36ceb943879f0039bbf0ff9dee",
    "rxyc": "0c217e9b48574e51b7b713c2d7107c9b",
    "WallyDonkey": "a93d13758ea240cc90a244585776e1d7",
    "BandNerdMama": "ff702ab4ea354dd4b91e0074a86fb908",
    "BooBearCrafter": "91dfd6135a544d2981637bbc4a9b25e1",
    "caught_n_candy": "18117c41cb0c4c49a30a672e60384622",
    "Cora216": "4ebbebbdfbcb4108ae055bbbbaf01856",
    "FITJ2564": "b0858c2e10784e3d988598292bee8024",
    "JinKiJoo": "f6dfee1cc42743b28e856df709299d88",
    "_M1nnow": "b614de6c07934400a8d47c5a8c3dc6c6",
    "PookieCrafter": "348228a026b54a319918dc0d452f21c0",
    "SammyTheElf": "a9c47d52a71a4b5580bc120894b69d0b",
    "Syrynn": "e339a9e23bdd49d6a97c0a9548661683",
    "daddybearcrafter": "8a82cc1508d74378acec63cbf406a099",
    "Joshiek": "8c4590e4bfe74aa68d049f459666c08e",
    "LissaLaine": "5d23569fccf24d27a7a9f19e3b943574",
    "PositiveTherapy1": "ed2cd1b8e3dc42e2af286516283411d5",
    "_Sammiee_": "a214bc0ae64642cf848315bf5f6c7581",
    "SleepyBean": "fd88d8e2f2624092aa12f6851240b27a",
    "Tisjstme": "2189cb846173457f8526f622526e4ec0",
    "TT_McQueen": "1572c9fda57242e5b3532bf488c0459b",
    "vic_torus": "0ea72b90459d4e44923f67676e9ecab8",
    "vip2kea": "3b0493dcf64c48f9b11702d3dfbc8214",
    "DripstoneCrafter": "996ccf7765534d2c9c179bd58215ed14",
    "hyliangrits": "a790f13a6b76484c907a5e81bfcaaf87",
    "jstautumn": "baa55b26438d41229ce63d056787259d",
    "Lumeriana": "9026cdc093684baf8a3f377f755181d7",
    "MCG8": "218257ec57be43dd8f847d985231bb44",
    "redstone_nub": "13eefe72561c4c0dab02a78c87c24d24",
    "SunnyDemon202": "d93f3c7af0f041ab9685740ff95810c4",
    "SuperAlexstar": "774aa89977324855aa23bbbe4a6333b6",
    "TiredSoul5": "1fbb1eb9f69f404a965920002794108b",
    "WeatherCats": "50b04546d30c4e0894f9494933c8c8ff",
    "101Wolves": "d1d7b35861ec4a0ab617e6d1c538cb70",
    "boinor": "86000bb940b74ab995e0cf2c81a2f41a",
    "Cherilee": "25f0c2ba6473439283e96821d84fefc2",
    "KessieRose": "47c7823e725546f49f8f36a32c26594b",
    "ParadisesTurtles": "5118bb14c47442dbab3898b347337611",
    "RacingBeam6502": "0f6edb41853845f78e91fb82003b9579",
    "samthescientist": "00776bbcf5014188b8ac508ecd3cde17",
    "SooprJ": "6c42b23a6fda4166ac79f5a9f0607eb9",
    "SpeedyG123": "78aeef02160c423b82151575020b648d",
    "Bluebear1858": "7e253fe442ce4bde879785407d455529",
    "CheetahGhost92": "bd9d9e6f75d841d49f06d4dd0a8b0302",
    "Firesnuke": "95eb4cafe6cb47878625987528c8aba4",
    "LoganDaNinja": "7677395cde4b429f9d06f375df193148",
    "OverDhill": "a0eb2a65eb5540da8a829a955a1b7aa4",
    "PartyGreyson": "2f376f3abe984bc0ba06ea9ff57604d1",
    "_Rt11": "e01b73dfc9914332b62472b13abd6702",
    "TindurLikesCats": "75121edca4eb422ca2c5addefea6d111",
    "TsoMein": "793ba790fd4943f0b4ca8f8aeb168ddd",
    "whamWHAMmooMOO": "77018a299d8c439c88d2feb30ae8d2d3",
    "ChowTime": "6e0840879a5f4254bcf9792e7738723d",
    "Erwut": "162556ac4774466591149cbc6761dfe2",
    "MarxTheGamer": "cf66e16189a74e329325e3e077233af0",
    "IW_Hisl": "76c5ef0068594e8cbd41fc78f8fdeec1",
    "less_more": "ee8ddd562c574872933e582c928acc00",
    "pterr": "4566c69b8557440a82330d9f2e599e94",
    "PuppyFancier": "51914c970668402e92a385cbbb57faa5",
    "SpaceFox884": "61eb5c6d859a4ab2ba29c60d00b278e6",
    "SkyButNo": "06b1c8234a6f42789b682706982587ef",
    "VictoryMan123": "6559837802d94e2b9439a817dc2992f3",
    "CastleMiner64": "bbf76ec3b59b475aa623e7825c087e4d",
    "DADFISH": "15085288c169448783d58ffca9e0fec6",
    "EmmaKR": "0a6ff29e74134230be4a83b0151ed237",
    "ItsMeNeon": "95fbb47b89504221aff87f2e8769bfec",
    "mariomilkm": "b16206489f694ee08fdad2b7b1f4343b",
    "MiaMiaMiana": "b037b93ad3d24fa28b8b41afce88ec73",
    "shoppingcartt": "da2a76b172084183bd8811ca28fc4e6d",
    "slef69": "d0534cb3260a439c9e915ea69479df0c",
    "StrmtrooprMB9910": "eccfea25a1d446979028e051168d957f",
    "xxmn": "9a9bba7db30142a0b9587c76209ce779",
    "AidanEJ": "38d646dd55c94362b51e8f7eaaeb0371",
    "Clanky_Minecraft": "1ed769a8cd99496a973ae120f106666c",
    "Creator_Bob": "92230750bf3b4f42a56d217b791bfc65",
    "EagleKneagle": "acd1d915cc3a4af28ece6da868eec4ff",
    "Ethanlues": "6623d30449fc42e7b617c4c0212d1432",
    "HalZurkit": "b06117b71eb24bfa80f1c8abce6776d4",
    "_Moza": "ad9e2c1dda994a2ea7316f6c39bfec71",
    "Pizza4001": "4a19453c7fe7402fa12ded3101970efa",
    "RenFurnael": "739688953e0440c99b98f25deb6f46cd",
    "ThatCrazyManiac": "25ed1d6b4c8d4e51a7d634d5da3a1af0",
    "AwhDennis": "016d533228704df3baa10fcee5254cb2",
    "Heidsy": "04c65398c8004990b8ff008ec2b91075",
    "Itss01diesyl": "a84d8740746a4cd88233e8b03c3bcc73",
    "Majest0": "f96ea76ad4644e0ab06fbdd69a696e97",
    "MrSmall8": "b92482d57365443386e08acb855782b6",
}

mapi = API()

# data = cvdbdata.load()

esplayersdata = __data__(
    r"C:\Users\Blurry\PycharmProjects\playersData\es_players_data.json"
)

with open(r"data\es_players.txt", "r", encoding="UTF-8") as file:
    esnicknames = file.read().split("\n")

# dbnicknames = []
# for player in data:
#     if data[player]["does_exist"]:
#         dbnicknames.append(data[player]["name"])

# esplayers = []
# for esnickname in esnicknames:
#     # if esnickname not in dbnicknames:
#     # print(esnickname)
#     try:
#         profile = mapi.get_profile(mapi.get_uuid(esnickname))
#         esplayers.append(profile.name)
#         print(profile.name)
#         # esplayers[profile.id] = profile.__dict__
#     except errors.NotFound:
#         print(f"{Back.RED}{esnickname} invalid.")
#     time.sleep(5)
# # print(json.dumps(dbnicknames,))
# print(esplayers)
# print(dbnicknames)
# print(json.dumps(esplayers, indent=4))


# print("\n".join(sorted(list(set(players)))))
# print(len(list(set(players))))
data = esplayersdata.load()

# for i in range(0, len(players), 10):
#     # mapi.get_uuids
#     print(players[i : i + 10])
#     uuids.append(mapi.get_uuids(players[i : i + 10]))

UUIDSONLY = []
for i in uuids:
    UUIDSONLY.append(uuids[i])
print("\n".join(UUIDSONLY))
if input(f"{Fore.MAGENTA}Would you like to update data? y/n: ").lower() in ["y", ""]:
    print(Fore.RESET)
    for i in uuids:
        profile = mapi.get_profile(uuids[i])
        data[profile.id] = {
            "id": profile.id,
            "name": profile.name,
            "is_legacy_profile": profile.is_legacy_profile,
            "skin_variant": profile.skin_variant,
            "cape_url": profile.cape_url,
            "skin_url": profile.skin_url,
        }
        print(f"{Fore.GREEN}{profile.name} updated")
        print(json.dumps(data[profile.id], indent=2))
        print("\n")
        time.sleep(1)
    esplayersdata.dump(data)
print(Fore.RESET)
data = esplayersdata.load()
names = [data[i]["name"] for i in data]
uuids = {data[i]["name"]: data[i]["id"] for i in data}
print("\n".join(sorted(names)))
print(names, end="\n" * 2)
print(uuids, end="\n" * 2)
print(len(names), len(data), len(uuids))
