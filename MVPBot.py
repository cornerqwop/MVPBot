from mvp import MVPList
from mvp import MVP
import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime, timezone
import datetime
import asyncio
import chalk
import json
import re

minute = datetime.timedelta(seconds = 60)
hour = 60 * minute
day = 24 * hour
BOT_PREFIX = ("?", "!")
TOKEN = "NDI0NzIwNjMzNjI1MDUxMTM2.DY9uPQ.0Qzo6i5lyxoSi2-ZyaXUkUs3x3s"
MVPDataFile = 'data.txt'
mvplist = MVPList()
bot = Bot(command_prefix = BOT_PREFIX) #Initialise client bot
utc_dt = datetime.datetime.utcnow()
dt = utc_dt.astimezone() 
now = datetime.datetime.utcnow()

def currentTime():
    return datetime.datetime.utcnow()

#Read Data from JSON File On Load
def OpenMVPdata():
    with open(MVPDataFile) as json_file:  
        data = json.load(json_file)
        for p in data['MVP']:
            newMvp = MVP(
                p['name'],
                p['spawnMap'],
                p['respawnRate'],
                p['weakTo']
            )
            tombCoords = p['tombCoords']
            timeKilled = p['timeKilled']
            t = re.split('\D', timeKilled)
            toSet =  str(t[3]) + ':'+ str(t[4])
            mvplist.push(newMvp)
            mvplist.setMVP(p['name'], tombCoords, toSet)
    print('MVP DATA LOAD SUCCESS')

#Store Data in JSON File
def StoreMVPdata():
    data = {} 
    data['MVP'] = []
    for x in mvplist.mvps:
        data['MVP'].append({
            'name' : mvplist.mvps[x].name,
            'spawnMap' : mvplist.mvps[x].spawnMap,
            'respawnRate' : mvplist.mvps[x].respawnRate,
            'weakTo' : mvplist.mvps[x].weakTo,
            'tombCoords' : mvplist.mvps[x].tombCoords,
            'timeKilled' : mvplist.mvps[x].timeKilled.strftime("%Y-%m-%d %H:%M"),
            'respawnTime' : mvplist.mvps[x].respawnTime.strftime("%Y-%m-%d %H:%M")
        })

    with open(MVPDataFile, 'w') as outfile:  
        json.dump(data, outfile, indent=4)
    print('MVP DATA SAVED')

#####CREATE DUMMY MVPS FOR TESTING
def DebugTest():
    for x in range(0,1):
        #FORMAT FOR NEW MVP: name, spawnMap, respawnRate, weakTo=""
        newMvp = MVP('thantos' + str(x), 'spawnamp' + str(x), random.randint(200,600), "Holy")
        timeKilled = str(random.randint(10,12)) +":"+  str(random.randint(0,2))
        tombCoords = "00,00"
        mvplist.push(newMvp)
        mvplist.setMVP(newMvp.name, tombCoords,timeKilled)
        pass
    StoreMVPdata()

#######

@bot.event 
async def on_ready():
    	print("Bot is online and connected to Discord") #This will be called when the bot connects to the server


@bot.event
async def on_message(message):
    if message.content == "cookie":
        await bot.send_message(message.channel, ":cookie:")#responds with Cookie emoji when someone says "cookie"
    elif message.content == "MVP":
    	await bot.send_message(message.channel, "MVPNAME: " + mvplist.nextUp())
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
    mvplist.push(newMvp)
    StoreMVPdata()
    await bot.say(mvplist.printMVP(mvplist.get(name)))

@bot.command(name = "GetMVP", 
    aliases= ['getmvp', 'Getmvp'], 
    pass_context = True)
async def _MVPGet(ctx, arg):  
    await bot.say(mvplist.printMVP(mvplist.get(arg)))

@bot.command(name = "ListMVPs", 
    aliases= ['listmvps', 'ListMvps', 'list'])
async def _MVPShowList():
    formatedString = ""
    formatedString = mvplist.printAll()
    await bot.say(formatedString)

@bot.command(name = "NextMVP", 
    aliases= ['nextMVP', 'next', 'whosnext','WhosNext'])
async def _NextMVP():
    await bot.say("Current Time is: " + now.strftime("%Y-%m-%d %H:%M"))
    await bot.say(mvplist.printMVP(mvplist.nextUp()))

@bot.command(name = "KilledMVP",
    aliases = ['KMVP', 'Killed', 'SetMVP', 'killed', 'setmvp', 'kmvp', 'killedmvp'])
async def  _KilledMVP(mvpName, tombCoords, timeKilled):
    print(mvpName + " " + tombCoords + " " + timeKilled)
    if(mvplist.get(mvpName) != -1):
        if mvplist.setMVP(mvpName,tombCoords,timeKilled) != -1:
            mvplist.setMVP(mvpName,tombCoords,timeKilled)
            await bot.say("Set " + mvpName + " to: \n" + mvplist.printMVP(mvplist.get(mvpName)))
        else:
            await bot.say("IMPROPER TIME FORMAT")
    else:
        await bot.say(mvplist.printMVP(mvplist.get(mvpName)))
    pass
    StoreMVPdata()

#Keep Track of time
async def display_date(loop):
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.utcnow())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)






print("\n\nCurrent Time is:" + now.strftime("%Y-%m-%d %H:%M") )

#Load and Save data on start of the bot

OpenMVPdata()
StoreMVPdata()

bot.run(TOKEN) #Replace token with your bots token

loop = asyncio.get_event_loop()
# Blocking call which returns when the display_date() coroutine is done
loop.run_until_complete(display_date(loop))



