import asyncio

import discord
from discord import Role
from redbot.core import commands
from redbot.core.commands import Context


class Chacall(commands.Cog):
    """My custom cog"""

    dict_role_suppressor: dict[int, int] = {}

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    async def _delete_role(self, role: Role, channel_id: int, message_id: int):
        await asyncio.sleep(10)
        if channel_id in self.dict_role_suppressor and self.dict_role_suppressor[channel_id] == message_id:
            await role.delete()
            del self.dict_role_suppressor[channel_id]

    @commands.command()
    @commands.bot_has_permissions(manage_roles=True)
    async def chacall(self, ctx: Context):
        """This does stuff!"""
        # Your code will go here
        channel = ctx.channel
        id_msg = ctx.message.id
        role_name = f"Chacall-{channel.name}"
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        # Create role if it doesn't exist
        if role is None:
            role = await ctx.guild.create_role(name=role_name)

        for member in channel.members:
            if not member.bot and member.status != discord.Status.offline:
                await member.add_roles(role)
        self.dict_role_suppressor[channel.id] = id_msg
        await ctx.send(f"Pinging {role.mention} for active members!")
        await self._delete_role(role, channel.id, id_msg)
