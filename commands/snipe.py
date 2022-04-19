from discord.ext import commands
from discord import embeds
from discord.utils import get
import discord
from datetime import datetime
import typing
import asyncio
from lib import MessageSnipe


class SnipeCommand(commands.Cog):
    """Handles Sniping of deleted messages"""

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.NUM_TO_STORE = 6
        self.snipes = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.guild and not message.author == self.bot.user:
            snipe = MessageSnipe.from_message(message)
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

    @commands.command(aliases=['s', 'shoot', 'fire'])
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def snipe(self, ctx: commands.Context, num_back: typing.Optional[int] = 0, channel: typing.Optional[discord.TextChannel] = None):
        channel_id = channel.id if channel and channel in ctx.guild.text_channels else ctx.channel.id
        if num_back > self.NUM_TO_STORE-1:
            await ctx.send("Nothing to snipe that far back.")
            return
        try:
            current_num = self.snipes[channel_id][0] - num_back
            snipe = self.snipes[channel_id][1][current_num]
            if snipe:
                await ctx.send(embed=snipe.embed)
            else:
                await ctx.send("This snipe has been removed.")
        except KeyError:
            await ctx.send("Nothing to snipe here.")

    @commands.command(aliases=['snipea'])
    @commands.guild_only()
    @commands.cooldown(1, 120, commands.BucketType.guild)
    @commands.has_guild_permissions(administrator=True)
    async def snipeall(self, ctx: commands.Context, maximum: typing.Optional[int] = -1, channel: typing.Optional[discord.TextChannel] = None):
        channel_to_send = channel.id if channel and channel in ctx.guild.text_channels else ctx.channel.id
        counter = 0
        try:
            for snipe in self.snipes[channel_to_send][1].values():
                if snipe:
                    await ctx.send(embed=snipe.embed)
                else:
                    await ctx.send("This snipe has been removed.")
                counter += 1
                if counter == maximum:
                    break
            await ctx.send("That's everything.")
        except KeyError:
            pass

    @commands.command(aliases=['ms'])
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def maxsnipe(self, ctx: commands.Context):
        try:
            result = len(self.snipes[ctx.channel.id][1]) - 1
            await ctx.send(result)
        except KeyError:
            await ctx.send("Nothing yet.")

# region removesnipe
    @commands.command(aliases=["rms", "rmsnipe"])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def removesnipe(self, ctx, num_back: typing.Optional[int] = 0):
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
    async def clearsnipes(self, ctx: commands.Context):
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
    bot.add_cog(SnipeCommand(bot))
