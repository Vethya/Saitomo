import discord
from bot import config

async def check_perm(ctx, member):
    if member == ctx.author:
        return await ctx.send(
                embed=discord.Embed(
                    title='No!',
                    description=f"Please don't {ctx.command.name} yourself! Take a break and think about it.",
                    colour=discord.Color.red()
                )
            )
    if member == ctx.guild.owner:
        return await ctx.send(
                embed=discord.Embed(
                    title='No!',
                    description=f"You can't {ctx.command.name} the owner of the server.",
                    colour=discord.Color.red()
                )
            )
    if member.id in config['config']['dev_id']:
        if ctx.author.id in config['config']['dev_id']:
            return await ctx.send(
                embed=discord.Embed(
                    title='No!',
                    description=f"Come on dude! Don't do that to your comrade.",
                    colour=discord.Color.red()
                    )
                )
        else:
            return await ctx.send(
                embed=discord.Embed(
                    title='No!',
                    description=f"I'm definitely not gonna {ctx.command.name} my developers.",
                    colour=discord.Color.red()
                )
            )
    if member == ctx.me:
        return await ctx.send(
                embed=discord.Embed(
                    title='No!',
                    description=f"Don't make me {ctx.command.name} myself it's tragic.",
                    colour=discord.Color.red()
                )
            )
    if ctx.author.top_role == member.top_role:
        return await ctx.send(
                embed=discord.Embed(
                    title='No!',
                    description=f"You can't {ctx.command.name} someone that has the same permissions as you.",
                    colour=discord.Color.red()
                )
            )
    if ctx.author.top_role < member.top_role:
        return await ctx.send(
                embed=discord.Embed(
                    title='No!',
                    description=f"You can't {ctx.command.name} someone that has more permissions than you.",
                    colour=discord.Color.red()
                )
            )
