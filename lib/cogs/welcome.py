from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Forbidden
from discord import Embed
from datetime import datetime

from ..db import db

class Welcome(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("welcome")


	@Cog.listener()
	async def on_member_join(self, member):
		db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
		#await self.bot.get_channel(727266182864044052).send(f"Welcome to **{member.guild.name}**, {member.mention}!")

		em=Embed(title=f'{member.display_name}', description='• User joined', timestamp=datetime.utcnow())
		await self.bot.get_channel(727266182864044052).send(embed=em)

		try:
			await member.send(f"Welcome to **{member.guild.name}**! Enjoy your stay!")

		except Forbidden:
			pass

		await member.add_roles(member.guild.get_role(727267159763583006))


	@Cog.listener()
	async def on_member_remove(self, member):
		db.execute("DELETE FROM exp WHERE UserID = ?", member.id)
		#await self.bot.get_channel(727266182864044052).send(f"{member.mention} has left {member.guild.name}.")

		em=Embed(title=f'{member.display_name}', description='• User lefted', timestamp=datetime.utcnow())
		await self.bot.get_channel(727266182864044052).send(embed=em)
		

def setup(bot):
	bot.add_cog(Welcome(bot))