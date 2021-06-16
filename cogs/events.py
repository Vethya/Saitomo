"""
Events Cog

Events:
- on ready
- on_command_error
"""

import logging
import discord
from discord.ext import commands
from discord.ext.commands import errors

class Events(commands.Cog):
    """Events Cog"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        """Runs when the bot is ready"""
        await self.client.change_presence(activity=discord.Game('.help'))
        logging.info("Bot is ready!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Error handler"""
        if isinstance(error, errors.MissingRequiredArgument):
            await ctx.send(embed=
                        discord.Embed(
                                title="**Error**",
                                colour=discord.Color.red(),
                                description=f"Missing required argument! Please refer to this command's usage information with .help {ctx.command}."
                            )
                    )
        elif isinstance(error, errors.MemberNotFound):
            await ctx.send(embed=
                        discord.Embed(
                                title="**Error**",
                                colour=discord.Color.red(),
                                description=f"Member not found! Please specify a valid member argument, refer to .help {ctx.command} for more information on it."
                            )
                    )
        elif isinstance(error, errors.MissingPermissions):
            await ctx.send(embed=
                        discord.Embed(
                                title="**Error**",
                                colour=discord.Color.red(),
                                description="Insufficient permission! You don't have enough permissions to run this command."
                            )
                    )
        elif isinstance(error, errors.CommandNotFound):
            await ctx.send(embed=
                        discord.Embed(
                                title="**Error**",
                                colour=discord.Color.red(),
                                description="Command not found! There is no command with this name."
                            )
                    )
        # https://github.com/AlexFlipnote/discord_bot.py/blob/f7d1107b4514706d85125b643bf471fb7580f013/cogs/events.py#L26
        elif "2000 or fewer" in str(error) and len(ctx.message.clean_content) > 1900:
            await ctx.send(embed=
                        discord.Embed(
                                title="**Error**",
                                colour=discord.Color.red(),
                                description="Character Limit Reached! The following command tried to display more than 2000 characters."
                            )
                    )
        else:
            await ctx.send(f"`{error}`")

def setup(client):
    """Cog set up"""
    client.add_cog(Events(client))
