"""
Let it just be here. Okay?
I made it at the time I was making the sorted list of ES nicknames. Last updated version of the list can be obtained at pins of #general in ES discord
"""

from mojang import API, errors
from __data__ import cvdbdata
from colorama import init, Back
import json
import time

mapi = API()

init(autoreset=True)
# data = cvdbdata.load()

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
    "Jinkijoo",
    "TT_McQueen",
    "PositiveTherapy1",
    "Vic_Torus",
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
    "_Rt11",
    "TsoMein",
    "LoganDaNinja",
    "PartyGreyson",
    "OverDHill",
    "whamWHAMmooMOO",
    "CheetahGhost92",
    "TindurMar",
    "SpaceFox884",
    "VictoryMan123",
    "PuppyFancier",
    "less_more",
    "ChowTime",
    "Erwut",
    "Pterr",
    "TheActualSky",
    "GamerAnthony14",
    "IW_Hisl",
    "EmmaKR",
    "xxmn",
    "DadFish",
    "StrmtrooprMB9910",
    "MiaMiaMiana",
    "CastleMiner64",
    "mariomilkm",
    "ItsMeNeon",
    "shoppingcartt",
    "Slef69",
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
    "Itss01Diesyl",
    "MrSmall8",
    "AwhDennis",
    "Majest0",
]


print("\n".join(sorted(list(set(players)))))
print(len(list(set(players))))
