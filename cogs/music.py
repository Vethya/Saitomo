"""
Music Cog

Commands:
- play
- disconnect
- pause
- resume
- stop
"""

import os

from youtube_dl.utils import DownloadError
from utils.parser import parse_seconds

from discord.ext import commands
import discord
import youtube_dl

class Music(commands.Cog):
    """Music Cog"""
    def __init__(self, client):
        self.client = client

    @commands.command(description="Play music in the voice channel you're in.", usage="play <url>\nUrl is a Youtube video url.")
    async def play(self, ctx, url):
        if not ctx.guild:
            await ctx.send('This command can only be used in a server!')
            return

        filename = f"{ctx.guild.id}.mp3"
        dir = f"./musics/{filename}"
        voice = ctx.author.voice

        if os.path.isfile(dir):
            try:
                os.remove(dir)
            except:
                await ctx.send(
                    embed=discord.Embed(
                        title='Playing Music',
                        description="Please stop the playing music first before playing another music.",
                        colour=discord.Color.red()
                    )
                )
            return
        if not voice:
            await ctx.send(
                    embed=discord.Embed(
                        title='Not in Voice Channel',
                        description="You're not in a voice channel. Please join a voice channel first for this command to work.",
                        colour=discord.Color.red()
                    )
                )
            return
        voice_client = ctx.voice_client
        if not voice_client:
            voice_client = await voice.channel.connect()

        ytdl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
            try:
                ytdl.download([url])
                info = ytdl.extract_info(url)
            except DownloadError:
                await ctx.send(
                    embed=discord.Embed(
                        title='Url Not Supported',
                        description="The url you specified is not supported.",
                        colour=discord.Color.red()
                    )
                )
                return
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, filename)
                os.replace(f"./{filename}", dir)
                
        voice_client.play(discord.FFmpegPCMAudio(dir))
        embed = discord.Embed(title="Playing", colour=discord.Color.green())
        embed.set_thumbnail(url=info['thumbnail'])
        embed.add_field(name="Title", value=info['title'], inline=True)
        embed.add_field(name="Duration", value=parse_seconds(info['duration']), inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['leave'], description="Get the bot out of the voice channel you're in.", usage="leave")
    async def disconnect(self, ctx):
        if not ctx.guild:
            await ctx.send('This command can only be used in a server!')
            return
        
        voice_client = ctx.voice_client
        if not voice_client:
            await ctx.send(
                    embed=discord.Embed(
                        title='Not in Voice Channel',
                        description="I'm not in this voice channel.",
                        colour=discord.Color.red()
                    )
                )
            return
        
        await voice_client.disconnect()
        await ctx.send(
                    embed=discord.Embed(
                        title='Disconnected!',
                        description=f"Successfully disconnected from **{voice_client.channel.name}**.",
                        colour=discord.Color.green()
                    )
                )

    @commands.command(description="Pause the playing music in the voice channel you're in.", usage="pause")
    async def pause(self, ctx):
        if not ctx.guild:
            await ctx.send('This command can only be used in a server!')
            return
        
        voice_client = ctx.voice_client
        if voice_client.is_playing():
            voice_client.pause()
            await ctx.send(
                    embed=discord.Embed(
                        title='Paused!',
                        description=f"Successfully paused the music in **{voice_client.channel.name}**.",
                        colour=discord.Color.green()
                    )
                )
        else:
            await ctx.send(
                    embed=discord.Embed(
                        title='No Music!',
                        description=f"There is no playing music in **{voice_client.channel.name}**.",
                        colour=discord.Color.red()
                    )
                )

    @commands.command(description="Resume the playing music in the voice channel you're in.", usage="resume")
    async def resume(self, ctx):
        if not ctx.guild:
            await ctx.send('This command can only be used in a server!')
            return
        
        voice_client = ctx.voice_client
        if voice_client.is_paused():
            voice_client.resume()
            await ctx.send(
                    embed=discord.Embed(
                        title='Resumed!',
                        description=f"Successfully resumed the music in **{voice_client.channel.name}**.",
                        colour=discord.Color.green()
                    )
                )
        else:
            await ctx.send(
                    embed=discord.Embed(
                        title='No Music!',
                        description=f"There is no paused music in **{voice_client.channel.name}**.",
                        colour=discord.Color.red()
                    )
                )

    @commands.command(description="Stop the playing music in the voice channel you're in.", usage="stop")
    async def stop(self, ctx):
        if not ctx.guild:
            await ctx.send('This command can only be used in a server!')
            return
        
        voice_client = ctx.voice_client
        if voice_client.is_playing() or voice_client.is_paused():
            voice_client.stop()
            await ctx.send(
                    embed=discord.Embed(
                        title='Stopped!',
                        description=f"Successfully stopped the music in **{voice_client.channel.name}**.",
                        colour=discord.Color.green()
                    )
                )
            os.remove(f"./musics/{ctx.guild.id}.mp3")
        else:
            await ctx.send(
                    embed=discord.Embed(
                        title='No Music!',
                        description=f"There is no playing music in **{voice_client.channel.name}**.",
                        colour=discord.Color.red()
                    )
                )

def setup(client):
    """Cog set up"""
    client.add_cog(Music(client))