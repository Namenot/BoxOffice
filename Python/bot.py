import discord
from discord.ext import commands

from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions

token = "NDk1OTUxMTU0NjczNjE0ODQ4.DpJiyQ.5NgmMJVfjshxVLt0eBna4ndVVt0"

bot = commands.Bot(command_prefix = '>', description='A Bot that manages a voting system for a movie night.')

voting = []
votes = []
vote = 0

def checkspaces(a):
    nos = 10 #number of spaces
    nos -= len(a)

    if nos >=0:
        while 


    return strg


##here beginns the discord stuff
@bot.event
async def on_ready():
    print("--------------")
    print("Logged in as ")
    print(bot.user.name)
    print(bot.user.id)
    print("--------------")

@bot.event
async def on_message(msg):
    global voting
    global votes
    if msg.content.startswith('>bnominate'):
        voting.append(msg[11:]) ##check the IMdB database
        votes.append(0)


@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def start(ctx):
    global vote
    vote = 1
    await ctx.send("`Voting has begun`")


@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def stop(ctx):
    global vote
    vote = 0
    await ctx.send("`Voting has ended`")

@bot.command()
async def votefor(ctx, a: int):
    if vote:
        strg  = "`You voted for "
        strg += voting[a-1]
        strg += "`"
        await ctx.send(strg)
    else:
        await ctx.send("`Voting is not in progress`")
    #here I still need a system to track all votes

@bot.command()
async def bhelp(ctx):
    strg  = "```The following commands are currently available:\n"
    strg += "----------------------------------------------\n"
    strg += "bstart    : starts the voting process(**_ADMIN_** only)\n"
    strg += "bstop     : stops the voting process(**_ADMIN_** only)\n"
    strg += "binfo     : gives you details about the current vote in progress\n"
    strg += "bvotefor  : let's you vote for a nominated Movie\n"
    strg += "bnominate : let's you nominate a Movie\n"
    strg += "bhelp     : DUH\n```"
    await ctx.send(strg)

@bot.command()
async def info(ctx):
    i = 0
    if len(voting) > 0:
        strg = "```"
        strg += "\n These Movies are currently up for voting:"
        strg += "\n ------------------------------------------\n"
        while i < len(voting):
            strg += "["
            strg += str(i+1)
            strg += "] "
            strg += voting[len(voting)-(i+1)]
            strg += "                      "##add function that finds the necessary number of spaces
            strg += str(votes[len(votes)-(i+1)])
            strg += " votes\n"
            i+= 1

        strg += "```"
        await ctx.send(strg)
    else:
        await ctx.send("`Voting is not in progress`")

bot.run(token)


#misses a fuction were one can nominate a Movie
#misses a fuction that can search a movie data base, to check whether the
#       nominated movie exists
