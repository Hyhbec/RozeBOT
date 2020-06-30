from asyncio import sleep
from datetime import datetime, timedelta
from re import search
from typing import Optional

from better_profanity import profanity
from discord import Embed, Member
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions

from ..db import db


class Mod(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name='kick')
	@bot_has_permissions(kick_members=True)
	@has_permissions(kick_members=True)
	async def kick_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = 'No reason provided.'):
		if not len(targets):
			await ctx.send('Tell me someone or more to kick.')

		else:
			for target in targets:
				if (ctx.guild.me.top_role.position > target.top_role.position
					and not target.guild_permissions.administrator):
					await target.kick(reason=reason)
					db.execute("DELETE FROM exp WHERE UserID = ?", target.id)

					embed = Embed(title='Member kicked',
								  colour=0xDD2222,
								  timestamp=datetime.utcnow())
					embed.set_thumbnail(url=target.avatar_url)

					fields = [('Member', f'{target.mention}', False),
							  ('Actioned by:', ctx.author.mention, True),
							  ('Reason:', reason.capitalize(), False)]

					for name, value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)


					await self.log_channel.send(embed=embed)

				else:
					await ctx.send(f'I can\'t kick `{target.display_name}` is an administrator')

			await ctx.send('Action completed.')


	@kick_members.error
	async def kick_members_error(self, ctx):
		if isinstance(exc, CheckFailure):
			await ctx.send('Insufficient permissions to perform that task.')


	@command(name='ban')
	@bot_has_permissions(ban_members=True)
	@has_permissions(ban_members=True)
	async def ban_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = 'No reason provided.'):
		if not len(targets):
			await ctx.send('Tell me someone or more to ban.')

		else:
			for target in targets:
				if (ctx.guild.me.top_role.position > target.top_role.position
					and not target.guild_permissions.administrator):
					await target.ban(reason=reason)
					db.execute("DELETE FROM exp WHERE UserID = ?", target.id)

					embed = Embed(title='Member banned',
								  colour=0xDD2222,
								  timestamp=datetime.utcnow())
					embed.set_thumbnail(url=target.avatar_url)

					fields = [('Member', f'{target.mention}', False),
							  ('Actioned by:', ctx.author.mention, True),
							  ('Reason:', reason.capitalize(), False)]

					for name, value, inline in fields:
						embed.add_field(name=name, value=value, inline=inline)


					await self.log_channel.send(embed=embed)

				else:
					await ctx.send(f'I can\'t ban `{target.display_name}` is an administrator')

			await ctx.send('Action completed.')


	@ban_members.error
	async def ban_members_error(self, ctx):
		if isinstance(exc, CheckFailure):
			await ctx.send('Insufficient permissions to perform that task.')


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.log_channel = self.bot.get_channel(727266207581077504)
			self.bot.cogs_ready.ready_up("mod")


def setup(bot):
	bot.add_cog(Mod(bot))