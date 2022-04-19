from discord.ext import commands
import discord
from PIL import Image, ImageDraw
import io
import aiohttp
import functools


class Aim(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    def generate_image(self, bytes: io.BytesIO) -> io.BytesIO:
        start_image: Image = Image.open(fp=bytes)

        if start_image.mode != "RGB" or start_image.mode != "RGBA":
            start_image = start_image.convert("RGBA")

        middlex = start_image.width/2
        middley = start_image.width/2
        midpoint = (middlex, middley)
        height = start_image.height
        width = start_image.width

        red = (255, 0, 0)  # (r, g, b)

        line_width = width // 30  # 128//30 = 4
        circle_radius = int(line_width*1.5)
        rect_offset = (circle_radius + line_width) * 2

        left_rect_bounds = [(0, middley-line_width), (middlex-rect_offset, middley+line_width)]
        top_rect_bounds = [(middlex-line_width, 0), (middlex+line_width, middley-rect_offset)]
        right_rect_bounds = [(middlex+rect_offset, middley-line_width), (width, middley+line_width)]
        bottom_rect_bounds = [(middlex-line_width, middley+rect_offset), (middlex+line_width, height)]
        circle_bounds = [(middlex-circle_radius, middley-circle_radius), (middlex+circle_radius, middley+circle_radius)]

        draw_obj = ImageDraw.Draw(start_image)
        draw_obj.ellipse(circle_bounds, red)
        draw_obj.rectangle(left_rect_bounds, red)
        draw_obj.rectangle(top_rect_bounds, red)
        draw_obj.rectangle(right_rect_bounds, red)
        draw_obj.rectangle(bottom_rect_bounds, red)

        buffered_image = io.BytesIO()
        start_image.save(buffered_image, "PNG")
        buffered_image.seek(0)

        return buffered_image

    async def get_user_pfp_bytes(self, user: discord.User) -> bytes:
        identifier = user.id
        user = await self.bot.fetch_user(identifier)
        start_url = str(user.avatar_url)  # avatar_url is an Asset, if you want to construct the url yourself you'd have to format it as f"{Asset.base}{Asset.url}"

        # Use aiohttp to not block
        async with aiohttp.ClientSession() as session:  # Start a session
            async with session.get(start_url) as response:  # Get a url
                av_bytesIO = io.BytesIO(await response.read())  # Read the raw response bytes into a buffer
                av_bytesIO.seek(0)  # Seek the buffer to the start
        return av_bytesIO

    @commands.command(aliases=['a'])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def aim(self, ctx: commands.Context, member: discord.User = None):
        if not member:
            try:
                channel_id = ctx.channel.id
                snipes = self.bot.get_cog("SnipeCommand")
                index = snipes.snipes[channel_id][0]
                snipe = snipes.snipes[channel_id][1][index]
                pfp_bytes = await self.get_user_pfp_bytes(snipe.user)
                to_run = functools.partial(self.generate_image, pfp_bytes)
                image: io.BytesIO = await self.bot.loop.run_in_executor(None, to_run)
                await ctx.send(file=discord.File(image, "snipe.png"))
            except KeyError:
                await ctx.send("There's nothing to snipe in this channel")
        else:
            pfp_bytes = await self.get_user_pfp_bytes(member)
            to_run = functools.partial(self.generate_image, pfp_bytes)
            image: io.BytesIO = await self.bot.loop.run_in_executor(None, to_run)
            await ctx.send(file=discord.File(image, "snipe.png"))


def setup(bot):
    bot.add_cog(Aim(bot))
