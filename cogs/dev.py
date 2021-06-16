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

def is_dev(ctx):
    """Check if user is a developer"""
    return ctx.author.id in config['config']['dev_id']

class Developer(commands.Cog):
    """Developer Cog"""
    def __init__(self, client):
        self.client = client
        self.speedtest_data = ()

    @commands.command(aliases=['exec'], description='__DEVELOPER ONLY__\nExecutes python code.', usage="exec|execute <code>")
    @commands.check(is_dev)
    async def execute(self, ctx, *, code):
        """Executes python code"""
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
    @commands.check(is_dev)
    async def echo(self, ctx, *, msg):
        """Send messages as the bot"""
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command(aliases=['st', 'speed'], description="__DEVELOPER ONLY__\nGet the bot's connection speed.", usage="st|speed|speedtest")
    @commands.check(is_dev)
    async def speedtest(self, ctx):
        """Get the bot's connection speed"""
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
    
    @commands.command(aliases=['gnotes'], description="__DEVELOPER ONLY__\nGet all the notes from the bot's database.", usage='gnotes')
    @commands.check(is_dev)
    async def globalnotes(self, ctx):
        """Get all the notes in the bot's database"""
        gnotes = db.execute("SELECT * FROM notes").fetchall()
        chats = []
        for gnote in gnotes:
            if gnote[1] not in chats:
                chats.append(gnote[1])
        await ctx.send(embed=
                        discord.Embed(
                                title='**Global Notes**',
                                description=f"There is/are a total of **{len(gnotes)}** note(s) across **{len(chats)}** chats",
                                colour=discord.Color.green(),
                            )
                    ) 

    @commands.command(aliases=['poweroff'], description="__DEVELOPER ONLY__\nShut the bot down.", usage="shutdown|poweroff")
    @commands.check(is_dev)
    async def shutdown(self, ctx):
        """Shut the bot down"""
        await ctx.send('Shutting down...')
        await self.client.close()

def setup(client):
    """Cog set up"""
    client.add_cog(Developer(client))
