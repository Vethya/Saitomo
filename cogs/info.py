"""
Information Cog

Commands:
- ping
- alive
- is special
"""

import time
from datetime import datetime, timedelta
import discord
from discord.ext import commands
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
        time = str(timedelta(seconds=delta.seconds)).split    (":")
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
    @commands.command(description="Check if a server is one of the special servers.", usage="isspecial")
    async def isspecial(self, ctx):
        """Check if a server is one of the special servers"""
        if ctx.guild.id in config['config']['special_servers']:
            await ctx.send(embed=discord.Embed(
                                title='**Yes!**',
                                description="Your server is in my special servers list!",
                                colour=discord.Color.green()
                            )
                        )
        else:
            await ctx.send(embed=discord.Embed(
                                title='**No!**',
                                description="Your server isn't in my special servers list!",
                                colour=discord.Color.red()
                            )
                        )
def setup(client):
    """Cog set up"""
    client.add_cog(Information(client))

