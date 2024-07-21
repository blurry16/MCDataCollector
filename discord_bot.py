import json
from datetime import datetime
from time import time

import disnake
from disnake.ext import commands
from mojang import API, errors

from mcdatacollector import cvdbdata

mapi = API()

activity = disnake.Activity(name="Forrest Gump", type=disnake.ActivityType.watching)
bot = commands.Bot(
    command_prefix="$",
    intents=disnake.Intents.all(),
    activity=activity,
    status=disnake.Status.offline,
)
TOKEN = ""


@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready!")


@bot.slash_command(
    description="Check last time when a selected player was seen online. (if the bot saw them online)"
)
async def lastseen(ctx, nickname):
    print(f"{ctx.author} used /lastseen {nickname}")
    data = cvdbdata.load()
    try:
        uuid = mapi.get_uuid(nickname)
        if uuid in data:
            last_seen = data[uuid]["last_seen"]
            await ctx.send(
                f"{data[uuid]['name']} was last seen at <t:{last_seen}:f> (shows in local time). ({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(last_seen)} ago.)"
            )
        else:
            await ctx.send("The bot has never seen this player.", ephemeral=True)
    except errors.NotFound:
        nickname = nickname.lower()
        if nickname in data:
            last_seen = data[nickname]["last_seen"]
            await ctx.send(
                f"{data[nickname]['name']} was last seen at <t:{last_seen}:f> (shows in local time). ({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(last_seen)} ago.)"
            )
        else:
            await ctx.send(f"Player {nickname} doesn't exist.", ephemeral=True)


@bot.slash_command(
    description="Check the first time when the bot has seen selected player."
)
async def firsttimeseen(ctx, nickname):
    print(f"{ctx.author} used /firsttimeseen {nickname}")
    data = cvdbdata.load()
    try:
        uuid = mapi.get_uuid(nickname)
        if uuid in data:
            first_time_seen = data[uuid]["first_time_seen"]
            await ctx.send(
                f"{data[uuid]['name']} was seen for the first time at <t:{first_time_seen}:f> (shows in local time). ({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(first_time_seen)} ago.)"
            )
        else:
            await ctx.send("The bot has never seen this player.", ephemeral=True)
    except errors.NotFound:
        nickname = nickname.lower()
        if nickname in data:
            first_time_seen = data[nickname]["first_time_seen"]
            await ctx.send(
                f"{data[nickname]['name']} was seen for the first time at <t:{first_time_seen}:f> (shows in local time). ({datetime.fromtimestamp(round(time())) - datetime.fromtimestamp(first_time_seen)} ago.)"
            )
        else:
            await ctx.send(f"Player {nickname} doesn't exist.", ephemeral=True)


@bot.slash_command(description="Get database player's id with their nickname.")
async def getdbid(ctx, nickname):
    print(f"{ctx.author} used /getdbid {nickname}")
    data = cvdbdata.load()
    try:
        uuid = mapi.get_uuid(nickname)
        if uuid in data:
            await ctx.send(
                f"{data[uuid]['name']}'s database ID is {data[uuid]['db_id']}."
            )
        else:
            await ctx.send("The bot has never seen this player.", ephemeral=True)
    except errors.NotFound:
        nickname = nickname.lower()
        if nickname in data:
            await ctx.send(
                f"{data[nickname]['name']}'s database ID is {data[nickname]['db_id']}"
            )
        else:
            await ctx.send(f"Player {nickname} doesn't exist.", ephemeral=True)


@bot.slash_command(
    description="Returns data of selected player from the database in JSON format."
)
async def getdata(ctx, nickname, indent=2):
    print(f"{ctx.author} used /getdata {nickname}")

    try:
        indent = int(indent)
    except ValueError:
        indent = 2

    indent = 2 if (0 > indent) or (indent > 20) else indent
    data = cvdbdata.load()
    try:
        uuid = mapi.get_uuid(nickname)
        if uuid in data:
            await ctx.send(f"```json\n{json.dumps(data[uuid], indent=indent)}```")
        else:
            await ctx.send("The bot has never seen this player.", ephemeral=True)
    except errors.NotFound:
        nickname = nickname.lower()
        if nickname in data:
            await ctx.send(f"```json\n{json.dumps(data[nickname], indent=indent)}```")
        else:
            await ctx.send(f"Player {nickname} doesn't exist.", ephemeral=True)


@bot.slash_command(description="Check the count of players in the database.")
async def count(ctx):
    print(f"{ctx.author} used /count")
    data = cvdbdata.load()
    await ctx.send(f"There are {len(data)} players in the database.")


@bot.slash_command(description="Project in a nutshell")
async def description(ctx):
    print(f"{ctx.author} used /description")
    await ctx.send(
        (
            f"# This project is NOT run by Cubeville staff. Everything is done by blurry16.\nYour personal data is not collected, your account is completely safe ||(only Mojang API data, last/first time joined/left the server are collected)||."
        )
        + (
            f"\nSource code can be gotten [here](https://github.com/blurry16/MCDataCollector).\n\n*Licensed under MIT License, Copyright (c) 2024 blurry16*"
        ),
        ephemeral=True,
    )


bot.run(TOKEN)
