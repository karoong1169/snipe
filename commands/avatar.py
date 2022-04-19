from discord.ext import commands
from discord import embeds
from discord.utils import get
import discord
import typing


class AvatarCmd(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(aliases=['av'])
    @commands.guild_only()
    async def avatar(self, ctx: commands.Context, member: typing.Optional[discord.Member]):
        member = member or ctx.author

        embed = embeds.Embed()
        embed.set_author(name="{member} Avatar")

        member = await self.bot.fetch_user(member.id)  # Fetch member to get most up to date pfp

        embed.set_image(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AvatarCmd(bot))
