"""
Saitomo bot's core
"""

import os
import logging
from datetime import datetime
import discord
from discord.ext import commands
import yaml

with open('config.yaml') as config:
    config = yaml.safe_load(config)

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
client = commands.Bot(
            command_prefix=config['discord']['prefix'],
            intents=intents
        )
client.remove_command('help')
prefix = config['discord']['prefix'][0]
runtime = datetime.now()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

for filename in os.listdir('./cogs'):
    name, ext = os.path.splitext(filename)
    if ext == '.py':
        client.load_extension(f"cogs.{name}")
        logging.info(f"Cog {name} loaded!")

client.run(config['discord']['bot_token'])
