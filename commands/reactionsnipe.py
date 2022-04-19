from discord.ext import commands
from discord import embeds
from discord.utils import get
import discord
from datetime import datetime
import typing
import asyncio
from lib import ReactionSnipe


class ReactionSnipeCommand(commands.Cog):
    """Handles sniping of removed reactions"""

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.NUM_TO_STORE = 6
        self.snipes = {}

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.guild_id:
            if payload.event_type == "REACTION_REMOVE":
                user = self.bot.get_user(payload.user_id)
                snipe = ReactionSnipe.from_reaction_remove(user, payload)
                try:
                    if self.snipes[snipe.channel_id]:
                        current_num = self.snipes[snipe.channel_id][0]
                        self.snipes[snipe.channel_id][1][current_num + 1] = snipe
                        self.snipes[snipe.channel_id][0] = self.snipes[snipe.channel_id][0] + 1

                        try:
                            to_remove = self.snipes[snipe.channel_id][0] - self.NUM_TO_STORE if self.snipes[snipe.channel_id][0] > self.NUM_TO_STORE else None
                            if to_remove:
                                del self.snipes[snipe.channel_id][1][to_remove]
                        except KeyError:
                            pass
                except KeyError:
                    self.snipes[snipe.channel_id] = [1, {1: snipe}]

    @commands.command(aliases=['rs', 'reactsnipe', 'rsnipe'])
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def reactionsnipe(self, ctx: commands.Context, num_back: typing.Optional[int]):
        if num_back:
            if num_back > self.NUM_TO_STORE-1:
                await ctx.send("Nothing to snipe that far back.")
                return
            try:
                current_num = self.snipes[ctx.channel.id][0] - num_back
                snipe = self.snipes[ctx.channel.id][1][current_num]
                await ctx.send(embed=snipe.embed)
            except KeyError:
                await ctx.send("Nothing to snipe here.")
        else:
            try:
                current_num = self.snipes[ctx.channel.id][0]
                snipe = self.snipes[ctx.channel.id][1][current_num]
                await ctx.send(embed=snipe.embed)
            except KeyError:
                await ctx.send("Nothing to snipe here.")

    @commands.command(aliases=['mr'])
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def maxreact(self, ctx: commands.Context):
        try:
            result = len(self.snipes[ctx.channel.id][1]) - 1
            await ctx.send(result)
        except KeyError:
            await ctx.send("Nothing yet.")

# region removesnipe
    @commands.command(aliases=["rmr", "rmreact", "rmreaction"])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def removereaction(self, ctx, num_back: typing.Optional[int]):
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
    async def clearreactions(self, ctx: commands.Context):
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
    bot.add_cog(ReactionSnipeCommand(bot))
