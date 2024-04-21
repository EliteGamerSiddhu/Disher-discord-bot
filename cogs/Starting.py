import discord
from discord.ext import commands
import discord.utils

class Starting(commands.Cog):
    def __init__ (self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot logged in as {self.client.user}")
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        general = discord.utils.find(lambda x: x.name == 'general' or x.name == 'lounge',  guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            await general.send('Hello {}!'.format(guild.name))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong!! {self.client.latency}")

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title = "Invite me to your server !!", description = 'Click [here](https://discord.com/api/oauth2/authorize?client_id=806402225026105378&permissions=8&scope=bot)', color = discord.Colour.random())
        embed.set_footer(text = f"Requested by {ctx.author.name}", icon_url= ctx.author.avatar_url)
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Starting(client))