import discord
from discord.ext import commands

token = "NDk1OTUxMTU0NjczNjE0ODQ4.DpJiyQ.5NgmMJVfjshxVLt0eBna4ndVVt0"

bot = commands.Bot(command_prefix = 'b!', description='A Bot that manages a voting system for a movie night.')

@bot.event
async def on_ready():
    print("--------------")
    print("Logged in as ")
    print(bot.user.name)
    print(bot.user.id)
    print("--------------")

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a+b)

@bot.command()
async def multiply(ctx, a: int, b: int):
    await ctx.send(a*b)

@bot.command()
async def greet(ctx):
    await ctx.send(":smiley: :wave: Hello, there!")

@bot.command()
async def cat(ctx):
    await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")

@bot.command()
async def printer(ctx, a: str, b: str):
    a += ""
    b += ""
    c += ""
    c = a + b
    await ctx.send(c)

bot.run(token)
print("Done")
