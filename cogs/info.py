"""
Information Cog

Commands:
- ping
- alive
"""

from os import name
import time
from datetime import datetime, timedelta
import discord
from discord import colour
from discord.embeds import Embed, EmptyEmbed
from discord.ext import commands
from discord.utils import valid_icon_size
from utils.parser import parse_date
from bot import config, runtime

class Information(commands.Cog):
    """Information Cog"""
    def __init__(self, client):
        self.client = client

    @commands.command(description="Get the bot's ping.", usage="ping")
    async def ping(self, ctx):
        """Get the bot's ping"""
        start = time.time()
        msg = await ctx.send(embed=
                    discord.Embed(
                            title="**Pong!**",
                            colour=discord.Color.green(),
                            description="Pinging..."
                        )
                )
        end = time.time()
        between = int((end - start)*1000)
        await msg.edit(embed=
                    discord.Embed(
                            title="**Pong!**",
                            colour=discord.Color.green(),
                            description=f"*{between} ms*"
                        )
                )

    @commands.command(description="Check if the bot is alive with some additional informations.", usage="alive")
    async def alive(self, ctx):
        """Check if the bot is alive with some additional informations"""
        now = datetime.now()
        delta = now - runtime
        time = str(timedelta(seconds=delta.seconds)).split(":")
        days = "" if delta.days == 0 else str(delta.days) + " days, "
        hours = "" if time[0] == "0" else time[0] + " hours, "
        minutes = "" if time[1] == "00" else time[1] + " minutes and "
        await ctx.send(embed=discord.Embed(
                        title="**Bot is alive!**\n",
                        colour=discord.Color.green(),
                        description="Python version: *3.9.0*\n"+
                                    "discord.py version: *1.0.1*\n"+
                                    "Repository: https://github.com/Vethya/Saitomo\n"+
                                    f"Uptime: **{days}{hours}{minutes}{time[2]} seconds**"
                    )
            )

    @commands.command(description="Get information on the current server.", usage="server")
    async def server(self, ctx):
        """Get information on the current server"""
        if not ctx.guild:
            await ctx.send('This command can only be used in a server!')
            return
        embed = discord.Embed(title="Server Information", colour=discord.Color.green())

        if ctx.guild.icon_url:
            embed.set_thumbnail(url=ctx.guild.icon_url)
        created_at = ctx.guild.created_at

        embed.add_field(name="Name", value=ctx.guild.name, inline=True)
        embed.add_field(name="ID", value=ctx.guild.id, inline=True)
        embed.add_field(name="Member Count", value=ctx.guild.member_count, inline=True)
        embed.add_field(name="Owner", value=ctx.guild.owner)
        embed.add_field(name="Region", value=str(ctx.guild.region).title(), inline=True)
        embed.add_field(name="Max Members", value=ctx.guild.max_members, inline=True)
        embed.add_field(name="Created At", value=parse_date(created_at), inline=True)

        await ctx.send(embed=embed)

    @commands.command(description="Get information on the current or given user.", usage="user <user>")
    async def user(self, ctx, user: discord.Member=None):
        """Get information on the current or given user"""
        if not ctx.guild:
            await ctx.send('This command can only be used in a server!')
            return
        
        user = user if user else ctx.author
        embed = discord.Embed(title="User Information", colour=discord.Color.green())

        embed.set_thumbnail(url=user.avatar_url)
        roles = []
        if len(user.roles) > 1:
            for role in user.roles:
                if role.id != ctx.guild.default_role.id:
                    roles.append(f"<@&{role.id}>")
            roles = ", ".join(roles)
        else:
            roles = None

        embed.add_field(name="Name", value=user, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Created At", value=parse_date(user.created_at), inline=True)
        embed.add_field(name="Roles", value=roles, inline=True)

        await ctx.send(embed=embed)


def setup(client):
    """Cog set up"""
    client.add_cog(Information(client))