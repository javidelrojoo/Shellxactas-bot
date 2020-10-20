import discord
from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
	print('Estoy Listo')

@client.command()
async def icon(ctx):
	await ctx.send(discord.Guild.icon)

@client.command()
async def prueba(ctx,arg=None,*,recordatorio=''):
	"""Te manda un mensaje cuando pase el tiempo que le pidas (en segundos)"""
	link=f'https://discord.com/channels/{ctx.message.guild.id}/{ctx.channel.id}/{ctx.message.id}'
	try:
		if arg==None:
			await ctx.send('Poné un tiempo conchudo, no me hagas calentar')
			return
		else:
			await ctx.send(f'Ahora te hago acordar en {round(float(arg))} segundos.')
			await asyncio.sleep(float(arg))
			if recordatorio=='':
				await ctx.send(f'{ctx.author.mention} ya pasó el tiempo. {link}')
			else:
				await ctx.send(f'{ctx.author.mention} ya pasó el tiempo. {recordatorio} {link}')
	except:
		await ctx.send('¿Me estas tratando de pelotudo? Poné un tiempo y dejate de joder.')

client.run('NzY3NTA0MTA2NjMzMDM1Nzk2.X4y35g.QbvMfFCPe1rwbHEJbltl_8vpT9I')
