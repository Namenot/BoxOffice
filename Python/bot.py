import discord
from discord.ext import commands

from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions

token = "NDk1OTUxMTU0NjczNjE0ODQ4.DpJiyQ.5NgmMJVfjshxVLt0eBna4ndVVt0"

bot = commands.Bot(command_prefix = 'b!', description='A Bot that manages a voting system for a movie night.')

voting = []
votes = []
vote = 0

def checkspaces(a):
    nos = 30 #number of spaces
    nos -= len(a)
    if nos >=0:
        strg = a
        for a in range(nos+5):
            strg += " "
    else:
        strg = a[:nos]
        strg += "...  "
    return strg


##here beginns the discord stuff
@bot.event
async def on_ready():
    print("--------------")
    print("Logged in as ")
    print(bot.user.name)
    print(bot.user.id)
    print("--------------")

@bot.command()
async def nominate(ctx, *,msg: str):
    global voting
    global votes
    if vote:
        voting.append(msg) ##check the IMdB database
        votes.append(0)
        print(voting)
        strg  = "``` You nominated "
        strg += msg
        strg += "```"
        await ctx.send(strg)
    else:
        await ctx.send("```Nominting a movie is not possible at the moment```\n")

@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def start(ctx):
    global vote
    vote = 1
    await ctx.send("```Voting has begun```")


@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def stop(ctx):
    global vote
    global voting
    global votes
    vote = 0
    await ctx.send("```Voting has ended```")
    #determin the winner
    votes, voting = zip(*sorted(zip(votes, voting)))
    print(voting)
    strg  = "```The winner is...\n"
    strg += voting[len(voting)-1]
    strg += "\nwith "
    strg += str(votes[len(votes)-1])
    strg += " votes```\n"
    await ctx.send(strg)



@bot.command()
async def votefor(ctx, a: int):
    global votes
    if vote:
        #votes[len(votes)-(a+1)] +=1
        votes[a-1] +=1
        strg  = "```You voted for "
        #strg += voting[len(voting)-(a+1)]
        strg += voting[a-1]
        strg += "```"
        await ctx.send(strg)
    else:
        await ctx.send("```Voting is not in progress```")
    #here I still need a system to track all votes

@bot.command()
async def bhelp(ctx):
    strg  = "```The following commands are currently available:\n"
    strg += "----------------------------------------------\n"
    strg += "start    : starts the voting process(**_ADMIN_** only)\n"
    strg += "stop     : stops the voting process(**_ADMIN_** only)\n"
    strg += "binfo     : gives you details about the current vote in progress\n"
    strg += "votefor  : let's you vote for a nominated Movie\n"
    strg += "nominate : let's you nominate a Movie\n"
    strg += "bhelp     : DUH\n```"
    await ctx.send(strg)

@bot.command()
async def binfo(ctx):
    i = 0
    if len(voting) > 0:
        strg = "```"
        strg += "\n These Movies are currently up for voting:"
        strg += "\n ------------------------------------------\n"
        while i < len(voting):
            strg += "["
            strg += str(i+1)
            strg += "] "
            #strg += voting[len(voting)-(i+1)]
            #strg += "                      "##add function that finds the necessary number of spaces
            #strg += checkspaces(voting[len(voting)-(i+1)])
            #strg += str(votes[len(votes)-(i+1)])
            strg += checkspaces(voting[i])
            strg += str(votes[i])
            strg += " votes\n"
            i+= 1

        strg += "```"
        await ctx.send(strg)
    else:
        await ctx.send("```Voting is not in progress```")

bot.run(token)


#misses a function that checks for double nominations
#misses a function that regulates, that everyone can vote multiple times
#misses a function that can search a movie data base, to check whether the
#       nominated movie exists
