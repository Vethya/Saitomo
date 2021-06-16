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
        if member == ctx.guild.owner:
            await ctx.send("You can't kick the owner of the server!")
            return
        if member == ctx.me:
            await ctx.send("Don't make me kick myself it's tragic.")
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
        if member == ctx.guild.owner:
            await ctx.send("You can't ban the owner of the server!")
            return
        if member == ctx.me:
            await ctx.send("Don't make me ban myself it's tragic.")
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
    async def unban(self, ctx, *, member: discord.Member):
        """Unban a banned user"""
        if not ctx.guild:
            await ctx.send('This command can only be used in a server!')
            return
        banned_users = await ctx.guild.bans()
        if len(banned_users) == 0:
            await ctx.send("There's no banned user in the server")
            return
        member_name, member_discriminator = member.split('#')
        for bans in banned_users:
            user = bans.user
            if (user.name, user.discriminator) != (member_name, member_discriminator):
                await ctx.send('User is not banned!')
            else:
                try:
                    await ctx.guild.unban(user)
                except commands.errors.MemberNotFound:
                    await ctx.send('User not found!')
                    return
                await ctx.send(
                        embed=discord.Embed(
                            title='Unbanned!',
                            description=f'Admin **{ctx.author.name}** unbanned **{member_name}**',
                            colour=discord.Color.green()
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

