import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import chalk


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

@bot.command(name = "ping", alternative = "Ping")
async def _ping():
    await bot.say("Pong!")
    print ("User has Pinged")

bot.run(TOKEN) #Replace token with your bots token