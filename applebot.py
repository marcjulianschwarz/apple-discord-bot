# applebot.py
import os
import aiohttp
import apple_loader
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime

description = 'Shows news from Apple Newsroom'

# Get hidden token and guild
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))

# Channel ids:
apple_newsroom = 791369425332207636
member_id = 792386416679321600

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', description=description, intents=intents)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    msg1.start()  # Loop for apple newsroom site
    server_stats.start()  # Loop for server stats
    member_roles.start()  # Loop for member roles based on days joined


# Apple Newsroom loop
@tasks.loop(seconds=10)
async def msg1():
    file = open("data.txt", "r")
    current = file.read()
    file.close()

    new = await apple_loader.save()

    if(new != current):
        channel = bot.get_channel(apple_newsroom)
        await channel.send("@everyone\n" + new)

    current = new


@tasks.loop(hours=24)
async def member_roles():

    guild = bot.get_guild(GUILD_ID)
    members = get_members()
    members.sort(key=get_joined_at)
    for member in members:
        days_on_server = (datetime.now() - member.joined_at).days
        print(member.name + " ist seit " + str(days_on_server) + " Tagen auf dem Server.")
        if(days_on_server > 30):
            await member.add_roles(guild.get_role(793083246480326697))


# bot commands
@bot.command()
async def news(ctx):
    if is_bot_channel(ctx):
        news = await apple_loader.save()
        await ctx.send(news)
    else:
        await delete(ctx)


# server stats
@tasks.loop(seconds=10)
async def server_stats():
    channel = bot.get_channel(member_id)
    await channel.edit(name="Mitglieder: " + str(len(get_members())))


def get_members():
    guild = bot.get_guild(GUILD_ID)
    return guild.members


# commands for testing
@bot.command()
async def test(ctx, arg="What?"):
    if is_bot_channel(ctx):
        await ctx.send(arg)
    else:
        await delete(ctx)


@bot.command()
async def channels(ctx):
    channels = bot.get_all_channels()
    for channel in channels:
        print(channel.name + " " + str(channel.id))


# helper functions
def is_bot_channel(ctx):
    return (ctx.message.channel.name == "🤖bot-commands")


async def delete(ctx):
    await ctx.message.delete()
    await ctx.send("Bitte Commands nur im 'bot-commands' Kanal verwenden. Danke :)")


def get_joined_at(member):
    return member.joined_at


bot.run(TOKEN)
