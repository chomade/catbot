import traceback
import discord
import os
import sys
import json

from discord.ext import commands
from dotenv import load_dotenv

if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)

load_dotenv()

command_prefix = commands.when_mentioned_or(config["prefix"])

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix=command_prefix, intents=intents)

initial_extensions = ['cogs.voice']


@bot.event
async def on_ready():
    print("Bot is ready!")

    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"Loaded {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}.", file=sys.stderr)
            traceback.print_exc()


bot.run(os.getenv("TOKEN"))
