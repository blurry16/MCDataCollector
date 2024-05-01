import disnake
import json
from time import time
from datetime import datetime
from mojang import API, errors
from disnake.ext import commands
from __data__ import cvdbdata

mapi = API()

activity = disnake.Activity(name="Forrest Gump", type=disnake.ActivityType.watching)
bot = commands.Bot(
    command_prefix="$",
    intents=disnake.Intents.all(),
    activity=activity,
    status=disnake.Status.idle,
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
            last_seen = datetime.fromtimestamp(data[uuid]["last_seen"])
            await ctx.send(
                f"{data[uuid]['name']} was last seen at {last_seen} UTC+3. ({datetime.fromtimestamp(round(time())) - last_seen} ago.)"
            )
        else:
            await ctx.send("The bot has never seen this player.", ephemeral=True)
    except errors.NotFound:
        nickname = nickname.lower()
        if nickname in data:
            last_seen = datetime.fromtimestamp(data[nickname]["last_seen"])
            await ctx.send(
                f"{data[nickname]['name']} was last seen at {last_seen} UTC+3 ({datetime.fromtimestamp(round(time())) - last_seen} ago.)"
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
            first_time_seen = datetime.fromtimestamp(data[uuid]["first_time_seen"])
            await ctx.send(
                f"{data[uuid]['name']} was seen for the first time at {first_time_seen} UTC+3. ({datetime.fromtimestamp(round(time())) - first_time_seen} ago.)"
            )
        else:
            await ctx.send("The bot has never seen this player.", ephemeral=True)
    except errors.NotFound:
        nickname = nickname.lower()
        if nickname in data:
            first_time_seen = datetime.fromtimestamp(data[nickname]["first_time_seen"])
            await ctx.send(
                f"{data[nickname]['name']} was seen for the first time at {first_time_seen} UTC+3. ({datetime.fromtimestamp(round(time())) - first_time_seen} ago.)"
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
async def getdata(ctx, nickname):
    print(f"{ctx.author} used /getdata {nickname}")
    data = cvdbdata.load()
    try:
        uuid = mapi.get_uuid(nickname)
        if uuid in data:
            await ctx.send(f"```json\n{json.dumps(data[uuid], indent=4)}```")
        else:
            await ctx.send("The bot has never seen this player.", ephemeral=True)
    except errors.NotFound:
        nickname = nickname.lower()
        if nickname in data:
            await ctx.send(f"```json\n{json.dumps(data[nickname], indent=4)}```")
        else:
            await ctx.send(f"Player {nickname} doesn't exist.", ephemeral=True)


@bot.slash_command(description="Check the count of players in the database.")
async def count(ctx):
    print(f"{ctx.author} used /count")
    data = cvdbdata.load()
    await ctx.send(f"There are {len(data)} players in the database.")


bot.run(TOKEN)
