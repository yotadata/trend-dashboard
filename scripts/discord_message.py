import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def test(ctx):
    embed = discord.Embed(title="テストタイトル", description="テスト本文", color=0x00ff00)
    await ctx.send(embed=embed)

bot.run("YOUR_BOT_TOKEN")
