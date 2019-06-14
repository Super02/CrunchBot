# Crunchbot - by Super02 & dnorhoj - Copyright 2019
import inspect, os
import discord
from discord.ext import commands

#Declare the bot, and the prefix
startup_extensions = []

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
	lst = []
	for extension in startup_extensions:
		try:
			bot.load_extension(extension)
			lst.append(extension.split('.')[-1])
		except Exception as e:
			exc = "{}: {}".format(type(e).__name__, str(e))
			print("Failed to load {}\n{}".format(extension, exc))
	print("Loaded: {}".format(" and".join(", ".join(lst).rsplit(',', 1))))

#This starts the bot with token
bot.run(os.environ['TOKEN'])