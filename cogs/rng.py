from random import randint
import discord
from discord.ext import commands

class RNG(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "howthot", aliases = ["thotrate","thotpercentage","thot"])
    async def howthot(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        thot = randint(0,100)
        thot = str(thot)

        embed = discord.Embed(title = "Thot rate generator", description = f"{member.name} is {thot}% thot :one_piece_swimsuit:", color = discord.Colour.random())

        await ctx.send(embed = embed)

    @commands.command(name = "howgay", aliases = ['gay','gayrate'])
    async def howgay(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author

        gay = randint(0,100)
        gay = str(gay)

        embed = discord.Embed(title = "Gay rate generator", description = f"{member.name} is {gay}% gay :rainbow_flag:", color = discord.Colour.random())

        await ctx.send(embed = embed)

    @commands.command(name = "pp", aliases = ['penis'])
    async def pp(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author

        r = randint(0,10)
        pp = '8'

        for x in range(r):
            pp = pp + '='

        pp = pp + 'D'

        embed = discord.Embed(title = "Penis generator", description = f"{member.name}\'s pp is \n{pp}", color = discord.Colour.random())

        if r == 0:
            embed.set_footer(text="Microscopic")
        elif r < 6:
            embed.set_footer(text="Normal size")
        else:
            embed.set_footer(text="OMG so long !!")

        await ctx.send(embed = embed)

    @commands.command(name="iq", aliases = ['IQ','iqrate','IQrate'])
    async def iq(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        iq = randint(0,200)
        iq = str(iq)

        embed = discord.Embed(title = "IQ generator", description = f"{member.name} has {iq} iq", color = discord.Colour.random())

        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(RNG(client))