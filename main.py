import discord
from discord.ext import commands
import json
import os

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    if not message.guild:
        return '#'

    if message.guild and  str(message.guild.id) in prefixes.keys():
        return prefixes[str(message.guild.id)]
    else: 
        prefixes[str(message.guild.id)] = '.'

        with open('prefixes.json','w') as f:
            json.dump(prefixes,f,indent=4)

        return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix)

def get_token():
    with open('token.json','r') as f:
        tokens = json.load(f)

    return tokens['token']

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f":arrows_counterclockwise: Loaded {extension}")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f":arrows_clockwise: Unloaded {extension}")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(f":arrows_clockwise: Unloaded {extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f":arrows_counterclockwise: Loaded {extension}")

@client.command(name = "prefix", aliases = ['setprefix', 'set_prefix'])
async def prefix(ctx, prefix):
    with open('prefixes.json','r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json','w') as d:
        json.dump(prefixes,d,indent=4)

    await ctx.send(f"Prefix sucessfully changed to {prefix}")

@client.command()
@commands.is_owner()
async def logout(ctx):
    await client.logout()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(get_token())