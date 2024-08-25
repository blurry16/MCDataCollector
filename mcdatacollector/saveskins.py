if __name__ == "__main__":
    raise Exception("Please don't run mcdatacollector package files.")

import os
from datetime import datetime
from time import sleep

import requests
from colorama import Fore

from mcdatacollector import datafile, MODELSPATH, SKINSPATH, SKINSURLPATH, __dirs__

__allowed_types__ = ["models", "urls", "skins"]


def initsaving(__type: str):
    data = datafile.load()

    if __type not in __allowed_types__:
        return os.curdir,

    foldername = (f"{MODELSPATH if __type == 'models' else SKINSURLPATH if __type == 'urls' else SKINSPATH}\\"

                  f"{datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')}")

    print(f"{Fore.GREEN}Creating new folder... ({foldername})")

    os.mkdir(foldername)

    print(f"{Fore.GREEN}Folder {foldername} created successfully.")
    print(f"{Fore.GREEN}Saving new files...")

    return foldername, data


def saveurls():
    foldername, data = initsaving("urls")

    for i in data:
        url = data[i]["skin_url"]
        if url is not None:
            response = requests.get(url=url)
            with open(rf"{foldername}\{url[39:]}.png", "wb") as file:
                file.write(response.content)
            print(f"{Fore.GREEN}Saved {url[39:]}.png")
        sleep(0.5)


def savenames():
    foldername, data = initsaving("skins")
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
    foldername, data = initsaving("models")
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
    for i in __dirs__:
        os.mkdir(rf"{i}/{foldername}")
        print(f"{Fore.GREEN}Folder {rf'{i}/{foldername}'} was created.")

    for i in data:
        if data[i]["does_exist"]:
            name = data[i]["name"]
            skin_url = data[i]["skin_url"]

            response = requests.get(url=skin_url)

            with open(rf"{SKINSPATH}\{foldername}\{name}.png", "wb") as file:
                file.write(response.content)
            with open(rf"{SKINSURLPATH}\{foldername}\{skin_url[39:]}.png", "wb") as file:
                file.write(response.content)
            with open(rf"{MODELSPATH}\{foldername}\{name}.html", "x") as file:
                file.write(rf'<iframe src="https://minerender.org/embed/skin/?skin={name}&shadow=true" \
                                frameborder="0" width="1920px" height="972px"></iframe>')
            sleep(0.5)
            print(f"{Fore.GREEN}Saved {name} ({skin_url})")
