"""
Misc Cog

Commands:
- urban dictionary
- wikipedia
- get help
"""

import json
from urllib.parse import quote as urlencode
import discord
from discord.ext import commands
import aiohttp
import wikipedia
from bot import prefix

class Misc(commands.Cog):
    """Misc Cog"""
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ud'], description="Get a definition of the query using the Urban Dictionary.", usage="ud|urbandictionary <index> <query>")
    async def urbandictionary(self, ctx, defamount, *, word):
        """Get a definition of the query using the Urban Dictionary"""
        url = f'https://api.urbandictionary.com/v0/define?term={urlencode(word)}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as raw_resp:
                resp = await raw_resp.text()
                rcode = raw_resp.status
        if rcode != 200:
            await ctx.send('Word not found!')
            return
        definitions = json.loads(resp)['list']
        try:
            definition = definitions[int(defamount)]
        except IndexError:
            await ctx.send('Not enough definitions')
            return
        text = f'**Definition:**\n{definition["definition"]}\n'
        text += f'**Examples:**\n{definition["example"]}'
        await ctx.send(embed=
                    discord.Embed(
                            title=f"**{definition['word']}**",
                            description=text,
                            colour=discord.Color.orange()
                        )
                )

    @commands.command(aliases=['wiki'], description="Get information for the query from wikipedia.", usage="wiki|wikipedia <query>")
    async def wikipedia(self, ctx, query):
        """Get information for the query from wikipedia"""
        msg = await ctx.send(embed=
                    discord.Embed(
                            title="**Wikipedia**",
                            description="Getting wikipedia info...",
                            colour=discord.Color.orange()
                        )
                )
        try:
            search = wikipedia.page(query)
            title = search.title
            content = wikipedia.summary(query)
            if len(content) > 2000:
                await msg.edit(embed=
                            discord.Embed(
                                    title="**{title}**",
                                    description=str(content[:1500]),
                                    colour=discord.Color.orange()
                                )
                        )
            await msg.edit(embed=
                        discord.Embed(
                                title=f"**{title}**",
                                description=content,
                                colour=discord.Color.orange()
                            )
                    )
        except wikipedia.exceptions.DisambiguationError as dis:
            dis_option = ''
            for option in dis.options:
                dis_option += f'**{option}**\n'
            await msg.edit(embed=
                        discord.Embed(
                            title=f"**{query}** may refer to:",
                            description=dis_option,
                            colour=discord.Color.orange()
                        )
                    )

    @commands.command(aliases=['h', 'help'], description="Get information on how to use the bot.", usage="h|help|gethelp <command>\nDon't specify the command to get the list of commands")
    async def gethelp(self, ctx, cmd=''):
        """Get information on how to use the bot"""
        command = self.client.get_command(cmd)
        if ctx.guild and cmd != '':
            await ctx.send(
                        embed=discord.Embed(
                                title='Command not available!',
                                description="This command can only be use in a DM!",
                                colour=discord.Color.red()
                            )
                    )
        elif command:
            embed = discord.Embed(
                        title=f"**{command.cog_name} - {command.name.title()}**\n\n",
                        description=f"Available prefix(es): {', '.join(prefix)}",
                        colour=discord.Colour.blue()
                    )
            embed.add_field(name="Description:", value=command.description)
            embed.add_field(name="Usage:", value=f"`{prefix}{command.usage}`")
            await ctx.send(embed=embed)
        elif cmd == '':
            embed = discord.Embed(
                        title="**Command List:**\n\n",
                        description="Use `.help <cmd>` to get informations on a specific command. All command's name must be lowercase.",
                        colour=discord.Color.green()
                    )
            cog_list = list(self.client.cogs.keys())
            cog_list.remove('Events')
            for cog in cog_list:
                cog_info = self.client.get_cog(cog)
                commands = [i.qualified_name.title() for i in cog_info.get_commands()]
                embed.add_field(name=cog, value=', '.join(commands))
            if not ctx.guild:
                await ctx.send(embed=embed)
            else:
                await ctx.author.send(embed=embed)
                await ctx.send(
                           embed=discord.Embed(
                                    title="**Sent!**",
                                    description="The help message was sent in your DM!",
                                    colour=discord.Color.green()
                                )
                        )
        else:
            await ctx.send(
                        embed=discord.Embed(
                                title='**No Command**',
                                description=f"No commands with the name of **{cmd}**!",
                                colour=discord.Colour.red()
                            )
                    )

def setup(client):
    """Cog set up"""
    client.add_cog(Misc(client))
