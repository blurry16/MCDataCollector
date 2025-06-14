"""--dumprm: removes a dump from hard drive after posting"""

import logging
import time
from pathlib import Path
from sys import argv

import disnake
from disnake.ext import commands
from dotenv import dotenv_values

import mcdatacollector.mojang as mcdcapi
from mcdatacollector import datafile, getuuid, initializescript
from mcdatacollector import mcdcdumps, dotenvpath

# mapi = API()
argv = [i.lower() for i in argv[1:]]

activity = disnake.Activity(name="Forrest Gump", type=disnake.ActivityType.watching)
bot = commands.Bot(
    command_prefix="$",
    intents=disnake.Intents.all(),
    activity=activity,
    status=disnake.Status.offline,
)
TOKEN = dotenv_values(dotenvpath)["DISCORD_BOT_TOKEN"]

logging.basicConfig()
logger = logging.getLogger("mcdc.discord_bot")
logger.setLevel(logging.INFO)

dumprm = "--dumprm" in argv
if dumprm:
    logger.info("this session is run with --dumprm argument. the dump will be removed after posting")


async def dbidcheck(db_id: int, inter: disnake.ApplicationCommandInteraction) -> str | None:
    if db_id < 0:
        return await inter.send("Database ID must be greater or equal 0.", ephemeral=True)
    data = datafile.load()
    if db_id >= len(data):
        return await inter.send("There's no such player with this Database ID.", ephemeral=True)

    return list(data)[db_id]


async def parsearguments(inter: disnake.ApplicationCommandInteraction, nickname: str | None, uuid: str | None,
                         db_id: int | None = -1) -> bool:
    if [nickname, uuid, db_id if db_id != -1 else None].count(None) != 2:
        await inter.send("Too few arguments!" if [nickname, uuid, db_id if db_id != -1 else None].count(
            None) > 2 else "Too many arguments!",
                         ephemeral=True)
        return False
    return True


@bot.event
async def on_ready() -> None:
    logger.info(f"Bot {bot.user} is ready!")


@bot.slash_command(description="Check last time when a selected player was seen online. (if the bot saw them online)")
async def lastseen(inter: disnake.ApplicationCommandInteraction, nickname: str = None, uuid: str = None,
                   db_id: int = None) -> None:
    if not await parsearguments(inter, nickname, uuid, db_id):
        return
    data = datafile.load()
    if nickname is not None:
        logger.info(f"{inter.author} used /lastseen {nickname=}")
        try:
            uuid = getuuid(nickname)
            if uuid in data:
                last_seen = data[uuid]["last_seen"]
                await inter.send(
                    f"{data[uuid]['name']} was last seen at <t:{last_seen}:f>. "
                    f"(<t:{last_seen}:R>)"
                )
            else:
                await inter.send("The bot has never seen this player.", ephemeral=True)
        except mcdcapi.NotFoundException:
            nickname = nickname.lower()
            if nickname in data:
                last_seen = data[nickname]["last_seen"]
                await inter.send(
                    f"{data[nickname]['name']} was last seen at <t:{last_seen}:f>. "
                    f"(<t:{last_seen}:R>)"
                )
            else:
                await inter.send(f"Player {nickname} doesn't exist.", ephemeral=True)
    elif uuid is not None:
        logger.info(f"{inter.author} used /lastseen uuid={uuid}")
        uuid = uuid.replace("-", "")
        if uuid in data:
            last_seen = data[uuid]["last_seen"]
            await inter.send(
                f"{data[uuid]['name']} ({uuid=}) was last seen at <t:{last_seen}:f>. "
                f"(<t:{last_seen}:R>)"
            )
        else:
            await inter.send("There's no such player in the Database with this UUID.", ephemeral=True)

    else:
        logger.info(f"{inter.author} used /lastseen db_id={db_id}")
        uuid = await dbidcheck(db_id, inter)
        if uuid is None:
            return
        last_seen = data[uuid]["last_seen"]
        await inter.send(
            f"{data[uuid]['name']} ({db_id=}) was last seen at <t:{last_seen}:f>. "
            f"(<t:{last_seen}:R>)"
        )


@bot.slash_command(description="Check the first time when the bot has seen selected player.")
async def firsttimeseen(inter: disnake.ApplicationCommandInteraction, nickname: str = None, uuid: str = None,
                        db_id: int = None) -> None:
    if not await parsearguments(inter, nickname, uuid, db_id):
        return

    if nickname is not None:
        logger.info(f"{inter.author} used /firsttimeseen nickname={nickname}")
        data = datafile.load()
        try:
            uuid = getuuid(nickname)
            if uuid in data:
                first_time_seen = data[uuid]["first_time_seen"]
                await inter.send(
                    f"{data[uuid]['name']} was seen for the first time at <t:{first_time_seen}:f>. "
                    f"(<t:{first_time_seen}:R>)"
                )
            else:
                await inter.send("The bot has never seen this player.", ephemeral=True)
        except mcdcapi.NotFoundException:
            nickname = nickname.lower()
            if nickname in data:
                first_time_seen = data[nickname]["first_time_seen"]
                await inter.send(
                    f"{data[nickname]['name']} was seen for the first time at <t:{first_time_seen}:f>. "
                    f"(<t:{first_time_seen}:R>)"
                )
            else:
                await inter.send(f"Player {nickname} doesn't exist.", ephemeral=True)
    elif uuid is not None:
        logger.info(f"{inter.author} used /firsttimeseen uuid={uuid}")
        uuid = uuid.replace("-", "")
        data = datafile.load()
        if uuid in data:
            first_time_seen = data[uuid]["first_time_seen"]
            await inter.send(
                f"{data[uuid]['name']} ({uuid=}) was seen for the first time at <t:{first_time_seen}:f>. "
                f"(<t:{first_time_seen}:R>)"
            )
        else:
            await inter.send("There's no such player in the Database with this UUID.", ephemeral=True)

    else:
        logger.info(f"{inter.author} used /firsttimeseen db_id={db_id}")
        uuid = await dbidcheck(db_id, inter)
        if uuid is None:
            return
        data = datafile.load()
        first_time_seen = data[uuid]["first_time_seen"]
        await inter.send(
            f"{data[uuid]['name']} ({db_id=}) was seen for the first time at <t:{first_time_seen}:f>. "
            f"(<t:{first_time_seen}:R>)"
        )


@bot.slash_command(description="Get database player's id with their nickname.")
async def getdbid(inter: disnake.ApplicationCommandInteraction, nickname: str = None, uuid: str = None) -> None:
    if not await parsearguments(inter, nickname, uuid):
        return
    if nickname is not None and uuid is None:
        logger.info(f"{inter.author} used /getdbid nickname={nickname}")
        data = datafile.load()
        try:
            uuid = getuuid(nickname)
            if uuid in data:
                await inter.send(
                    f"{data[uuid]['name']}'s database ID is {data[uuid]['db_id']}."
                )
            else:
                await inter.send("The bot has never seen this player.", ephemeral=True)
        except mcdcapi.NotFoundException:
            nickname = nickname.lower()
            if nickname in data:
                await inter.send(
                    f"{data[nickname]['name']}'s database ID is {data[nickname]['db_id']}"
                )
            else:
                await inter.send(f"Player {nickname} doesn't exist.", ephemeral=True)
    elif uuid is not None and nickname is None:
        logger.info(f"{inter.author} used /getdbid uuid={uuid}")
        uuid = uuid.replace("-", "")
        data = datafile.load()
        if uuid in data:
            await inter.send(
                f"{data[uuid]['name']}'s ({uuid=}) database ID is {data[uuid]['db_id']}."
            )
        else:
            await inter.send("There's no such player in the Database with this UUID", ephemeral=True)


@bot.slash_command(description="Performs a search using nickname, uuid or db id")
async def getdata(inter: disnake.ApplicationCommandInteraction, nickname: str = None, uuid: str = None,
                  db_id: int = None,
                  indent: int = 2) -> None:
    if not await parsearguments(inter, nickname, uuid, db_id):
        return

    if nickname is not None:
        logger.info(f"{inter.author} used /getdata nickname={nickname}")
        indent = 2 if (0 > indent) or (indent > 20) else indent
        data = datafile.load()
        try:
            uuid = getuuid(nickname)
            if uuid in data:
                await inter.send(f"```json\n{datafile.dumps(uuid, indent=indent)}```")
            else:
                await inter.send("The bot has never seen this player.", ephemeral=True)
        except mcdcapi.NotFoundException:
            nickname = nickname.lower()
            if nickname in data:
                await inter.send(f"```json\n{datafile.dumps(nickname, indent=indent)}```")
            else:
                await inter.send(f"Player {nickname} doesn't exist.", ephemeral=True)
    elif uuid is not None:
        logger.info(f"{inter.author} used /getdata uuid={uuid}")
        uuid = uuid.replace("-", "")
        data = datafile.load()
        if uuid in data:
            await inter.send(f"```json\n{datafile.dumps(uuid, indent=indent)}```")
        else:
            await inter.send("There's no such player in the Database with this UUID.", ephemeral=True)
    else:
        logger.info(f"{inter.author} used /getdata db_id={db_id}")
        uuid = await dbidcheck(db_id, inter)
        if uuid is None:
            return
        data = datafile.load()
        if uuid in data:
            await inter.send(f"```json\n{datafile.dumps(uuid, indent=indent)}```")
        else:
            await inter.send("There's no such player in the Database with this UUID.", ephemeral=True)


@bot.slash_command(description="Check the count of players in the database.")
async def count(inter: disnake.ApplicationCommandInteraction) -> None:
    logger.info(f"{inter.author} used /count")
    data = datafile.load()
    await inter.send(f"There are {len(data)} players in the database.")


def __unlink(path: Path):
    """
    Unlinks the path and logs it
    :param path:
    :return:
    """
    path.unlink()
    logger.info(f"{path} removed")


@bot.slash_command(description="Get full data dump in DB (csv format)")
async def getfulldata(inter: disnake.ApplicationCommandInteraction) -> None:
    # async def getfulldata(inter: disnake.ApplicationCommandInteraction, format: bool) -> None:
    logger.info(f"{inter.author} used /getfulldata")
    await inter.response.defer()
    # if format:
    path = mcdcdumps.dumpfullcsv()
    await inter.edit_original_message(file=disnake.File(path, path.name))
    if dumprm:
        __unlink(path)
    # return await inter.send(file=disnake.File(datafile.file_path, __gendumpname("json")))


@bot.slash_command(description="Get all uuids:usernames in DB (csv format)")
async def getplayers(inter: disnake.ApplicationCommandInteraction) -> None:
    logger.info(f"{inter.author} used /getplayer")
    await inter.response.defer()
    path = mcdcdumps.dumpplayerscsv()
    await inter.edit_original_message(file=disnake.File(path, path.name))
    if dumprm:
        __unlink(path)


# @bot.slash_command(description="Project in a nutshell")
# async def description(inter: disnake.ApplicationCommandInteraction) -> None:
#     logger.info(f"{inter.author} used /description")
#     await inter.send(
#         f"# This project is NOT run by Cubeville staff. Everything is done by blurry16.\n"
#         f"Your personal data is not collected, your account is completely safe. "
#         f"Only Mojang API data, last/first time joined/left the server are collected."
#         f"\nSource code can be obtained **[here](https://github.com/blurry16/MCDataCollector)**.\n"
#         f"\n"
#         f"*Licensed under **[MIT License](https://github.com/blurry16/MCDataCollector/tree/main/LICENSE)**, " +
#         open("LICENSE").read().split("\n")[2] + "*",
#         ephemeral=True,
#     )


def main():
    # It's here because logger works faster than regular print, logo is printed after the first log line.
    time.sleep(.1)

    logger.info("Starting up the bot...")
    bot.run(TOKEN)


if __name__ == "__main__":
    initializescript("discord_bot")
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
