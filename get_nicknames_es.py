from mojang import API, errors
from __data__ import cvdbdata

mapi = API()

data = cvdbdata.load()

# with open(r"data\es_players.txt", "r", encoding="UTF-8") as file:
#     esnicknames = file.read().split("\n")


# dbnicknaes = []
# for player in data:
#     if data[player]["does_exist"]:
#         dbnicknaes.append(data[player]["name"])

# for esnickname in esnicknames:
#     if esnickname not in dbnicknaes:
#         try:
#             profile = mapi.get_profile(mapi.get_uuid(esnickname))
#             esnicknames[esnicknames.index(esnickname)] = profile.name
#         except errors.NotFound:
#             print(f"{esnickname} invalid.")

# print(esnicknames)

players = [
    "fredlime",
    "Aves_Felix",
    "cagedFALC0N",
    "blurry16",
    "MamaCheckers",
    "WallyDonkey",
    "Goaticecream",
    "_kittyxx",
    "rxyc",
    "ItsMeQueenLuna_I",
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
    "RainyDemon101",
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
    "XxRyan303",
    "LoganDaNinja",
    "KINGGREYSON",
    "OverDhill",
    "whamWHAMmooMOO",
    "CheetahGhost92",
    "ItzMeTindur",
    "TsoMein",
    "SpaceFox884",
    "VictoryMan123",
    "PuppyFancier",
    "less_more",
    "ChowTime",
    "Erwut",
    "pterr",
    "SkyButYes",
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
    "MCG9",
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
]


print("\n".join(sorted(players)))
print(len(list(set(players))))
