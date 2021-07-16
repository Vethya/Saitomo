"""
Developer Cog

Commands:
- execute
- echo
- speedtest
- globalnotes
- shutdown
"""

import discord
from discord.ext import commands
from bot import config, db
import speedtest

class Developer(commands.Cog):
    """Developer Cog"""
    def __init__(self, client):
        self.client = client
        self.speedtest_data = ()

    @commands.command(aliases=['exec'], description='__DEVELOPER ONLY__\nExecutes python code.', usage="exec|execute <code>")
    async def execute(self, ctx, *, code):
        """Executes python code"""
        if ctx.author.id not in config['config']['dev_id']:
            await ctx.send(embed=
                    discord.Embed(
                            title='No!',
                            description=f"Only my developers can use this command.",
                            colour=discord.Color.red(),
                        )
                )
            return
        exec(
            'async def __ex(self, ctx):' +
            ''.join([f'\n {l}' for l in code.split('\n')])
        )
        output = await locals()['__ex'](self, ctx)
        end = '\n`' + str(output) + '`' if output is not None else '\nNone'
        await ctx.send(
                '**INPUT**\n'+
                f'`{code}`\n'+
                '**OUTPUT**'+
                f'{end}'
                )

    @commands.command(description='__DEVELOPER ONLY__\nSend messages as the bot.', usage="echo <text>")
    async def echo(self, ctx, *, msg):
        """Send messages as the bot"""
        if ctx.author.id not in config['config']['dev_id']:
            await ctx.send(embed=
                    discord.Embed(
                            title='No!',
                            description=f"Only my developers can use this command.",
                            colour=discord.Color.red(),
                        )
                )
            return
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command(aliases=['st', 'speed'], description="__DEVELOPER ONLY__\nGet the bot's connection speed.", usage="st|speed|speedtest")
    async def speedtest(self, ctx):
        """Get the bot's connection speed"""
        if ctx.author.id not in config['config']['dev_id']:
            await ctx.send(embed=
                    discord.Embed(
                            title='No!',
                            description=f"Only my developers can use this command.",
                            colour=discord.Color.red(),
                        )
                )
            return
        mode = await ctx.send(
                    embed=discord.Embed(
                            title='**Speedtest**',
                            colour=discord.Color.blue(),
                            description='Please choose a speedtest mode:\n1. Text\n2. Image'
                        )
                )
        self.speedtest_data = (ctx.author.id, mode.id)
        await mode.add_reaction('1️⃣')
        await mode.add_reaction('2️⃣')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Reaction handler for speedtest"""
        if (user.id, reaction.message.id) != self.speedtest_data:
            return
        await reaction.message.clear_reactions()
        await reaction.message.edit(
                    embed=discord.Embed(
                            title='**Speedtest**',
                            colour=discord.Color.blue(),
                            description='Testing...'
                        )
                )
        speed = speedtest.Speedtest()
        speed.get_best_server()
        speed.upload()
        speed.download()
        if reaction.emoji == '1️⃣':
            result = speed.results.dict()
            await reaction.message.edit(
                        embed=discord.Embed(
                                title='**Speedtest**',
                                colour=discord.Color.blue(),
                                description=f"Ping: {result['ping']}\nUpload: {round(result['upload'] / 1048576, 2)} mbps\nDownload: {round(result['download'] / 1048576, 2)} mbps"
                            )
                    )
        if reaction.emoji == '2️⃣':
            result = speed.results.share()
            await reaction.message.edit(
                        embed=discord.Embed(
                                title='**Speedtest Result**',
                                colour=discord.Color.blue(),
                                image=result
                            )
                    )
 
    @commands.command(aliases=['poweroff'], description="__DEVELOPER ONLY__\nShut the bot down.", usage="shutdown|poweroff")
    async def shutdown(self, ctx):
        """Shut the bot down"""
        if ctx.author.id not in config['config']['dev_id']:
            await ctx.send(embed=
                    discord.Embed(
                            title='No!',
                            description=f"Only my developers can use this command.",
                            colour=discord.Color.red(),
                        )
                )
            return
        await ctx.send('Shutting down...')
        await self.client.close()

def setup(client):
    """Cog set up"""
    client.add_cog(Developer(client))
