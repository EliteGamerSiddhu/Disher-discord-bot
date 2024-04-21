import discord
from discord.ext import commands
import json
import os
import typing

def getchannel(message : discord.Message, name : str):
    path = os.getcwd()

    path = path + "/cogs/json files/channel.json"

    with open(path, 'r') as f:
        chanol = json.load(f)

    if str(message.guild.id) in chanol.keys():
        if name in chanol[str(message.guild.id)].keys():
                return chanol[str(message.guild.id)][name]
        else:
            return None
    else:
        return None

def getnumber(message : discord.Message, number : str):
    path = os.getcwd()

    path = path + "/cogs/json files/variables.json"

    with open(path,'r') as f:
        var = json.load(f)

    if str(message.guild.id) in var.keys():
        if number in var[str(message.guild.id)].keys():
            return var[str(message.guild.id)][number]
        else:
            var[str(message.guild.id)][number] = '1'

            with open[path,'w'] as d:
                json.dump(var,d,indent=4)
            
            return 1
    else:
        v = {number : '1'}
        var[str(message.guild.id)] = v

        with open(path,'w') as d:
            json.dump(var,d,indent=4)

        return 1

def increasenumber(message: discord.Message, number : str):
    path = os.getcwd()

    path = path + "/cogs/json files/variables.json"

    with open(path,'r') as f:
        var = json.load(f)

    x = var[str(message.guild.id)][number]
    y = int(x) + 1
    var[str(message.guild.id)][number] = str(y)

    with open(path,'w') as d:
        json.dump(var,d,indent=4)

def setchannel(message: discord.Message, t : str, chanid : str):
    path = os.getcwd()

    path = path + "/cogs/json files/channel.json"

    with open(path,'r') as f:
        chanol = json.load(f)

    if str(message.guild.id) in chanol.keys():
        if t in chanol[str(message.guild.id)].keys():
            chanol[str(message.guild.id)][t] = chanid

            with open(path,'w') as d:
                json.dump(chanol,d,indent=4)
        else:
            chanol[str(message.guild.id)][t] = chanid

            with open(path,'w') as d:
                json.dump(chanol,d,indent=4)
    
    else:
        chanol[str(message.guild.id)] = {t : chanid}

        with open(path,'w') as d:
            json.dump(chanol,d,indent=4)

class Mod(commands.Cog):
    def __init__ (self, client):
        self.client = client

    @commands.command(name = "suggestion", aliases = ['suggest','suggestions'])
    async def suggestion(self, ctx, *, msg : str):
        no = getnumber(ctx, 'suggestion')
        increasenumber(ctx, 'suggestion')
        sug = discord.Embed(title = f"Suggestion#{no}", description = msg, color = discord.Colour.random())
        authname = ctx.author.name
        authid = ctx.author.discriminator
        fullname = authname + "#" + authid
        sug.set_author(name = fullname, icon_url= ctx.author.avatar_url)
        sug.set_footer(text = f"Requested by {ctx.author.name}")
        sug_channel = getchannel(ctx, 'suggestion')
        if sug_channel is None:
            await ctx.send("Set a suggestion channel using the setsuggest command.")
        else:
            await ctx.message.delete()
            xd = await self.client.fetch_channel(sug_channel)
            lol = await xd.send(embed = sug)
            await lol.add_reaction("✅")
            await lol.add_reaction("❌")

    @commands.command(name = "setsuggest", aliases = ['setsuggestchannel','setsuggestionchannel'])
    @commands.has_permissions(manage_channels = True)
    async def setsug(self, ctx, chan : discord.TextChannel):
        setchannel(ctx,'suggestion',chan.id)

        await ctx.send(f"Suggestion channel has been set to {chan}")

    @commands.command(name="setmail")
    @commands.has_permissions(administrator = True)
    async def setmail(self, ctx, chanol : typing.Optional[discord.TextChannel], chan : int):
        if chanol is None and chan is None:
            await ctx.send("Give me a channel or channel id to set")
        else:
            if chanol is None:
                setchannel(ctx, 'mail', chan)
                xd = self.client.fetch_channel(chan)
                await ctx.send(f"Modmail channel successfully set to {xd}")
            else:
                setchannel(ctx, 'mail', chanol.id)
                await ctx.send(f"Modmail channel successfully set to {chanol}")

    @commands.command(name = "modmail", aliases = ['mail'])
    async def mail(self, ctx, message : str):
        chanol = getchannel(ctx, 'mail')
        if chanol is None:
            await ctx.send("Set a modmail channel first using the setmail command.")
        else:
            if message is None:
                await ctx.send("Give me a message to send")
            else:
                mail = discord.Embed(title = "Modmail", description = message, color = discord.Colour.random())
                mail.set_author(name = ctx.author, icon_url= ctx.author.avatar_url)
                mail.set_footer(text = f"Problem reported by {ctx.author.name}")
                mail_chanol = await self.client.fetch_channel(chanol)
                await mail_chanol.send(embed = mail)

def setup(client):
    client.add_cog(Mod(client))