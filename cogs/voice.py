import os
import discord

from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
password = os.getenv("password")
client = MongoClient(
    f"mongodb+srv://choyoonh2401:{password}@voice.2g8pb9h.mongodb.net/?retryWrites=true&w=majority&appName=voice")
db = client.voiceid


class Voice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="setup", description="Change the bot settings.")
    @commands.bot_has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        category_channel = await interaction.guild.create_category("음성 채널")
        ready_channel = await category_channel.create_voice_channel(name="방-생성하기")
        id = interaction.guild.id
        db.ids.insert_one(
            {
                "guild_id": id,
                "ready_channel_id": ready_channel.id,
            }
        )
        embed = discord.Embed(description="음성 채널 설정이 완료되었습니다.", color=discord.Color.blurple())
        await interaction.reply(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        author = member.guild.id
        key = {"guild_id": author}
        for m in db.ids.find(key):
            voice_channel_id = m["ready_channel_id"]
        try:
            if after.channel.id in [voice_channel_id]:
                ready_channel = self.bot.get_channel(voice_channel_id)
                clone_channel = await ready_channel.clone(name=f"{member.name}의 방")
                await member.move_to(clone_channel)
                await clone_channel.set_permissions(member, connect=True, manage_channels=True)

                def check(a, b, c):
                    return len(clone_channel.members) == 0

                await self.bot.wait_for('voice_state_update', check=check)
                await clone_channel.delete()
        except:
            pass


async def setup(bot):
    await bot.add_cog(Voice(bot))
