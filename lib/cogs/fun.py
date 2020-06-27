from discord.ext.commands import Cog
from discord.ext.commands import command
from random import choice, randint
from discord import Member
from typing import Optional
from discord import Embed
from discord.errors import HTTPException, Forbidden
from datetime import datetime
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
								  CommandOnCooldown)


class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot


	@command(name='hi')
	async def say_hello(self, ctx):
		await ctx.send(f"{choice(['Hello', 'Hi', 'Hey', 'Dammn'])}, {ctx.author.mention}!")


	@command(name='roll', aliases=['r']) ### it's a little bug here, and we call the cmd it repeats twice and fuck my brain
	async def roll_dice(self, ctx, die_string: str, *, message: str = None):
		dice, value = (int(term) for term in die_string.split('d'))

		if dice <= 25:
			rolls = [randint(1, value) for i in range(dice)]
			await ctx.send(f'{message}: ' + ' + '.join([str(r) for r in rolls]) + f' = {sum(rolls)}' if message != None else ' + '.join([str(r) for r in rolls]) + f' = {sum(rolls)}')

		else:
			await ctx.send('Err.. it\'s too many dices for me to roll lower it.')


		#embedr=Embed(title=f'{ctx.author.mention} rolled {value} {dice} times!', colour=0xFF0000, timestamp=utcnow())
		#embedr.add_field(name=f"{message}: {' + '.join([str(r)] for r in rolls)} = {sum(rolls)}" if message != None else f"{' + '.join([str(r)] for r in rolls)} = {sum(rolls)}")

		#await ctx.send(embed=embedr)


	@command(name='slap', aliases=['hit'])
	async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = 'no reason'):
		await ctx.send(f'{ctx.author.mention} slapped {member.mention} for {reason}')

	@slap_member.error
	async def slap_member_error(self, ctx, exc):
		if isinstance(exc, BadArgument):
			await ctx.send('Err.. i can\'t find that member.')


	@command(name='echo', aliases=['say'])
	async def echo_messager(self, ctx, *, message):
		await ctx.message.delete()
		await ctx.send(message.capitalize())


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up('fun')
		print('→Fun cog ready')


def setup(bot):
	bot.add_cog(Fun(bot))