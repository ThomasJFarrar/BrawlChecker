"""This module runs the Brawl Checker Discord bot"""

import discord
import requests
from discord.ext import commands

TOKEN = "Replace this with your Discord bot token"

APIKEY = "Replace this with your Brawl Stars API key"
APIURL = "https://api.brawlstars.com/v1/"

# Store the club requirements once set.
requirements = {
    "clubname": None,
    "minTrophies": None,
    "minMaxedBrawlers": None,
    "min3v3wins": None
}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

def search_and_set_club(tag: str) -> str:
    """Search for the club by tag and set the trophies required.
    
    Args:
        tag (str): The club tag.

    Returns:
        str: A message saying if the club was set or if it was invalid.
    
    """
    # Search for the club by tag.
    response = requests.get(
        APIURL + "clubs/%23" + tag.upper().strip("#"), # Adds the hashtag to the start of the tag.
        headers={"Authorization" : "Bearer " + APIKEY},
        timeout=5
    )

    if response.status_code == 200:
        clubdata = response.json()
        requirements.update({"clubname": clubdata["name"], \
                             "minTrophies": clubdata["requiredTrophies"]})
        return "Club Set: " + clubdata["name"]
    return "Invalid club tag"

def get_num_maxed_brawlers(playerdata: dict) -> int:
    """Check how many maxed brawlers a player has.
    
    Args:
        playerdata (dict): The player's data.

    Returns:
        int: The number of maxed brawlers the player has.

    """
    brawlers = playerdata["brawlers"]

    # Add up how many maxed brawlers the player has.
    maxedbrawlercount = 0
    for brawler in brawlers:
        if brawler["power"] == 11 and \
           len(brawler["starPowers"]) >= 1 and \
           len(brawler["gadgets"]) >= 1 and \
           len(brawler["gears"]) >= 2:
            maxedbrawlercount += 1

    return maxedbrawlercount

def check_player(tag: str) -> str:
    """Search for a player by tag and check if they meet the club requirements.
    
    Args:
        tag (str): The player's tag.

    Returns:
        str: A message saying whether the player meets the requirements or not.

    """
    # Search for the player by tag.
    response = requests.get(
        APIURL + "players/%23" + tag.upper().strip("#"), # Adds the hashtag to the start of the tag.
        headers={"Authorization" : "Bearer " + APIKEY},
        timeout=5
    )

    # Check that the api response was successful.
    if response.status_code == 200:
        playerdata = response.json()

        # Check that the player meets all the requirements.
        if playerdata["trophies"] >= requirements["minTrophies"] and \
           get_num_maxed_brawlers(playerdata) >= requirements["minMaxedBrawlers"] and \
           playerdata["3vs3Victories"] >= requirements["min3v3wins"]:
            return "Player meets club requirements"
        return "Player does not meet club requirements"

    return "Invalid player tag"

@bot.command()
@commands.has_permissions(administrator=True)
async def setclub(ctx, tag):
    """Set the club by tag, updating the club requirements.
    
    Args:
        ctx (discord.ext.commands.Context): The context of the command.
        tag (str): The club tag.

    Returns:
        None

    """
    message = search_and_set_club(tag)
    await ctx.reply(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def setminmaxedbrawlers(ctx, num):
    """Set the minimum number of maxed out brawlers required.
    
    Args:
        ctx (discord.ext.commands.Context): The context of the command.
        num (str): The minimum number of maxed out brawlers.

    Returns:
        None

    """
    requirements.update({"minMaxedBrawlers": num})
    await ctx.reply("Minimum amount of maxed out brawlers set")

@bot.command()
@commands.has_permissions(administrator=True)
async def setmin3v3wins(ctx, num):
    """Set the minimum number of 3v3 wins required.
    
    Args:
        ctx (discord.ext.commands.Context): The context of the command.
        num (str): The minimum number of 3v3 wins.

    Returns:
        None

    """
    requirements.update({"min3v3wins": num})
    await ctx.reply("Minimum amount of 3v3 wins set")

@bot.command()
async def checkplayer(ctx, tag):
    """Check if a player meets the club requirements.
    
    Args:
        ctx (discord.ext.commands.Context): The context of the command.
        tag (str): The player's tag.

    Returns:
        None
    """
    message = check_player(tag)
    await ctx.reply(message)

@bot.command()
async def help(ctx):
    """Display the help message.
    
    Args:
        ctx (discord.ext.commands.Context): The context of the command.

    Returns:
        None

    """
    await ctx.reply("`!setclub <clubtag>` Set the club (sets minimum trophies players need)\n"
                    "`!setminmaxedbrawlers` Set the number of maxed out brawlers players need "
                    "(including 2 gears, a star power, and gadget)\n"
                    "`!setmin3v3wins` Set the number of 3v3 wins players need\n"
                    "`!checkplayer <playertag>` Check if the player meets the club requirements")
bot.run(TOKEN)
