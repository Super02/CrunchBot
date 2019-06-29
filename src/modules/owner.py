from discord.ext import commands
from utils import config
import os

class Owner(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = config.Config()

	async def cog_check(self, ctx: commands.Context):
		return ctx.author.id in self.config._get("config/config", "owners")

	async def cog_command_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send("Only the bot owners can run this command.")

	@commands.command()
	async def testcog(self, ctx):
		await ctx.send("Hejsa")

def setup(bot):
	bot.add_cog(Owner(bot))