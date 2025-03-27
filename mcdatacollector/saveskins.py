import os
from datetime import datetime
from time import sleep

import requests
from colorama import Fore

from mcdatacollector import datafile, Data, initializescript

__allowed_types__ = ["html", "urls", "skins"]


def initsave(__type: str) -> tuple[str, dict]:
    data: dict = datafile.load()

    if __type not in __allowed_types__:
        return os.curdir, data

    foldername = (
        f"{Data.HTMLPATH if __type == 'html' else Data.SKINSURLPATH if __type == 'urls' else Data.SKINSPATH}\\"

        f"{datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')}")

    print(f"{Fore.GREEN}Creating new folder... ({foldername})")

    os.mkdir(foldername)

    print(f"{Fore.GREEN}Folder {foldername} created successfully.")
    print(f"{Fore.GREEN}Saving new files...")

    return foldername, data


def saveurls():
    foldername, data = initsave("urls")

    for i in data:
        url = data[i]["skin_url"]
        if url is not None:
            response = requests.get(url=url)
            with open(rf"{foldername}\{url[39:]}.png", "wb") as file:
                file.write(response.content)
            print(f"{Fore.GREEN}Saved {url[39:]}.png")
        sleep(0.5)


def savenames():
    foldername, data = initsave("skins")
    for i in data:
        url = data[i]["skin_url"]
        if url is not None:
            response = requests.get(url=url)
            name = data[i]["name"]
            with open(
                    rf"{foldername}\{name}.png",
                    "wb",
            ) as file:
                file.write(response.content)
            print(f"{Fore.GREEN}Saved {name}.png")
        sleep(0.5)
    del foldername


def savehtml():
    foldername, data = initsave("html")
    for i in data:
        if data[i]["does_exist"]:
            name = data[i]["name"]
            to_save = rf'<iframe src="https://minerender.org/embed/skin/?skin={name}&shadow=true" \
                                frameborder="0" width="1920px" height="972px"></iframe>'
            with open(rf"{foldername}\{name}.html", "x") as file:
                file.write(to_save)
            print(f"{Fore.GREEN}Saved {name}.html")
    del foldername


def saveeverything():
    data = datafile.load()
    foldername = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    for i in Data.__dirs__:
        os.mkdir(rf"{i}/{foldername}")
        print(f"{Fore.GREEN}Folder {rf'{i}/{foldername}'} was created.")

    for i in data:
        if data[i]["does_exist"]:
            name = data[i]["name"]
            skin_url = data[i]["skin_url"]

            response = requests.get(url=skin_url)

            with open(rf"{Data.SKINSPATH}\{foldername}\{name}.png", "wb") as file:
                file.write(response.content)
            with open(rf"{Data.SKINSURLPATH}\{foldername}\{skin_url[39:]}.png", "wb") as file:
                file.write(response.content)
            with open(rf"{Data.HTMLPATH}\{foldername}\{name}.html", "x") as file:
                file.write(rf'<iframe src="https://minerender.org/embed/skin/?skin={name}&shadow=true" \
                                frameborder="0" width="1920px" height="972px"></iframe>')
            sleep(0.5)
            print(f"{Fore.GREEN}Saved {name} ({skin_url})")


if __name__ == "__main__":
    initializescript(__file__)
    print(f"{Fore.GREEN}No errors found in {__file__}.")
