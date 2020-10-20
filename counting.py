import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
	print('Estoy Listo')

@client.event
async def on_message(message):
	await message.channel.send(round(float(message.content)+1))

client.run('NzY3NTA0MTA2NjMzMDM1Nzk2.X4y35g.QbvMfFCPe1rwbHEJbltl_8vpT9I')
