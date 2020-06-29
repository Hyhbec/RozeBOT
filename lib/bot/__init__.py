from asyncio import sleep
from datetime import datetime
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed, File, DMChannel
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
								  CommandOnCooldown)
from discord.ext.commands import when_mentioned_or, command, has_permissions

from ..db import db

OWNERID = [652999719710097419]
COGS = [path.split('\\')[-1][:-3] for path in glob('./lib/cogs/*.py')]
IGNORE_EXCEPTIONS =  (CommandNotFound, BadArgument)


def get_prefix(bot, message):
	prefix = db.field('SELECT Prefix FROM guilds WHERE GuildID = ?', message.guild.id)
	return when_mentioned_or(prefix)(bot, message)


class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)


	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f'{cog} cog ready')


	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])



class Bot(BotBase):
	def __init__(self):
		self.guild = None
		self.ready = False
		self.cogs_ready = Ready()
		self.scheduler = AsyncIOScheduler()
		db.autosave(self.scheduler)
		super().__init__(command_prefix=get_prefix, owner_ids=OWNERID)


	def setup(self):
		for cog in COGS:
			self.load_extension(f'lib.cogs.{cog}')
			print(f'{cog} cog loaded')

		print('setup completed')


	def run(self, version):
		self.VERSION = version
		self.setup()

		with open('./lib/bot/token.0', 'r', encoding='utf-8') as tf:
			self.TOKEN = tf.read()

		print('running bot...')
		super().run(self.TOKEN, reconnect=True)


	async def process_commands(self, message):
		ctx = await self.get_context(message, cls=Context)

		if ctx.command is not None and ctx.guild is not None:
			if self.ready:
				await self.invoke(ctx)

			else:
				await ctx.send('Err.. i\'m not ready now!')


	async def on_connect(self):
		print('→bot connected')


	async def on_disconnect(self):
		print('bot disconnected')


	async def on_error(self, err, *args, **kwargs):
		if err == 'on_command_error':
			await  args[0].send('Something went wrong')

		else:
			await self.stdout.send('An error occured')

			raise


	async def on_command_error(self, ctx, exc):
		if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
			pass

		elif isinstance(exc, MissingRequiredArgument):
			await ctx.send('One or more required arguments are missing.')

		elif isinstance(exc, CommandOnCooldown):
			await ctx.send(f"That command is on `{str(exc.cooldown.type).split('.')[-1]}` cooldown. Try again in {exc.retry_after:,.0f} secs.")

		elif hasattr(exc, 'original'):
			if isinstance(exc.original, HTTPException):
				await ctx.send('Unable to respond.')

			elif isinstance(exc.original, Forbidden):
				await ctx.send('Err.. i don\'t have permissiob to do that.')

			else:
				raise exc.original

	async def on_ready(self):
		if not self.ready:
			self.stdout = self.get_channel(727287866824327222)
			self.scheduler.start()
			print('→bot ready')

			while not self.cogs_ready.all_ready():
				await sleep(0.5)

			self.ready = True
			await self.stdout.send('~roze on!')

		else:
			print('bot reconnected')


	async def on_message(self, message):
		if not message.author.bot:
			await self.process_commands(message)


# runs the bot
bot = Bot()