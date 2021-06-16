"""
Notes Cog

Commands:
- add note
- remove note
- remove all notes
- note list
- get note
"""

import discord
from discord.ext import commands
from bot import config
from .utils import notesdb as db

class Notes(commands.Cog):
    """Notes Cog""" 
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['note'], description='__MODERATOR ONLY__\nAdd a note into this server.', usage='note <key> <text>\nTo update the note, use the same command but with the new text')
    @commands.has_permissions(manage_messages=True)
    async def addnote(self, ctx, key, *, text):
        """Add a note into this server"""
        if not await db.get_note(key, ctx.guild.id):
            await db.add_note(key, ctx.guild.id, text)
            await ctx.send(embed=
                        discord.Embed(
                                title='**Note Added**',
                                description=f'Note {key} added successfully!',
                                colour=discord.Color.green()
                        )
                    )
        elif ctx.guild.id not in config['config']['special_servers'] and len(await db.note_list(ctx.guild.id)) > config['config']['note_limit']:
            await ctx.send(embed=
                        discord.Embed(
                                title='**Note Limit Reached**',
                                description=f"This server has reached the note limit of **{config['config']['note_limit']}**!",
                                colour=discord.Color.red()
                            )
                    )
            return
        elif len(text) > 2048:
            await ctx.send(embed=
                        discord.Embed(
                                title='**Note Character Limit Reached!**',
                                description="You tried to add a note where the text surpasses the character's limit!",
                                colour=discord.Color.red()
                            )
                    )
        else:
            await db.update_note(key, ctx.guild.id, text)
            await ctx.send(embed=
                        discord.Embed(
                                title='**Note Updated**',
                                description=f'Note {key} updated successfully!',
                                colour=discord.Color.red()
                            )
                    )

    @commands.command(aliases=['clear'], description='__MODERATOR ONLY__\nRemove a note in this server.', usage='clear <key>')
    @commands.has_permissions(manage_messages=True)
    async def removenote(self, ctx, key):
        """Removr a note in this server"""
        if await db.get_note(key, ctx.guild.id):
            await db.rm_note(key, ctx.guild.id)
            await ctx.send(embed=
                        discord.Embed(
                                title='**Note Removed**',
                                description=f'Note {key} cleared sucessfully!',
                                colour=discord.Color.green()
                            )
                    )
        else:
            await ctx.send(embed=
                        discord.Embed(
                                title="**Note Doesn't Exist**",
                                description=f"No note with the name of {key}!",
                                colour=discord.Color.red()
                            )
                    )
            
    @commands.command(aliases=['clearall'], description='__MODERATOR ONLY__\nRemove all notes in this server.', usage='clearall')
    async def removeallnotes(self, ctx):
        """Remove all notes in this server"""
        if not await db.note_list(ctx.guild.id):
            await ctx.send(embed=
                        discord.Embed(
                                title="**No Notes**",
                                description="There are no notes in this server!",
                                colour=discord.Color.red()
                            )
                    )
            return
        await db.rm_all(ctx.guild.id)
        await ctx.send(embed=
                    discord.Embed(
                        title="**Notes Removed**",
                        description="All notes in this server have been cleared!",
                        colour=discord.Color.green()
                        )
                )

    @commands.command(aliases=['notes'], description='Get a list of notes in this server', usage='notes')
    async def notelist(self, ctx):
        """Get a list of notes in this server"""
        notes = await db.note_list(ctx.guild.id)
        if not notes:
            await ctx.send(embed=
                        discord.Embed(
                                title="**No Notes**",
                                description="There are no notes in this server!",
                                colour=discord.Color.red()
                            )
                    )
            return
        guild_notes = []
        for note in notes:
            if note[1] == ctx.guild.id:
                guild_notes.append(note[0])
        text = ''
        for i in guild_notes:
            text += f'- {i}\n'
        await ctx.send(embed=
                        discord.Embed(
                            title="**Notes in this servers are:**",
                            description=text,
                            colour=discord.Color.green()
                            )
                    )

    @commands.command(aliases=['get'], description='Get a note in this server', usage='get <key>')
    async def getnote(self, ctx, key):
        """Get a note in this server"""
        note = await db.get_note(key, ctx.guild.id)
        if not note:
            await ctx.send(embed=
                        discord.Embed(
                                title="**Note Doesn't Exist**",
                                description="No note with the name of {key}!",
                                colour=discord.Color.red()
                            )
                    )
            return
        await ctx.send(embed=
                        discord.Embed(
                            title=f"**{note[0]}**",
                            description=note[2],
                            colour=discord.Color.green()
                        )
                    )

def setup(client):
    """Cog set up"""
    client.add_cog(Notes(client))
