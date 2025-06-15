import discord
from discord.ext import commands
from config import *
from logic import DB_Manager

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='.',intents=intents)

db = DB_Manager("special_days.db")

@bot.event
async def on_ready():
    print(f'{bot.user.name} botu çalışmaya hazır!')

@bot.command()
async def gunler(ctx, *, ulke_adi):
    cevap = db.specialcountry(ulke_adi)  
    if not cevap:
        return f" {ulke_adi} için özel gün bulunamadı."
    message = f" {ulke_adi} özel günleri:\n"
    for name, date in cevap:
        message += f"{name} ({date})\n"
    await ctx.send(message)

@bot.command()
async def rastgele(ctx):
    cevap = db.randomday()  
    await ctx.send(cevap)


bot.run(TOKEN)