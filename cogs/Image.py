from discord.ext import commands
import discord
from io import BytesIO
import random
import os
import asyncio
from pathlib import Path
from PIL import ImageDraw, ImageFilter, ImageFont
import PIL.Image
import typing

def shapecharacter(msg : str, character : int):
    words = msg.split(" ")
    length = 0
    final = ""
    for x in words:
        done = length + len(x)
        if done > character:
            final = final + "\n" + x + " "
            length = len(x)
        else:
            final = final + x + " "
            length = length + len(x) + 1
    return final

class Image(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def wanted(self, ctx, member : typing.Optional[discord.Member] = None, amount : int = 10000):
        if len(str(amount)) > 13:
            await ctx.send("Amount has to be less than 14 characters")
        else:
            if member is None:
                member = ctx.author
            
            p = os.getcwd()
            wanted = Image.open(p + "/cogs/image_templates/wanted_template.jpg")
            avatar = member.avatar_url_as(size = 256)
            data = BytesIO(await avatar.read())

            pfp = PIL.Image.open(data)

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
            file = discord.File(arr, filename = f"{member.name}_wanted.png")
            
            await ctx.send(file = file)

    @commands.command()
    async def jail(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author

        p = os.getcwd()
        jail = PIL.Image.open(p + "/cogs/image_templates/jail_template.png")
        avatar = member.avatar_url_as(size = 256)
        data = BytesIO(await avatar.read())

        pfp = PIL.Image.open(data)

        pfp = pfp.resize((590,590))
        mask = PIL.Image.new("RGBA",(590,590),(0,0,0,0))
        mask.paste(pfp, (0,0))
        mask.paste(jail, (0,0), mask = jail)

        arr = BytesIO()
        mask.save(arr, format = "png")
        arr.seek(0)
        file = discord.File(arr, filename= f"{member.name}_jail.png")

        await ctx.send(file = file)

    @commands.command()
    async def sketch(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        
        avatar = member.avatar_url_as(size = 256)
        data = BytesIO(await avatar.read())

        pfp = PIL.Image.open(data)
        pfp.resize((590,590))
        pfp = pfp.convert("RGB")
        sketch = pfp.filter(ImageFilter.CONTOUR)

        arr = BytesIO()
        sketch.save(arr, format = "png")
        arr.seek(0)
        file = discord.File(arr, filename = f"{member.name}_sketch.png")

        await ctx.send(file = file)

    @commands.command(name = "sad")
    async def sad(self, ctx, member:discord.Member = None):
        if member is None:
            member = ctx.author

        avatar = member.avatar_url_as(size = 256)
        data = BytesIO(await avatar.read())
        pfp = PIL.Image.open(data)

        p = os.getcwd()
        sad_template = PIL.Image.open(p + "/cogs/image_templates/sad_template.png")

        pfp = pfp.resize((512,512)).convert('LA')
        back = PIL.Image.new("RGBA", (512,512), (0,0,0,0))
        back.paste(pfp, (0,0))
        back.paste(sad_template, (0,0), mask = sad_template)

        signature = random.randint(0,50)
        location = p + f"/cogs/temp_images/sad_{signature}.png"

        while os.path.exists(location):
            signature = random.randint(0,50)
            location = p + f"/cogs/temp_images/sad_{signature}.png"

        back.save(location)

        await ctx.send(file = discord.File(location))

        if os.path.exists(location):
            os.remove(location)

    @commands.command()
    async def rip(self, ctx, member:discord.Member = None):
        if member is None:
            member = ctx.author

        avatar = member.avatar_url_as(size = 256)
        data = BytesIO(await avatar.read())
        pfp = PIL.Image.open(data)

        p = os.getcwd()
        rip_template = PIL.Image.open(p + "/cogs/image_templates/rip_template.jpg")

        pfp = pfp.resize((145,145))
        rip_template.paste(pfp, (81,144))

        signature = random.randint(0,50)
        location = p + f"/cogs/temp_images/rip_{signature}.jpg"

        while os.path.exists(location):
            signature = random.randint(0,50)
            location = p + f"/cogs/temp_images/rip_{signature}.jpg"

        rip_template.save(location)

        await ctx.send(file = discord.File(location))

        if os.path.exists(location):
            os.remove(location)

    @commands.command()
    async def cheat(self, ctx, *, say: str = None):
        if say is None:
            await ctx.send("You have to give me something to write on the meme, dumbo.")
        else:
            if len(say) > 39:
                await ctx.send("The text can only be 35 characters long")
            else:
                p = os.getcwd()
                cheat = PIL.Image.open(p + "/cogs/image_templates/cheat_template.jpg")
                cheat_font = ImageFont.truetype(p + "/cogs/Fonts/handwriting.ttf", 26)
                blank = PIL.Image.new('RGBA', (175,110), (0,0,0,0))
                txt = shapecharacter(say, 12)
                d = ImageDraw.Draw(blank)
                d.multiline_text((80,50), txt, fill = (0,0,0), font = cheat_font, anchor = "mm")
                ok = blank.rotate(-24, expand=1)
                cheat.paste(ok, (380,440), mask = ok)
                signature = random.randint(0,50)
                next = p + f"/cogs/temp_images/cheat_{signature}.png"

                while os.path.exists(next):
                    signature = random.randint(0,50)
                    next = p + f"/cogs/temp_images/cheat_{signature}.png"

                cheat.save(next)

                await ctx.send(file = discord.File(next))

                if os.path.exists(next):
                    os.remove(next)

    @commands.command()
    async def worthless(self, ctx, member : typing.Optional[discord.Member] = None, *, say : str = None):
        if member is None and say is None:
            await ctx.send("You have to mention a member or tell me something to write on the meme, dumbo")

        elif member is not None and say is not None:
            if len(say) > 31:
                await ctx.send(f"When you are giving me text with mention, it cannot be longer than 31 characters. You gave me a {len(say)} characters input.")
            else:
                avatar = member.avatar_url_as(size = 256)
                data = BytesIO(await avatar.read())
                pfp = PIL.Image.open(data)
                pfp = pfp.resize((71,71))

                p = os.getcwd()
                template = PIL.Image.open(p + "/cogs/image_templates/worthless_template.jpg")
                d = ImageDraw.Draw(template)
                hand_font = ImageFont.truetype(p + "/cogs/Fonts/handwriting.ttf", 26)

                template.paste(pfp, (173,79))
                d.text((210,180), say, fill = (0,0,0), font = hand_font, anchor = "mm")

                signature = random.randint(0,50)
                location = p + f"/cogs/temp_images/worthless_{signature}.jpg"

                while os.path.exists(location):
                    signature = random.randint(0,50)
                    location = p + f"/cogs/temp_images/worthless_{signature}.jpg"

                template.save(location)

                await ctx.send(file = discord.File(location))

                if os.path.exists(location):
                    os.remove(location) 

        elif member is None:
            if len(say) > 43:
                await ctx.send(f"Sentence cannot be longer than 83 characters. You gave me an iput of {len(say)} characters.")
            else:
                p = os.getcwd()
                template = PIL.Image.open(p + "/cogs/image_templates/worthless_template.jpg")
                d = ImageDraw.Draw(template)
                hand_font = ImageFont.truetype(p + "/cogs/Fonts/handwriting.ttf", 26)
                txt = shapecharacter(say, 20)

                signature = random.randint(0,50)
                location = p + f"/cogs/temp_images/worthless_{signature}.jpg"

                while os.path.exists(location):
                    signature = random.randint(0,50)
                    location = p + f"/cogs/temp_images/worthless_{signature}.jpg"

                d.multiline_text((217,138), txt, fill = (0,0,0), font = hand_font, anchor = "mm")
                template.save(location)

                await ctx.send(file = discord.File(location))

                if os.path.exists(location):
                    os.remove(location)

        else:
            avatar = member.avatar_url_as(size = 256)
            data = BytesIO(await avatar.read())
            pfp = PIL.Image.open(data)
            pfp = pfp.resize((114,114))

            p = os.getcwd()
            template = PIL.Image.open(p + "/cogs/image_templates/worthless_template.jpg")

            signature = random.randint(0,50)
            location = p + f"/cogs/temp_images/worthless_{signature}.jpg"

            while os.path.exists(location):
                signature = random.randint(0,50)
                location = p + f"/cogs/temp_images/worthless_{signature}.jpg"

            template.paste(pfp, (155,88))
            template.save(location)

            await ctx.send(file = discord.File(location))

            if os.path.exists(location):
                os.remove(location)
    
def setup(client):
    client.add_cog(Image(client))