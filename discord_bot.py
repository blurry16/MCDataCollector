import json
from datetime import datetime
from time import time

import disnake
from disnake.ext import commands
from mojang import API, errors

from mcdatacollector import datafile

mapi = API()

activity = disnake.Activity(name="Forrest Gump", type=disnake.ActivityType.watching)
bot = commands.Bot(
    command_prefix="$",
    intents=disnake.Intents.all(),
    activity=activity,
    status=disnake.Status.offline,
)
TOKEN = ""


async def dbidcheck(db_id: int, inter: disnake.ApplicationCommandInteraction) -> str | None:
    if db_id < 0:
        return await inter.send("Database ID must be greater or equal 0.", ephemeral=True)
    data = datafile.load()
    if db_id > len(data):
        return await inter.send("There's no such player with this Database ID.", ephemeral=True)

    return list(data)[db_id]


@bot.event
async def on_ready() -> None:
    print(f"Bot {bot.user} is ready!")


@bot.slash_command(
    description="Check last time when a selected player was seen online. (if the bot saw them online)"
)
async def lastseen(inter: disnake.ApplicationCommandInteraction, nickname: str = None, uuid: str = None,
                   db_id: int = None) -> None:
    if nickname is not None and uuid is None and db_id is None:
        print(f"{inter.author} used /lastseen nickname={nickname}")
        data = datafile.load()
        try:
            uuid = mapi.get_uuid(nickname)
            if uuid in data:
                last_seen = data[uuid]["last_seen"]
                await inter.send(
                    f"{data[uuid]['name']} was last seen at <t:{last_seen}:f>. "
                    f"({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(last_seen)} ago.)"
                )
            else:
                await inter.send("The bot has never seen this player.", ephemeral=True)
        except errors.NotFound:
            nickname = nickname.lower()
            if nickname in data:
                last_seen = data[nickname]["last_seen"]
                await inter.send(
                    f"{data[nickname]['name']} was last seen at <t:{last_seen}:f>. "
                    f"({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(last_seen)} ago.)"
                )
            else:
                await inter.send(f"Player {nickname} doesn't exist.", ephemeral=True)
    elif uuid is not None and nickname is None and db_id is None:
        print(f"{inter.author} used /lastseen uuid={uuid}")
        uuid = uuid.replace("-", "")
        data = datafile.load()
        if uuid in data:
            last_seen = data[uuid]["last_seen"]
            await inter.send(
                f"{data[uuid]['name']} ({uuid}) was last seen at <t:{last_seen}:f>. "
                f"({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(last_seen)} ago.)"
            )
        else:
            await inter.send("There's no such player in the Database with this UUID.", ephemeral=True)

    elif db_id is not None and nickname is None and uuid is None:
        print(f"{inter.author} used /lastseen db_id={db_id}")
        uuid = await dbidcheck(db_id, inter)
        if uuid is None:
            return
        data = datafile.load()
        last_seen = data[uuid]["last_seen"]
        await inter.send(
            f"{data[uuid]['name']} ({db_id}) was last seen at <t:{last_seen}:f>. "
            f"({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(last_seen)} ago.)"
        )
    elif nickname is None and uuid is None and db_id is None:
        await inter.send("Too few arguments!", ephemeral=True)
    else:
        await inter.send("Too many arguments!", ephemeral=True)


@bot.slash_command(
    description="Check the first time when the bot has seen selected player."
)
async def firsttimeseen(inter: disnake.ApplicationCommandInteraction, nickname: str = None, uuid: str = None,
                        db_id: int = None) -> None:
    if nickname is not None and uuid is None and db_id is None:
        print(f"{inter.author} used /firsttimeseen nickname={nickname}")
        data = datafile.load()
        try:
            uuid = mapi.get_uuid(nickname)
            if uuid in data:
                first_time_seen = data[uuid]["first_time_seen"]
                await inter.send(
                    f"{data[uuid]['name']} was seen for the first time at <t:{first_time_seen}:f>. "
                    f"({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(first_time_seen)} ago.)"
                )
            else:
                await inter.send("The bot has never seen this player.", ephemeral=True)
        except errors.NotFound:
            nickname = nickname.lower()
            if nickname in data:
                first_time_seen = data[nickname]["first_time_seen"]
                await inter.send(
                    f"{data[nickname]['name']} was seen for the first time at <t:{first_time_seen}:f>. "
                    f"({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(first_time_seen)} ago.)"
                )
            else:
                await inter.send(f"Player {nickname} doesn't exist.", ephemeral=True)
    elif uuid is not None and nickname is None and db_id is None:
        print(f"{inter.author} used /firsttimeseen uuid={uuid}")
        uuid = uuid.replace("-", "")
        data = datafile.load()
        if uuid in data:
            first_time_seen = data[uuid]["first_time_seen"]
            await inter.send(
                f"{data[uuid]['name']} ({uuid}) was seen for the first time at <t:{first_time_seen}:f>. "
                f"({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(first_time_seen)} ago.)"
            )
        else:
            await inter.send("There's no such player in the Database with this UUID.", ephemeral=True)

    elif db_id is not None and nickname is None and uuid is None:
        print(f"{inter.author} used /firsttimeseen db_id={db_id}")
        uuid = await dbidcheck(db_id, inter)
        if uuid is None:
            return
        data = datafile.load()
        first_time_seen = data[uuid]["first_time_seen"]
        await inter.send(
            f"{data[uuid]['name']} ({db_id}) was seen for the first time at <t:{first_time_seen}:f>. "
            f"({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(first_time_seen)} ago.)"
        )
    elif nickname is None and uuid is None and db_id is None:
        await inter.send("Too few arguments!", ephemeral=True)
    else:
        await inter.send("Too many arguments!", ephemeral=True)


@bot.slash_command(description="Get database player's id with their nickname.")
async def getdbid(inter: disnake.ApplicationCommandInteraction, nickname: str = None, uuid: str = None) -> None:
    if nickname is not None and uuid is None:
        print(f"{inter.author} used /getdbid nickname={nickname}")
        data = datafile.load()
        try:
            uuid = mapi.get_uuid(nickname)
            if uuid in data:
                await inter.send(
                    f"{data[uuid]['name']}'s database ID is {data[uuid]['db_id']}."
                )
            else:
                await inter.send("The bot has never seen this player.", ephemeral=True)
        except errors.NotFound:
            nickname = nickname.lower()
            if nickname in data:
                await inter.send(
                    f"{data[nickname]['name']}'s database ID is {data[nickname]['db_id']}"
                )
            else:
                await inter.send(f"Player {nickname} doesn't exist.", ephemeral=True)
    elif uuid is not None and nickname is None:
        print(f"{inter.author} used /getdbid uuid={uuid}")
        uuid = uuid.replace("-", "")
        data = datafile.load()
        if uuid in data:
            await inter.send(
                f"{data[uuid]['name']}'s ({uuid}) database ID is {data[uuid]['db_id']}."
            )
        else:
            await inter.send("There's no such player in the Database with this UUID", ephemeral=True)
    elif nickname is not None and uuid is not None:
        await inter.send("Too few arguments!", ephemeral=True)
    else:
        await inter.send("Too many arguments!", ephemeral=True)


@bot.slash_command(
    description="Returns data of selected player from the database in JSON format."
)
async def getdata(inter: disnake.ApplicationCommandInteraction, nickname: str = None, uuid: str = None,
                  db_id: int = None,
                  indent: int = 2) -> None:
    if nickname is not None and uuid is None and db_id is None:
        print(f"{inter.author} used /getdata nickname={nickname}")
        indent = 2 if (0 > indent) or (indent > 20) else indent
        data = datafile.load()
        try:
            uuid = mapi.get_uuid(nickname)
            if uuid in data:
                await inter.send(f"```json\n{json.dumps(data[uuid], indent=indent)}```")
            else:
                await inter.send("The bot has never seen this player.", ephemeral=True)
        except errors.NotFound:
            nickname = nickname.lower()
            if nickname in data:
                await inter.send(f"```json\n{json.dumps(data[nickname], indent=indent)}```")
            else:
                await inter.send(f"Player {nickname} doesn't exist.", ephemeral=True)
    elif uuid is not None and nickname is None and db_id is None:
        print(f"{inter.author} used /getdata uuid={uuid}")
        uuid = uuid.replace("-", "")
        data = datafile.load()
        if uuid in data:
            await inter.send(f"```json\n{json.dumps(data[uuid], indent=indent)}```")
        else:
            await inter.send("There's no such player in the Database with this UUID.", ephemeral=True)
    elif db_id is not None and nickname is None and uuid is None:
        print(f"{inter.author} used /getdata db_id={db_id}")
        uuid = await dbidcheck(db_id, inter)
        if uuid is None:
            return
        data = datafile.load()
        if uuid in data:
            await inter.send(f"```json\n{json.dumps(data[uuid], indent=indent)}```")
        else:
            await inter.send("There's no such player in the Database with this UUID.", ephemeral=True)
    elif nickname is None and uuid is None and db_id is None:
        await inter.send("Too few arguments!", ephemeral=True)
    else:
        await inter.send("Too many arguments!", ephemeral=True)


@bot.slash_command(description="Check the count of players in the database.")
async def count(inter: disnake.ApplicationCommandInteraction) -> None:
    print(f"{inter.author} used /count")
    data = datafile.load()
    await inter.send(f"There are {len(data)} players in the database.")


@bot.slash_command(description="Project in a nutshell")
async def description(inter: disnake.ApplicationCommandInteraction) -> None:
    print(f"{inter.author} used /description")
    await inter.send(
        f"# This project is NOT run by Cubeville staff. Everything is done by blurry16.\n"
        f"Your personal data is not collected, your account is completely safe "
        f"||(only Mojang API data, last/first time joined/left the server are collected)||."
        f"\nSource code can be gotten [here](https://github.com/blurry16/MCDataCollector).\n"
        f"\n"
        f"*Licensed under MIT License, Copyright (c) 2024 blurry16*",
        ephemeral=True,
    )


bot.run(TOKEN)
