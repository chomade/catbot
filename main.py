import traceback
import discord
import os
import sys
import json

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv

if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json", encoding='utf8') as file:
        config = json.load(file)

load_dotenv()

command_prefix = commands.when_mentioned_or(config["prefix"])
status = config["status"]

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=command_prefix, intents=intents)

initial_extensions = ['cogs.general', 'cogs.voice']


@bot.event
async def on_ready():
    print("Bot is ready!")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.playing, name=status)
    )
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"Loaded {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}.", file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_command_error(context: Context, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description="권한이 없습니다.", color=discord.Color.red())
        await context.send(embed=embed, ephemeral=True)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description="봇이 권한이 없습니다.", color=discord.Color.red())
        await context.send(embed=embed, ephemeral=True)
    elif isinstance(error, commands.NotOwner):
        embed = discord.Embed(description="봇 소유자만 사용할 수 있는 명령어입니다.", color=discord.Color.red())
        await context.send(embed=embed, ephemeral=True)
    elif isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            description=f" {f'{round(hours)} 시간' if round(hours) > 0 else ''}"
                        f" {f'{round(minutes)} 분' if round(minutes) > 0 else ''}"
                        f" {f'{round(seconds)} 초' if round(seconds) > 0 else ''} 뒤에 사용 하실 수 있습니다.",
            color=discord.Color.red()
        )
        await context.send(embed=embed, ephemeral=True)
    elif isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Error!", description=str(error).capitalize(), color=discord.Color.red())
        await context.send(embed=embed, ephemeral=True)
    else:
        raise error


bot.run(os.getenv("TOKEN"))
