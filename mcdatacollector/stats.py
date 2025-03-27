from datetime import datetime, UTC
from json import dumps

from colorama import Fore

from mcdatacollector import datafile, statsdataobj, initializescript


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
    print(dumps(statsdata, indent=2) + "\n")
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


if __name__ == "__main__":
    initializescript(__file__)
    print(f"{Fore.GREEN}No errors found in {__file__}.")
