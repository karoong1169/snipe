from discord.ext import commands
from discord import embeds
from discord.utils import get
import discord
from datetime import datetime
import typing
import asyncio
from lib import EditSnipe


class EditSnipeCommand(commands.Cog):
    """Handles sniping of Edited messages"""

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.NUM_TO_STORE = 6
        self.snipes = {}

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.guild:  # only messages in guilds

            before_content = before.clean_content
            after_content = after.clean_content

            if after_content == before_content:  # prevent non content edited messages from being tracked
                return

            snipe = EditSnipe.from_messages(before, after)
            try:
                if self.snipes[snipe.channel_id]:
                    current_num = self.snipes[snipe.channel_id][0]
                    self.snipes[snipe.channel_id][1][current_num + 1] = snipe
                    self.snipes[snipe.channel_id][0] = self.snipes[snipe.channel_id][0] + 1

                    try:  # Remove the one that's more than NUM_TO_STORE back
                        to_remove = self.snipes[snipe.channel_id][0] - self.NUM_TO_STORE if self.snipes[snipe.channel_id][0] > self.NUM_TO_STORE else None
                        if to_remove:
                            del self.snipes[snipe.channel_id][1][to_remove]
                    except KeyError:
                        pass
            except KeyError:
                self.snipes[snipe.channel_id] = [1, {1: snipe}]

    @commands.command(aliases=['esnipe', 'es'])
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def editsnipe(self, ctx: commands.Context, num_back: typing.Optional[int] = 0):
        if num_back > self.NUM_TO_STORE-1:
            await ctx.send("Nothing to snipe that far back.")
            return
        try:
            current_num = self.snipes[ctx.channel.id][0] - num_back
            snipe = self.snipes[ctx.channel.id][1][current_num]
            if snipe:
                await ctx.send(embed=snipe.embed)
            else:
                await ctx.send("This edit snipe has been removed.")
        except KeyError:
            await ctx.send("Nothing to snipe here.")

    @commands.command(aliases=['me'])
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def maxedit(self, ctx: commands.Context):
        try:
            result = len(self.snipes[ctx.channel.id][1]) - 1
            await ctx.send(result)
        except KeyError:
            await ctx.send("Nothing yet.")

# region Remove edit
    @commands.command(aliases=["rme", "rmesnipe"])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def removeedit(self, ctx, num_back: typing.Optional[int]):
        if self.check_should_remove_mine(ctx):
            if num_back > self.NUM_TO_STORE-1:
                await ctx.send("My history doesn't go that far back.")
                return
            try:
                current_num = self.snipes[ctx.channel.id][0] - num_back
                self.snipes[ctx.channel.id][1][current_num] = None
                await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
            except KeyError:
                pass
        else:
            await ctx.send("You ain't really expect that to work here, did you?")

    def check_should_remove_mine(self, ctx: commands.Context) -> bool:
        if ctx.guild.id == 683724561505845255:
            if not ctx.author.id == self.bot.owner_id:
                return False
            else:
                return True
        else:
            return True
# endregion

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.channel)
    @commands.has_permissions(manage_messages=True)
    async def clearedits(self, ctx: commands.Context):
        channel_id = ctx.channel.id
        try:
            await ctx.send("Are you sure about that? Say yes to confirm.")
            msg = await self.bot.wait_for("message", check=lambda msg: msg.author.id == ctx.author.id, timeout=20.0)
            if "yes" in msg.content.lower():
                del self.snipes[channel_id]
                await ctx.send("Done.")
            else:
                await ctx.send("Cancelled.")
        except asyncio.TimeoutError:
            await ctx.send("Never mind then.")


def setup(bot):
    bot.add_cog(EditSnipeCommand(bot))
