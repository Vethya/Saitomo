"""
Music Cog

Commands:
- play
- disconnect
- pause
- resume
- stop
"""

from utils.parser import parse_seconds
from utils.matcher import music_url_type
from utils.youtube import search, get_video_info
from utils.spotify import get_track_info

from discord.ext import commands
import discord

class Music(commands.Cog):
    """Music Cog"""
    def __init__(self, client):
        self.client = client

    @commands.command(description="Play music in the voice channel you're in.", usage="play <url>\nUrl is a Youtube or Spotify url.")
    async def play(self, ctx, url):
        if not ctx.guild:
            await ctx.send('This command can only be used in a server!')
            return

        voice = ctx.author.voice
        voice_client = ctx.voice_client

        if not voice:
            await ctx.send(
                    embed=discord.Embed(
                        title='Not in Voice Channel',
                        description="You're not in a voice channel. Please join a voice channel first for this command to work.",
                        colour=discord.Color.red()
                    )
                )
            return

        url_type = music_url_type(url)
        if url_type == "youtube":
            music = get_video_info(url)

        elif url_type == "spotify":
            track = get_track_info(url)
            youtube_url = search(f"{track['artist']} - {track['name']}")

            music = get_video_info(youtube_url)

        elif url_type == "invalid":
            await ctx.send(
                    embed=discord.Embed(
                        title='Unsupported Url',
                        description="This url is either invalid or currently unsupported.",
                        colour=discord.Color.red()
                    )
                )
            return

        if not voice_client:
            voice_client = await voice.channel.connect()

        if voice_client.is_playing():
            await ctx.send(
                    embed=discord.Embed(
                        title='Playing Music',
                        description="Please stop the playing music first before playing another music.",
                        colour=discord.Color.red()
                    )
                )
            return
        
        voice_client.play(discord.FFmpegPCMAudio(music["formats"][0]["url"], before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
        embed = discord.Embed(title="Playing", colour=discord.Color.green())
        embed.add_field(name="Title", value=music['title'], inline=True)
        embed.add_field(name="Duration", value=parse_seconds(music['duration']), inline=True)
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