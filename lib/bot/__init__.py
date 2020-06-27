from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

PREFIX = '.'
OWNERID = [652999719710097419]

class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.guild = None
		self.ready = False
		self.scheduler = AsyncIOScheduler()
		super().__init__(command_prefix=PREFIX, owner_ids=OWNERID)

	def run(self, version):
		self.VERSION = version

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
			channel = self.get_channel(725392322698674276)
			await channel.send('An error occured')

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
			print('bot ready')

			channel = self.get_channel(725392322698674276)
			await channel.send('@everyone ~roze on!')

		else:
			print('bot reconnected')


	async def on_message(self, message):
		pass


bot = Bot()