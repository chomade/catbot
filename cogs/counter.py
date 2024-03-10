import os
import discord

from discord.ext import commands, tasks
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
password = os.getenv("password")
client = MongoClient(
    f"mongodb+srv://choyoonh2401:{password}@voice.2g8pb9h.mongodb.net/?retryWrites=true&w=majority&appName=voice")
db = client.counter


class Counter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.update_counter.start()

    @commands.hybrid_group(fallback=None)
    async def counter(self, interaction: discord.Interaction):
        pass

    @commands.bot_has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @counter.command()
    async def setup(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        result = db.ids.find_one({"guild_id": guild_id})
        members = interaction.guild.members
        bot_count = 0
        member_count = 0
        for i in members:
            if i.bot:
                bot_count += 1
            else:
                member_count += 1
        if result is None:
            category_channel = await interaction.guild.create_category(name="서버 인원")
            await category_channel.set_permissions(interaction.guild.default_role, connect=False, view_channel=True)
            all_member_channel = await category_channel.create_voice_channel(name=f"전체 인원: {bot_count + member_count}")
            member_channel = await category_channel.create_voice_channel(name=f"사람: {member_count}")
            bot_channel = await category_channel.create_voice_channel(name=f"봇: {bot_count}")
            await category_channel.move(beginning=True)
            db.ids.insert_one(
                {
                    "guild_id": guild_id,
                    "category_channel_id": category_channel.id,
                    "all_member_channel_id": all_member_channel.id,
                    "member_channel_id": member_channel.id,
                    "bot_channel_id": bot_channel.id

                }

            )
            embed = discord.Embed(title="설정이 완료되었습니다.", description="10분마다 자동 업데이트합니다.", color=discord.Color.blurple())
            await interaction.reply(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description="이미 설정되어 있습니다.", color=discord.Color.red())
            await interaction.reply(embed=embed, ephemeral=True)

    @commands.bot_has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @counter.command()
    async def reset(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        key = {"guild_id": guild_id}
        try:
            for m in db.ids.find(key):
                all_member_channel_id = m["all_member_channel_id"]
                member_channel_id = m["member_channel_id"]
                bot_channel_id = m["bot_channel_id"]
                category_channel_id = m["category_channel_id"]
            db.ids.delete_one(key)
            await self.bot.get_channel(all_member_channel_id).delete()
            await self.bot.get_channel(member_channel_id).delete()
            await self.bot.get_channel(bot_channel_id).delete()
            await self.bot.get_channel(category_channel_id).delete()
            embed = discord.Embed(description="초기화 되었습니다.", color=discord.Color.blurple())
            await interaction.reply(embed=embed, ephemeral=True)
        except:
            embed = discord.Embed(description="설정이 되어있지 않습니다.", color=discord.Color.red())
            await interaction.reply(embed=embed, ephemeral=True)

    @tasks.loop(minutes=5)
    async def update_counter(self):
        guilds = self.bot.guilds
        for guild in guilds:
            guild_id = guild.id
            key = {"guild_id": guild_id}
            result = db.ids.find_one(key)
            members = guild.members
            bot_count = 0
            member_count = 0
            for i in members:
                if i.bot:
                    bot_count += 1
                else:
                    member_count += 1
            try:
                all_member_channel_id = result["all_member_channel_id"]
                member_channel_id = result["member_channel_id"]
                bot_channel_id = result["bot_channel_id"]
                await self.bot.get_channel(all_member_channel_id).edit(name=f"전체 인원: {bot_count + member_count}")
                await self.bot.get_channel(member_channel_id).edit(name=f"사람: {member_count}")
                await self.bot.get_channel(bot_channel_id).edit(name=f"봇: {bot_count}")
            except:
                pass


async def setup(bot):
    await bot.add_cog(Counter(bot))
