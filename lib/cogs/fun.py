from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown
from random import choice, randint
from discord import Member, Embed
from typing import Optional
from aiohttp import request
from discord.errors import HTTPException, Forbidden
from datetime import datetime
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
								  CommandOnCooldown)


class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot


	@command(name='hi', brief='Say hello for me!')
	async def say_hello(self, ctx, member: Member = None):
		"""Say hi for me!"""
		if member == None:
			await ctx.send(f"{choice(['Hello', 'Hi', 'Hey', 'Damn'])}, {ctx.author.mention}!")

		else:
			await ctx.send(f"{ctx.author.mention} said {choice(['hello', 'hi', 'hey', 'damn'])} to {member.mention}")


	@command(name='roll', aliases=['r'], brief='Roll a dice') ### it's a little bug here, and we call the cmd it repeats twice and fuck my brain
	@cooldown(1, 20, BucketType.user)
	async def roll_dice(self, ctx, die_string: str, *, message: str = None):
		"""Roll as many dices with many sides as you want."""
		dice, value = (int(term) for term in die_string.split('d'))

		if dice <= 25:
			rolls = [randint(1, value) for i in range(dice)]
			await ctx.send(f'{message}: ' + ' + '.join([str(r) for r in rolls]) + f' = {sum(rolls)}' if message != None else ' + '.join([str(r) for r in rolls]) + f' = {sum(rolls)}')

		else:
			await ctx.send('Err.. it\'s too many dices for me to roll lower it.')


		#embedr=Embed(title=f'{ctx.author.mention} rolled {value} {dice} times!', colour=0xFF0000, timestamp=utcnow())
		#embedr.add_field(name=f"{message}: {' + '.join([str(r)] for r in rolls)} = {sum(rolls)}" if message != None else f"{' + '.join([str(r)] for r in rolls)} = {sum(rolls)}")

		#await ctx.send(embed=embedr)


	@command(name='slap', aliases=['hit'], brief='Slap someone in his/her face!')
	@cooldown(1, 20, BucketType.user)
	async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = 'no reason'):
		"""Mention someone to slap him/her"""
		await ctx.send(f'{ctx.author.mention} slapped {member.mention} for {reason}')

	@slap_member.error
	async def slap_member_error(self, ctx, exc):
		if isinstance(exc, BadArgument):
			await ctx.send('Err.. i can\'t find that member.')


	@command(name='echo', aliases=['say'], brief='Echo, echo, echo, echo...')
	@cooldown(1, 20, BucketType.user)
	async def echo_messager(self, ctx, *, message):
		"""Echo your message for everyone can see it."""
		await ctx.message.delete()
		await ctx.send(message.capitalize())

	@command(name='fact', brief='Shows up some cool animal facts')
	@cooldown(1, 20, BucketType.user)
	async def fact_command(self, ctx, animal: str):
		"""Animals avaible: koala, fox, dog, cat, bird, panda"""
		if (animal := animal.lower()) in ('dog', 'cat', 'panda', 'bird', 'fox', 'koala'):
			URL = f'https://some-random-api.ml/facts/{animal}'
			IMG = f'https://some-random-api.ml/img/{animal}'

			async with request('GET', IMG, headers={}) as response:
				if response.status == 200:	
					data = await response.json()
					image = data['link']

				else:
					image = None

			async with request('GET', URL, headers={}) as response:
				if response.status == 200:
					data = await response.json()

					em = Embed(title=f'{animal.title()} fact',
								description=data['fact'],
								colour=ctx.author.colour)
					if image is not None:
						em.set_image(url=image)
					await ctx.send(embed=em)

				else:
					await ctx.send(f'API returned a {response.status} status.')
		
		else:
			await ctx.send('No facts avaible for that animal.')


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up('fun')
		print('→Fun cog ready')


def setup(bot):
	bot.add_cog(Fun(bot))