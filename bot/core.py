# Python 3.8
# discord.py: 1.3.1 
# Author: nyaa-chan
# Version: 1.0.1
import os
import discord
from discord.ext import commands
from PIL import Image
import requests
import random
import yaml
import ImgProcess


with open("..\\config\\config.yml") as config:
    cfg = yaml.load(config, Loader = yaml.SafeLoader)


description = None
TOKEN = cfg["API_config"]["token"]

bot = commands.Bot(command_prefix = '.',)

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
                url = f
                file = requests.get(url, stream = True)
                file.raw.decode_content = True
            except requests.exceptions.MissingSchema:
                await ctx.send('"'+ f + '"' + " isn't a valid url")
                continue

            #open file with PIL
            im = Image.open(file.raw).copy()

            # open dio image an mask and resize it to feched image
            # TODO put DIO on a diet
            DIO = Image.open("diowalk.png").copy().resize(im.size)
            DIOMask = Image.open("diowalkMask.png").convert('L').copy().resize(im.size)
            DIO.putalpha(DIOMask)# apply mask

            tag += random.randrange(10000, 30000)# generate tag from previous tags

            # paste dio onto feched image and save
            im.paste(DIO, (0,0), DIO)
            im.save(str(tag) + ".png", "PNG")
            
            # add file name to myFiles list to be sent to discord an to output list to be deleted later
            myFiles.append(discord.File(str(tag) + ".png"))
            output.append(str(tag) + ".png")
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
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)