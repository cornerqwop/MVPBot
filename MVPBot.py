from mvp import MVPList
from mvp import MVP
import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime
from dateutil import tz
import asyncio
import chalk

mvplist = MVPList()

for x in range(0,5):
    #FORMAT FOR NEW MVP: name, spawnMap, respawnRate, weakTo=""
    newMvp = MVP('thantos' + str(x), 'spawnamp' + str(x), random.randint(0,5), "Holy")
    mvplist.push(newMvp)
    pass


BOT_PREFIX = ("?", "!")
TOKEN = "NDI0NzIwNjMzNjI1MDUxMTM2.DY9uPQ.0Qzo6i5lyxoSi2-ZyaXUkUs3x3s"

bot = Bot(command_prefix = BOT_PREFIX) #Initialise client bot


@bot.event 
async def on_ready():
    	print("Bot is online and connected to Discord") #This will be called when the bot connects to the server


@bot.event
async def on_message(message):
    if message.content == "cookie":
        await bot.send_message(message.channel, ":cookie:")#responds with Cookie emoji when someone says "cookie"
    elif message.content == "MVP":
    	await bot.send_message(message.channel, "MVPNAME: " + MvpList[1].name)
    await bot.process_commands(message)

@bot.command(name = "ping", 
    aliases = "Ping")
async def _ping():
    await bot.say("Pong!")
    print ("User has Pinged")

@bot.command(name = "AddMVP", 
    description = "Add a Single MVP to the List\nFORMAT FOR NEW MVP: Name, spawnMap, RespawnRate, WeakTo",
    brief="Add an MVP",
    aliases= ['addmvp', 'Addmvp'], 
    pass_context = True)
async def _MVPAdd(ctx, name, spawnMap,respawnRate,weakTo):
    #FORMAT FOR NEW MVP: name, spawnMap, respawnRate, weakTo=""
    newMvp = MVP(name,spawnMap,respawnRate,weakTo)
    MvpList.append(newMvp)
    await bot.say("NAME: " + MvpList[-1].name + "\nMAP: "+ MvpList[-1].spawnMap +"\nHas Been Added to List")

@bot.command(name = "GetMVP", 
    aliases= ['getmvp', 'Getmvp'], 
    pass_context = True)
async def _MVPGet(ctx, arg):  
    await bot.say(mvplist.printMVP(mvplist.get(arg)))

@bot.command(name = "ListMVPs", 
    aliases= ['listmvps', 'ListMvps'])
async def _MVPShowList():
    formatedString = ""
    formatedString = mvplist.printAll()
    await bot.say(formatedString)

@bot.command(name = "NextMVP", 
    aliases= ['nextMVP', 'next', 'whosnext','WhosNext'])
async def _NextMVP():
    await bot.say(mvplist.printMVP(mvplist.nextUp()))

@bot.command(name = "KilledMVP",
    aliases = ['KMVP', 'Killed', 'SetMVP', 'killed', 'setmvp', 'kmvp', 'killedmvp'])
async def  _KilledMVP(mvpName, tombCoords, timeKilled):
    print(mvpName + " " + tombCoords + " " + timeKilled)
    if(mvplist.get(mvpName) != -1):
        mvplist.setMVP(mvpName,tombCoords,timeKilled)
        await bot.say("Set " + mvpName + " to: \n" + mvplist.printMVP(mvplist.get(mvpName)))
    else:
        await bot.say(mvplist.printMVP(mvplist.get(mvpName)))
    pass

bot.run(TOKEN) #Replace token with your bots token



