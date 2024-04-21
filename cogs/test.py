import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import typing
import os

class test(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def ok(self, ctx, member : typing.Optional[discord.Member] = None, amount : int = 10000):
        if len(str(amount)) > 13:
            await ctx.send("Amount has to be less than 14 characters")
        else:
            if member is None:
                member = ctx.author
            
            p = os.getcwd()
            wanted = Image.open(p + "/cogs/image_templates/wanted_template.jpg")
            avatar = member.avatar_url_as(size = 256)
            data = BytesIO(await avatar.read())

            pfp = Image.open(data)

            pfp = pfp.resize((317,317))

            wanted.paste(pfp, (92,152))
            drawable = ImageDraw.Draw(wanted)
            wanted_font = ImageFont.truetype(p + "/cogs/Fonts/wanted.ttf", 60)
            comma = "{:,}".format(amount)
            text = "$" + comma
            drawable.text((248,546), text, fill = (0,0,0), font = wanted_font,anchor= "mm")

            arr = BytesIO()
            wanted.save(arr, format = "png")
            arr.seek(0)
            file = discord.File(arr, filename = 'test.png')
            
            await ctx.send(file = file)

def setup(client):
    client.add_cog(test(client))