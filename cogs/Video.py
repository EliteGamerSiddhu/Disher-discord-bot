import discord
from discord.ext import commands
from moviepy.editor import ImageClip, VideoFileClip, CompositeVideoClip
import moviepy.video.fx.all as vfx
from io import BytesIO
from PIL import Image
from random import randint
import os


class Video(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "depressed")
    async def depressed(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        avatar = member.avatar_url_as(size = 256)
        data = BytesIO(await avatar.read())
        p = os.getcwd()
        sad_template = Image.open(p + "/cogs/image_templates/sad_template.png")
        pfp = Image.open(data).resize((512,512)).convert('LA')
        back = Image.new("RGBA", (512,512), (0,0,0,0))
        back.paste(pfp, (0,0))
        back.paste(sad_template, (0,0), mask = sad_template)

        signature = randint(1,50)
        pfp_location = p + f"/cogs/temp_images/pfp_{signature}.png"

        while os.path.exists(pfp_location):
            signature = randint(1,50)
            pfp_location = p + f"/cogs/temp_images/pfp_{signature}.png"

        back.save(pfp_location)
        clip = ImageClip(pfp_location, duration = 14)
        
        signature2 = randint(0,50)
        clip_location = p + f"/cogs/temp_vids/depressed_{signature2}.mp4"

        while os.path.exists(clip_location):
            signature2 = randint(0,50)
            clip_location = p + f"/cogs/temp_vids/depressed_{signature2}.mp4"

        await ctx.send(":video_camera: This can take some time :computer:")

        clip.write_videofile(clip_location, fps = 30,audio = p + "/cogs/audio_clips/sad_violen.mp3")

        await ctx.send(file = discord.File(clip_location))

        if os.path.exists(clip_location):
            os.remove(clip_location)

        if os.path.exists(pfp_location):
            os.remove(pfp_location)

def setup(client):
    client.add_cog(Video(client))