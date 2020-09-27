# Python 3.8
# discord.py: 1.3.1 
# Author: nyaa-chan
# Version: 1.0.1
import os
import discord
from discord.ext import commands
import random
import yaml
import img


with open("config\\config.yml") as config:
    cfg = yaml.load(config, Loader = yaml.SafeLoader)


description = None

bot = commands.Bot(
    command_prefix = cfg["command-config"]["command-prefix"],  
    self_bot = cfg["command-config"]["self-bot"])

# de-bugging command
@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

# TODO fix .help command

@bot.command()
async def bearfacts(ctx, arg):
    # TODO
    pass


@bot.command()# retrieves image from imbedded link and places DIO on it xd
async def diowalk(ctx, *embed):# TODO add support for attachments
    myFiles = []
    output = []
    tag = random.randrange(10000, 30000)# generate initial tag
    try:
        # cycles through all embedded links an processes them
        for f in embed:
            print(f)
  
            # fetch file from url
            try:
                file = img.Fech(f)
            except requests.exceptions.MissingSchema:
                await ctx.send('"'+ f + '"' + " isn't a valid url")
                continue

            print(file)

            
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
            print(myFiles)# print list for de-bug

        # send files to discord
        await ctx.send(files=myFiles)
        await ctx.send("HE APPROACHES")

        # delete output images
        for i in output:
            os.remove(i)
            print("reomved: " + i)

    except discord.errors.HTTPException:
        # catches exception from not embeding an image
        await ctx.send("I need an image idiot")

@bot.command()# logs the bot off for updates to code
async def leave(ctx):
    msg = "later idiots"
    await ctx.send(msg)

    await bot.logout()

@bot.event# says when the bot is logged in
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(input("Paste your API token here: "))