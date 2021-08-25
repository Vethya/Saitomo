"""
Moderator Cog

Commands:
- kick
- ban
- unban
- purge
"""

from discord.ext import commands
import discord
from bot import config
from utils.permissions import check_perm

class Moderator(commands.Cog):
    """Moderator Cog"""
    def __init__(self, client):
        self.client = client

    @commands.command(description='__MODERATOR ONLY__\nKick a user from the server.', usage="kick <user>\nUser argument can be a mention or the user's name itself.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a user from the server"""
        if not ctx.guild:
            await ctx.send('This command can only be used in a server!')
            return
        if await check_perm(ctx, member):
            return
        try:
            await member.kick(reason=reason)
        except commands.errors.MemberNotFound:
            await ctx.send("User not found!")
            return
        await ctx.send(
                    embed=discord.Embed(
                        title='Kicked!',
                        description=f'Admin **{ctx.author.name}** kicked **{member.name}** from the server\nReason: {reason}',
                        colour=discord.Color.red()
                    ),
                    delete_after=0
                )

    @commands.command(description='__MODERATOR ONLY__\nBan a user from the server.', usage="ban <user>\nUser argument can be a mention or the user's name itself.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a user from the server"""
        if not ctx.guild:
            await ctx.send('This command can only be used in a server!')
            return
        if await check_perm(ctx, member):
            return
        try:
            await member.ban(reason=reason)
        except commands.errors.MemberNotFound:
            await ctx.send('User not found!')
            return
        await ctx.send(
                    embed=discord.Embed(
                        title='Banned!',
                        description=f'Admin **{ctx.author.name}** banned **{member.name}** from the server\nReason: {reason}',
                        colour=discord.Color.red()
                    )
                )

    @commands.command(description='__MODERATOR ONLY__\nUnban a banned user.', usage="unban <user>\nUser argument can be a mention or the user's name itself.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user):
        """Unban a banned user"""
        if not ctx.guild:
            await ctx.send('This command can only be used in a server!')
            return
        user = self.client.get_user(int(user))
        banned_users = await ctx.guild.bans()
        if len(banned_users) == 0:
            await ctx.send("There's no banned user in the server")
            return
        try:
            await ctx.guild.unban(user)
        except commands.errors.MemberNotFound:
            await ctx.send(
                        embed=discord.Embed(
                                title='User not found!',
                                description='The user you specified can not be found.',
                                colour=discord.Color.red()
                            )
                    )
            return
        except Exception as e:
            if 'Unknown Ban' in str(e):
                await ctx.send(
                        embed=discord.Embed(
                                title='User is not banned!',
                                description='The user you specified is not banned.',
                                colour=discord.Color.red()
                            )
                    )
                return
        await ctx.send(
            embed=discord.Embed(
                    title='Unbanned!',
                    description=f'Admin **{ctx.author.name}** unbanned **{user.name}**',
                    colour=discord.Color.green()
                )
            )

    @commands.command(description='__MODERATOR ONLY__\nMute a user.', usage="mute <user>\nUser argument can be a mention or the user's name itself.")
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        """Mute a user"""
        if not ctx.guild:
            await ctx.send('This command can only be used in a server!')
            return
        if await check_perm(ctx, member):
            return
        muted = discord.utils.get(ctx.guild.roles, name='Muted')
        if not muted:
            await ctx.send(
                    embed=discord.Embed(
                        title='Muted role not found!',
                        description='Muted role is not found! Make sure to create a Muted role (case sensitive) with appropriate permissions for this command to work.',
                        colour=discord.Color.red()
                    )
                )
            return
        if discord.utils.get(member.roles, name='Muted'):
            await ctx.send(
                    embed=discord.Embed(
                        title='Already Muted!',
                        description='User is already muted.',
                        colour=discord.Color.red()
                    )
                )
            return
        try:
            await member.add_roles(muted, reason=reason)
        except commands.errors.MemberNotFound:
            await ctx.send('User not found!')
            return
        await ctx.send(
                    embed=discord.Embed(
                        title='Muted!',
                        description=f'Admin **{ctx.author.name}** muted **{member.name}**\nReason: {reason}',
                        colour=discord.Color.red()
                    )
                )

    @commands.command(description='__MODERATOR ONLY__\nUnmute a user.', usage="unmute <user>\nUser argument can be a mention or the user's name itself.")
    @commands.has_permissions(ban_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        """Unmute a user"""
        if not ctx.guild:
            await ctx.send('This command can only be used in a server!')
            return
        if await check_perm(ctx, member):
            return
        muted = discord.utils.get(ctx.guild.roles, name='Muted')
        if not muted:
            await ctx.send(
                    embed=discord.Embed(
                        title='Muted role not found!',
                        description='Muted role is not found! Make sure to create a Muted role (case sensitive) with appropriate permissions for this command to work.',
                        colour=discord.Color.red()
                    )
                )
            return
        if not discord.utils.get(member.roles, name='Muted'):
            await ctx.send(
                    embed=discord.Embed(
                        title='Not Muted!',
                        description='User is not muted.',
                        colour=discord.Color.red()
                    )
                )
            return
        try:
            await member.remove_roles(muted, reason=reason)
        except commands.errors.MemberNotFound:
            await ctx.send('User not found!')
            return
        await ctx.send(
                    embed=discord.Embed(
                        title='Unmuted!',
                        description=f'Admin **{ctx.author.name}** unmuted **{member.name}**\nReason: {reason}',
                        colour=discord.Color.red()
                    )
                )

    @commands.command(aliases=['p'], description="__MODERATOR ONLY__\nPurge messages.", usage="p|purge <amount>\nDefault amount is 5")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=5):
        """Purge messages"""
        if not ctx.guild:
            await ctx.send('This command can only be used in a server!')
            return
        await ctx.channel.purge(limit=int(amount)+1)
        await ctx.send(
                    embed=discord.Embed(
                        title='Purge completed!',
                        description=f'Message purged: **{amount}**',
                        colour=discord.Color.green()
                    )
                )

def setup(client):
    """Cog set up"""
    client.add_cog(Moderator(client))

