# KappehNet version 1.0 Alpha
# Made by Kappeh

import os
import sys
import discord
from discord.ext import commands
from discord.ext.commands import Bot

VERSION = "1.0 Alpha"
TOKEN = os.environ.get('DISCORD_TOKEN')

if not TOKEN:
    try:
        from Credentials import TOKEN
    except ModuleNotFoundError:
        if len(sys.argv) > 1:
            TOKEN = sys.argv[1]
        else:
            raise Exception('Specify discord token either with a credentials.py file or as an argument.')

bot = commands.Bot(command_prefix = '//')

async def on_ready():
    print("KappehNet version " + VERSION + " is now running")

@bot.command(brief = "Replies with Pong.")
async def ping():
    await bot.say(":ping_pong: Pong!! xSSS")

bot.run(TOKEN)