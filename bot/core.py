# Python 3.8
# discord.py: 1.5.0
# Author: nyaa-chan
# Version: 1.0.2
import os
import discord
from discord.ext import commands
import yaml
import img
import random
import requests

# load config files:
with open("config\\config.yml") as config:
    cfg = yaml.load(config, Loader = yaml.SafeLoader)

with open("config\\CommandConfig.yml") as config:
    command_config = yaml.load(config, Loader = yaml.SafeLoader)

# instalize bot with info from the config:
bot = commands.Bot(
    command_prefix = cfg["bot-config"]["command-prefix"],  
    self_bot = cfg["bot-config"]["self-bot"],
)

# Bot commands:

# diowalk command:
@bot.command()
async def diowalk(ctx):
    print("DEBUG: diowalk command invoked")
    return

@bot.listen('on_message')  # retrieves image from imbedded link and places DIO on it xd
async def diowalk_(message):
    if message.content.startswith(cfg["bot-config"]["command-prefix"] + 'diowalk'): # Confirms that the command is being run
        attach = message.attachments
        #converts the contents of the message to a list and removes ".diowalk"
        embed = list(message.content.split(' '))
        embed.remove(str(cfg["bot-config"]["command-prefix"] + 'diowalk'))
        
        try:
            for i in embed:
                await diowalk_funct(message, i)
            for i in attach:
                await diowalk_funct(message, i.url)
        except:
            await message.channel.send("Unknown exception occcured, call Matt")
            raise

# Functions for commands:

# diowalk function:
async def diowalk_funct(message, url):
    # fetch file from url
    myFiles = []
    output = []
    tag = random.randrange(10000, 30000)# generate initial tag

    try:
        file = img.Fech(url)
    except requests.exceptions.MissingSchema:
        await message.channel.send('"'+ url + '"' + " isn't a valid image, if it was an attachment it has been deleted")
        print("WARNING: " + url + " not a valid url")
        return

    print("DEBUG: image at " + str(file))
    
    overlay = "assets\\mask\\diowalk.png"
    mask = "assets\\mask\\diowalkMask.png"
    im = img.Mask(overlay, mask, file)

    # TODO put DIO on a diet

    tag += random.randrange(10000, 30000)# generate tag from previous tags

    fl_name = "assets\\" + str(tag) + ".png"
    im.save(fl_name, "PNG")
    
    # add file name to myFiles list to be sent to discord an to output list to be deleted later
    myFiles.append(discord.File(fl_name))
    output.append(fl_name)
    print("DEBUG: " + str(myFiles))# print list for de-bug

    # send files to discord
    await message.channel.send(files=myFiles)
    # await message.channel.send("HE APPROACHES")

    # delete output images
    for i in output:
        os.remove(i)
        print("DEBUG: reomved " + i)


# Bot login notification:

@bot.event# says when the bot is logged in
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# Token handeling
if cfg["Token-config"]["storeToken"]:
    if cfg["Token-config"]["Token"]  == None: # No saved token.
        # Prompt for token.
        cfg["Token-config"]["Token"] = input("Paste your API token here: ")

        with open("config\\config.yml", "w") as config:
            yaml.dump(cfg, config)

        # If token invalid.
        try:
            bot.run(cfg["Token-config"]["Token"])
        except:
            cfg["Token-config"]["Token"] = None
            with open("config\\config.yml", "w") as config:
                yaml.dump(cfg, config)
            print("Invalid token restart and try again")
    else: # Token is stored.
        # If token invalid.
        try:
            bot.run(cfg["Token-config"]["Token"])
        except:
            cfg["Token-config"]["Token"] = None
            with open("config\\config.yml","w") as config:
                yaml.dump(cfg, config)
            print("Invalid token restart and try again")
else:
    bot.run(input("Paste your API token here: "))