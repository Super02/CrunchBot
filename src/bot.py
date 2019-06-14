# Crunchbot - by Super02 & dnorhoj - Copyright 2019
import discord, inspect, secret
from discord.ext import commands

#Declare the bot, and the prefix
startup_extensions = ()

bot = commands.Bot(command_prefix=commands.when_mentioned_or('+'))

#This will run when the bot starts
@bot.event
async def on_ready():
	print("Bot started")
	print("Logged in as: {0}\nID: {0.id}".format(bot.user))
	
	await bot.change_presence(activity=discord.Game(name="+help"))

@bot.command()
async def test(ctx):
	await ctx.send("This bot is working")

#Load cogs
if __name__ == "__main__":
	lst = ""
	i = 0
	for extension in startup_extensions:
		try:
			bot.load_extension(extension)
			if(i==0):
				lst = lst + "{}".format(extension)
			else:
				lst = lst + ", {}".format(extension)
			i+=1
		except Exception as e:
			exc = "{}: {}".format(type(e).__name__, str(e))
			print("Failed to load {}\n{}".format(extension, exc))
	lst = (lst[::-1].replace(","[::-1]," and"[::-1], 1))[::-1].replace("cogs.","")
	print("Loaded: {}".format(lst))

#This starts the bot with token
bot.run(secret.token)