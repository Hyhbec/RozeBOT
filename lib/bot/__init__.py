from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from glob import glob

from ..db import db

PREFIX = '.'
OWNERID = [652999719710097419]
COGS = [path.split('\\')[-1][:-3] for path in glob('./lib/cogs/*.py')]

class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.guild = None
		self.ready = False
		self.scheduler = AsyncIOScheduler()
		db.autosave(self.scheduler)
		super().__init__(command_prefix=PREFIX, owner_ids=OWNERID)


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


	async def on_connect(self):
		print('bot connected')


	async def on_disconnect(self):
		print('bot disconnected')


	async def on_error(self, err, *args, **kwargs):
		if err == 'on_command_error':
			await  args[0].send('Something went wrong')

		else:
			await self.stdout.send('An error occured')

			raise


	async def on_command_error(self, ctx, exc):
		if isinstance(exc, CommandNotFound):
			await ctx.send('Err.. command not found')

		elif hasattr(exc, 'original'):
			raise exc.original

		else:
			raise exc

	async def on_ready(self):
		if not self.ready:
			self.ready = True
			self.stdout = self.get_channel(725392322698674276)
			self.scheduler.start()
			print('bot ready')

			await self.stdout.send('@everyone ~roze on!')

		else:
			print('bot reconnected')


	async def on_message(self, message):
		pass


# runs the bot
bot = Bot()