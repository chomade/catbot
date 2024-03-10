import discord
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="핑", description="Change the bot settings.")
    async def ping(self, ctx):
        await ctx.reply("퐁! {0}ms".format(round(self.bot.latency * 1000)))

    @commands.bot_has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    @commands.hybrid_command(name="청소", description="채팅을 청소합니다.", aliases=["clear"])
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        embed = discord.Embed(description=f"{amount}개의 메시지를 삭제했습니다.", color=discord.Color.blurple())
        try:
            await interaction.reply(embed=embed, ephemeral=True)
        except:
            await interaction.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
