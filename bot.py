"""
Saitomo bot's core
"""

import os
import logging
from datetime import datetime
import sqlite3
from discord.ext import commands
import yaml

with open('config.yaml') as config:
    config = yaml.safe_load(config)

client = commands.Bot(command_prefix=config['discord']['prefix'])
client.remove_command('help')
prefix = config['discord']['prefix'][0]
runtime = datetime.now()

db = sqlite3.connect('bot.db')

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")
        logging.info(f"Cog {filename[:-3]} loaded!")

client.run(config['discord']['bot_token'])
