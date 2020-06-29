from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions
from discord import Embed

from ..db import db

class Admin(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="prefix")
	@has_permissions(manage_guild=True)
	async def change_prefix(self, ctx, new: str):
		"""Admin command that changes server prefix."""
		if len(new) > 3:
			await ctx.send("The prefix can not be more than 3 characters in length.")

		else:
			db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
			await ctx.send(f"Prefix set to `{new}`.")

	@change_prefix.error
	async def change_prefix_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("You need the Manage Server permission to do that.")


	@command(name='serverinfo', aliases=['sinfo'], brief='')
	@has_permissions(manage_guild=True)
	async def show_server_info(self, ctx):
		"""Show server info."""
		em = Embed(title=f'{ctx.guild.name} Server Information',
				   description='Informations:',
				   colour=ctx.author.colour)
		em.add_field(name='Server name:', value=f'{ctx.guild.name}', inline=False)
		em.add_field(name='Server owner:', value=f'{ctx.guild.owner}', inline=False)
		em.add_field(name='Member count:', value=f'{ctx.guild.member_count}', inline=False)
		await ctx.send(embed=em)

	@show_server_info.error
	async def show_server_info_error(self, ctx):
		if isinstance(exc, CheckFailure):
			await ctx.send('You need the Manage Server permission to do that.')


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("admin")


def setup(bot):
	bot.add_cog(Admin(bot))