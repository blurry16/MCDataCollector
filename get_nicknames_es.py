from mojang import API, errors
from __data__ import cvdbdata
import json
import time

mapi = API()

data = cvdbdata.load()

with open(r"data\es_players.txt", "r", encoding="UTF-8") as file:
    esnicknames = file.read().split("\n")


# dbnicknames = []
# for player in data:
#     if data[player]["does_exist"]:
#         dbnicknames.append(data[player]["name"])

esplayers = []
for esnickname in esnicknames:
    # if esnickname not in dbnicknames:
        # print(esnickname)
    try:
        profile = mapi.get_profile(mapi.get_uuid(esnickname))
        esplayers.append(profile.name)
        # esplayers[profile.id] = profile.__dict__
    except errors.NotFound:
        print(f"{esnickname} invalid.")
    time.sleep(1)
# print(json.dumps(dbnicknames,))
print(esplayers)
# print(dbnicknames)
# print(json.dumps(esplayers, indent=4))
players = [
    "fredlime",
    "Dr_Aves",
    "cagedFALC0N",
    "blurry16",
    "MamaCheckers",
    "WallyDonkey",
    "Goaticecream",
    "_kittyxx",
    "rxyc",
    "DaKittiQueenOfSK",
    "Syrynn",
    "PookieCrafter",
    "BooBearCrafter",
    "SammyTheElf",
    "BandNerdMama",
    "caught_n_candy",
    "_M1nnow",
    "Cora216",
    "FITJ2564",
    "JinKiJoo",
    "TT_McQueen",
    "PositiveTherapy1",
    "vic_torus",
    "Tisjstme",
    "Joshiek",
    "SleepyBean",
    "vip2kea",
    "_Sammiee_",
    "daddybearcrafter",
    "LissaLaine",
    "SunnyDemon202",
    "redstone_nub",
    "Lumeriana",
    "DripstoneCrafter",
    "jstautumn",
    "hyliangrits",
    "MCG8",
    "SuperAlexstar",
    "WeatherCats",
    "TiredSoul5",
    "RacingBeam6502",
    "Cherilee",
    "SpeedyG123",
    "ParadisesTurtles",
    "SooprJ",
    "boinor",
    "King_Jude_I",
    "KessieRose",
    "samthescientist",
    "101Wolves",
    "Bluebear1858",
    "Firesnuke",
    "vip1kea",
    "TsoMein",
    "LoganDaNinja",
    "PartyGreyson",
    "OverDhill",
    "whamWHAMmooMOO",
    "CheetahGhost92",
    "TindurMar",
    "SpaceFox884",
    "VictoryMan123",
    "PuppyFancier",
    "less_more",
    "ChowTime",
    "Erwut",
    "pterr",
    "TheActualSky",
    "GamerAnthony14",
    "IW_Hisl",
    "EmmaKR",
    "xxmn",
    "DADFISH",
    "StrmtrooprMB9910",
    "MiaMiaMiana",
    "CastleMiner64",
    "mariomilkm",
    "ItsMeNeon",
    "shoppingcartt",
    "slef69",
    "HalZurkit",
    "RenFurnael",
    "AidanEJ",
    "_Moza",
    "Creator_Bob",
    "Ethanlues",
    "ThatCrazyManiac",
    "Pizza4001",
    "Clanky_Minecraft",
    "EagleKneagle",
    "Heidsy",
    "Itss01diesyl",
    "MrSmall8",
]


print("\n".join(sorted(list(set(players)))))
print(len(list(set(players))))
