from datetime import datetime, UTC
from json import dumps

from colorama import Fore

from mcdatacollector import datafile, statsdataobj


def savestats():
    data_len = len(datafile.load())
    statsdata: dict = statsdataobj.load()
    last_date = list(statsdata)[-1]
    # now_date = (datetime.now().date() - timedelta(days=1)).strftime("%Y-%m-%d")
    now_date = datetime.now(UTC).date().strftime("%Y-%m-%d")
    print(now_date)
    statsdata[now_date] = {
        "count": data_len,
        "delta": data_len - int(statsdata[last_date]["count"]),
    }

    print(dumps(statsdata, indent=2) + "\n")
    a = input(f"{Fore.GREEN}Proceed? {Fore.RESET}y/n: ").strip()
    if a.lower() in ["y", ""]:
        statsdataobj.dump(statsdata)


def parsestats():
    stats = statsdataobj.load()
    for i in stats:
        print(f"{i}: {stats[i]['count']} players, {stats[i]['delta']} delta.")


def parseraw():
    print(statsdataobj.dumps())


if __name__ == "__main__":
    print(f"{Fore.GREEN}No errors found in {__file__}.")
