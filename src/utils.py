from time import gmtime, strftime
import discord

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_time():
    raw_time = strftime("%Y/%m/%d %H:%M:%S", gmtime())
    return '[' + raw_time + '] '

def error_embed(title, description):
    return discord.Embed(title = title, colour = 0xff0000, description = ':x: ' + description)

def warning_embed(title, description):
    return discord.Embed(title = title, colour = 0xffff00, description = ':warning: ' + description)