# Work with Python 3.8
import os
import discord
from discord.ext import commands
from PIL import Image
import requests

description = None
TOKEN = 'Njc2OTE5NTc0Njc5MjU3MTU4.XkSMHw.dodadjWeHFEaE9K1x90BrQtT5x4'

#bot = discord.bot()
bot = commands.Bot(command_prefix = '.')

#class Mybot(discord.bot):
"""@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return"""

"""@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)"""

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def diowalk(ctx, *embed):
#if message.content.startswith('>diowalk'):
    myFiles = []
    output = []
    x = 1
    try:

        for f in embed:
            print(f)
            url = f
            file = requests.get(url, stream = True)
            file.raw.decode_content = True

            im = Image.open(file.raw).copy()

            dio = Image.open("diowalk.png").copy().resize(im.size)
            dioMask = Image.open("diowalkMask.png").convert('L').copy().resize(im.size)
            dio.putalpha(dioMask)

            im.paste(dio, (0,0), dio)
            im.save("output" + str(x) + ".png", "PNG")
            myFiles.append(discord.File("output" + str(x) + ".png"))
            output.append("output" + str(x) + ".png")
            print(myFiles)
            x += 1

        await ctx.send(files=myFiles)

        for i in output:
            os.remove(i)
            print("reomved: " + i)

    except AttributeError:
        raise
        await bot.send_message(message.channel, "I need an image idiot")

@bot.command()
async def leave(ctx):
    msg = "later idiots"
    await ctx.send(msg)

    await bot.logout()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#bot = Mybot()

bot.run(TOKEN)