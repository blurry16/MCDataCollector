import json
from datetime import datetime, UTC
from pathlib import Path

from colorama import Fore

from mcdatacollector import datafile, statsdataobj, initializescript, __JsonFile, Data


def genstats():
    data_len = len(datafile.load())
    statsdata: dict = statsdataobj.load()
    now_date = datetime.now(UTC).date().strftime("%Y-%m-%d")
    if len(statsdata) > 0:
        last_date = list(statsdata)[-1]

    statsdata[now_date] = {
        "count": data_len,
        "delta": data_len if len(statsdata) == 0 else data_len - int(statsdata[last_date]["count"]),
    }
    print(json.dumps(statsdata, indent=2) + "\n")
    if input(f"{Fore.GREEN}Proceed? {Fore.RESET}y/n: ").strip().lower() in ["y", ""]:
        statsdataobj.dump(statsdata)


def parsestats():
    stats = statsdataobj.load()
    if len(stats) > 0:
        for i in stats:
            print(f"{i}: {stats[i]['count']} players, {stats[i]['delta']} delta.")
    else:
        print("No stats available. Try generating them.")


def parseraw():
    print(statsdataobj.dumps())


def mergestats(path1: Path, path2: Path = statsdataobj.file_path):
    merged = __JsonFile(path1).load()
    tomerge = __JsonFile(path2).load()
    for i in tomerge:
        if i in merged:
            print("Merge conflict!")
            print(f"{i} already existed. Please choose what version you want to merge in.")
            merged[i] = {"1": merged[i], "2": tomerge[i]}[input(f"1. {merged[i]}\n"
                                                                f"2. {tomerge[i]}\n").strip()]
            print("Merge conflict resolved.")
            continue
        merged[i] = tomerge[i]
    mergedfile = Data.DATAPATH.join("merged-stats.json")
    with open(mergedfile, "x", encoding="UTF-8") as f:
        json.dump(merged, f, indent=2)


if __name__ == "__main__":
    initializescript(__file__)
    print(f"{Fore.GREEN}No errors found in {__file__}.")
