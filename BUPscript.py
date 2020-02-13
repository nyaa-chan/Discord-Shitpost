# Work with Python 3.8
# discord.py 1.3.1 
# Author: nyaa-chan
import os
import discord
from discord.ext import commands
from PIL import Image
import requests

description = None
TOKEN = 'Njc2OTE5NTc0Njc5MjU3MTU4.XkSXdA.Xqfggkry1sG10nLYrft2wVNxPeE'

bot = commands.Bot(command_prefix = '.')

# de-bugging command
@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


@bot.command()# retrieves image from imbedded link and places DIO on it xd
async def diowalk(ctx, *embed):
    myFiles = []
    output = []
    x = 1
    try:

        for f in embed:
            print(f)
            
            try:
                url = f
                file = requests.get(url, stream = True)
                file.raw.decode_content = True
            except requests.exceptions.MissingSchema:
                await ctx.send('"'+ f + '"' + " isn't a valid url")
                continue

            im = Image.open(file.raw).copy()

            DIO = Image.open("diowalk.png").copy().resize(im.size)
            DIOMask = Image.open("diowalkMask.png").convert('L').copy().resize(im.size)
            DIO.putalpha(DIOMask)

            im.paste(DIO, (0,0), DIO)
            im.save("output" + str(x) + ".png", "PNG")
            myFiles.append(discord.File("output" + str(x) + ".png"))
            output.append("output" + str(x) + ".png")
            print(myFiles)
            x += 1

        await ctx.send(files=myFiles)
        await ctx.send("HE APPROACHES")

        for i in output:
            os.remove(i)
            print("reomved: " + i)

    except discord.errors.HTTPException:
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