#Test bot made by Camiel when learning python
#Code first, bot.run(token) acts as start

#import things for discord
import discord
import asyncio
from   discord.ext import commands
import sys
import datetime
import string
import urllib
import requests
import subprocess
import random
import json

#load config
with open('config.json', 'r') as f:
    config = json.load(f)

#specify that bot is used for commands and stuff
bot = commands.Bot(command_prefix=config["prefix"], description=config["description"], game=discord.Game(name=config["nowplaying"]))

#gets bot's info
@bot.event
async def on_ready():
    print('Logged in as: {}.'.format(bot.user.name))
    owner = await bot.get_user_info(config["bot_owner_id"])
    print("Owner is: {}".format(owner))
    print("Bot loaded.")

#change prefix
@bot.command(pass_context=True)
async def prefix(ctx, newprefix):
    config["prefix"] = newprefix
    json.dump(config, open('config.json', 'w'), indent=2)
    await ctx.send("Prefix set to: `{}`. New prefix will be applied after restart.".format(newprefix))
    author = ctx.message.author
    print(author, "has changed the prefix to: {}".format(newprefix))

#first command! (says hello)
@bot.command(pass_context=True)
async def hey(ctx):
    await ctx.send("Hello, {}".format(ctx.author.mention))
    author = ctx.message.author
    print(author, "said hey!")

#math
@bot.command()
async def math(ctx, num1, indicator, num2):
    try:   
        int1 = int(num1)
    except:
        await ctx.send(num1, "is not a number!")
        return
    try:   
        int2 = int(num2)
    except:
        await ctx.send(num2, "is not a number!")
        return
    if indicator == "+":
        sumis = int1 + int2
    if indicator == "-":
        sumis = int1 - int2
    if indicator == "/":
        sumis = int1 / int2
    if indicator == "*":
        sumis = int1 * int2
    await ctx.send("The sum is: {}".format(sumis))

#Deletes messages
@bot.command()
async def clear(ctx, messages):
    try:
        totalMess = int(messages)
    except Exception:
        await ctx.send("That's not a number!")
        return
    counter = 0
    while totalMess > 0:
        gotMessage = False
        if totalMess > 100:
            tempNum = 100
        else:
            tempNum = totalMess
        try:
            async for message in ctx.channel.history(limit=tempNum):
                await message.delete()
                gotMessage = True
                counter += 1
                totalMess -= 1
        except Exception:
            pass
        if not gotMessage:
            # No more messages - exit
            break
    await ctx.send("Deleted *{} message(s)!*".format(counter))

#Date & time
print("Bot started on:",datetime.datetime.now().time(),datetime.date.today().strftime('%d-%m-%Y'))

#Tells the date
@bot.command()
async def date(ctx):
    today = datetime.date.today()
    todaysdate = today.strftime('%A, %b %Y (%d-%m-%Y)')
    await ctx.send("Today's date is: {}".format(todaysdate))

#Tells the time
@bot.command()
async def time(ctx):
    await ctx.send("The current time is:",datetime.datetime.now().time())

#changes now playing
@bot.command()
async def nowplaying(ctx, *, playing = None):
    await bot.change_presence(game=discord.Game(name=playing))
    config["nowplaying"] = playing
    json.dump(config, open('config.json', 'w'), indent=2)
    await ctx.send("Now playing has been changed to: Playing **{}**".format(playing))

#Defines a word
@bot.command()
async def define(ctx, *, word : str = None):
        url = "http://api.urbandictionary.com/v0/define?term={}".format(urllib.parse.quote(word))
        r = requests.get(url, headers = {'User-agent': "Camiel's Bot"})
        theJSON = r.json()["list"]
        msg = "I couldn't find a definition for: **{}**".format(word)
        if len(theJSON):
            # Got it - let's build our response
            ourWord = theJSON[0]
            msg = '__**{}:**__\n\n{}'.format(string.capwords(ourWord["word"]), ourWord["definition"])
        await ctx.send(msg)

@bot.command()
async def todo(ctx, *, add : str = None):
    if add is not True:
        with open('todo.txt', 'r') as f:
            todo = f.read().strip()
            await ctx.send(todo)
    if add is True:
        with open('todo.txt', 'r+') as f:
            f.write(todo)

# rewrite
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
        await ctx.send("{}: {}".format(type(error).__name__, error))
        formatted_help = await bot.formatter.format_help_for(ctx, ctx.command)
        for page in formatted_help:
            await ctx.send(page)

#stop
@bot.command(pass_context=True)
async def stop(ctx):
    await ctx.send("Stopping bot...")
    sys.exit(0)

#starts and joins channel
bot.run(config["token"])
