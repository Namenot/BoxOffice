import sys
import auth as au
import utilities as u
import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

token = au.token

bot = commands.Bot(command_prefix = 'b!', description='A Bot that manages a voting system for a movie night.')

voting = [] #movies that are nominated
votes  = [] #the votes each movie has
voters = [] #authors and their respective votes
allowvote     = 0
allownominate = 0

def nodoublicates(newM, lst):
    return newM not in lst

def test2Dpos(newM, lst):
    for x in range(len(lst)):
        if newM in lst[x][0]:
            return x
    return -1

##here beginns the discord stuff
@bot.event
async def on_ready():
    print("--------------")
    print("Logged in as ")
    print(bot.user.name)
    print(bot.user.id)
    print("--------------")

@bot.command()
@has_permissions(administrator=True)
async def end(ctx):
    await ctx.send("```Shuting down the Bot```")
    sys.exit()

@bot.command(pass_context=True)
async def nominate(ctx, *,msg: str):
    global voting
    global votes
    author = ctx.message.author.name
    if allownominate:
        if nodoublicates(msg, voting):
            voting.append(msg) ##check the IMdB database
            votes.append(0)
            strg  = "```"
            strg += author
            strg += " nominated "
            strg += msg
            strg += "```"
        else:
            strg  = "```Error: "
            strg += msg
            strg += " is already nominated```\n"
        await ctx.send(strg)
    else:
        await ctx.send("```Nominting a movie is not possible at the moment```\n")

@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def startv(ctx):
    global allowvote
    global allownominate
    global voters
    global votes

    if voting:
        allowvote = 1
        allownominate = 0
        await ctx.send("```Nominating has ended```")
        await ctx.send("```Voting has begun```")
    else:
        await ctx.send("```The Voting process can not be started without any Movies beeing nominated```")

@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def startn(ctx):
    global voting
    global allowvote
    global allownominate

    del voting[:] #(prevents old votes to be inherited)
    del votes [:]
    del voters[:] #empties every list that already exists

    allowvote = 0
    allownominate = 1
    await ctx.send("```Nomination process has started```")

@bot.command(pass_context=True)
@has_permissions(administrator=True)
async def stop(ctx):
    global allowvote
    global voting
    global votes
    allowvote = 0
    await ctx.send("```Voting has ended```")
    #determin the winner
    votes, voting = zip(*sorted(zip(votes, voting)))
    strg  = "```The winner is...\n"
    strg += voting[len(voting)-1]
    strg += "\nwith "
    strg += str(votes[len(votes)-1])
    strg += " votes```\n"
    strg += '```to join our Rabbit room click the link below```'
    strg += au.rabbit
    await ctx.send(strg)



@bot.command(pass_context=True)
async def votefor(ctx, a):

    strg = ""

    author = ctx.message.author.name
    vote   = [None]*2

    vote[0] = author

    global votes
    global voters
    if allowvote:
        if nodoublicates(author, voters):
            if a.isdigit():
                a = int(a)
            else:
                match = [s for s in voting if a in s]
                if len(match) == 1:
                    pos = [i for i, x in enumerate(voting) if x == match[0]]
                    a = pos[0] + 1
                else:
                    a = 0
                    strg = "```Could select a Movie, as the given name was not specific enough```"

            if a <= len(votes) and a > 0:
                vote[1] = a
                voters.append(vote)
                votes[a-1] +=1
                strg  = "```"
                strg += author
                strg += "voted for "
                strg += voting[a-1]
                strg += "```"
            elif a == 0:
                pass
            else:
                strg = "```Error: vote out of range```"
                print("a     : ", a)
                print("votes :", votes)
                print("voting:", voting)

            await ctx.send(strg)
        else:
            await ctx.send("```Error: You've already voted```")
    else:
        await ctx.send("```Voting is not in progress```")

@bot.command(pass_context=True)
async def rmvote(ctx):
    global voters
    global votes
    if allowvote:
        author = ctx.message.author.name
        pos = test2Dpos(author, voters)
        if pos != -1:
            item = voters[pos][1] - 1
            votes[item] -= 1
            del voters[pos]
            strg = "```"
            strg += author
            strg += " removed their vote```"
            await ctx.send(strg)
        else:
            await ctx.send("```Error: You didn't vote yet```")
    else:
        await ctx.send("```Error: Voting is not possible at the moment")

@bot.command()
async def bhelp(ctx):
    strg  = "```The following commands are currently available:\n"
    #strg += "------------------------------------------------------------------------\n"

    strg += "\nAdmin Commands:\n"
    strg += "------------------------------------------------------------------------\n"
    strg += "startv   : starts the voting process\n"
    strg += "startn   : starts the nomination process\n"
    strg += "stop     : stops the voting process\n"
    strg += "end      : shuts the Bot down\n"
    strg += "------------------------------------------------------------------------\n"

    strg += "\nUser Commands:\n"
    strg += "------------------------------------------------------------------------\n"
    strg += "binfo    : gives you details about the current vote in progress\n"
    strg += "votefor  : let's you vote for a nominated Movie\n"
    strg += "rmvote   : removes your vote\n"
    strg += "nominate : lets you nominate a Movie\n"
    strg += "bhelp    : gives you a list of every command + description of each, duh!\n"
    strg += "------------------------------------------------------------------------\n```"
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
            strg += u.checkspaces(voting[i])
            strg += str(votes[i])
            strg += " votes\n"
            i+= 1

        strg += "```"
        await ctx.send(strg)
    else:
        await ctx.send("```Voting is not in progress```")

bot.run(token)

#test rmvote function (+ everything else again for possible new errors)

#misses a function that can search a movie data base, to check whether the
#       nominated movie exists
