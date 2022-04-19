from discord.ext import commands
from discord import embeds
from discord.utils import get
import discord
import datetime
import typing


class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(aliases=["ui", "useri", "whois", "wi"])
    @commands.guild_only()
    async def userinfo(self, ctx: commands.Context, member: typing.Optional[discord.Member]):
        member = member or ctx.author
        member = await ctx.guild.fetch_member(member.id)  # fetch to make sure we get the most up to date pfp

        roles = [role for role in member.roles]
        roles_text = "".join([f'{role.mention}  ' for role in roles if role.name != "@everyone"]) if len("".join([f'{role.mention} ' for role in roles if role.name != "@everyone"])) < 800 else "Too many roles to show."

        embed = discord.Embed(color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())

        embed.set_author(name=f"{member} User Info")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.add_field(name="ID:", value=member.id, inline=False),
        embed.add_field(name="Member Name:", value=member.display_name, inline=False)
        embed.add_field(name="Created At:", value=member.created_at.strftime("%B %d %Y at %I:%M %p UTC"), inline=False)
        embed.add_field(name="Joined At:", value=member.joined_at.strftime("%B %d %Y at %I:%M %p UTC"), inline=False)
        embed.add_field(name=f"Roles: (69 Nice)" if len(roles)-1 == 69 else f"Roles: ({len(roles) - 1})", value=roles_text if len(roles) > 1 else "Just the standard role", inline=False)
        embed.add_field(name="Top Role:", value="".join(member.top_role.mention) if (len(roles) > 1) else "Doesn't have any..", inline=False)
        embed.add_field(name="Bot?", value="Yes" if member.bot else "No", inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(UserInfo(bot))
