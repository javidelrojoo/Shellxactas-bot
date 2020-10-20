import discord
from discord.ext import commands
import os
import time
import asyncio
import random
import subprocess
import requests

client = commands.Bot(command_prefix='.',case_insensitive=True,description='El bot de Shellxactas')

@client.event
async def on_ready():
	print('Estoy Listo')
	await client.change_presence(activity=discord.Game('Preparando un golpe de estado'))


@client.command()
async def ping(ctx):
	"""Tira el ping del bot"""
	await ctx.send(f'Pong! {round(client.latency*1000,2)} ms')

@client.command()
async def pasalo(ctx):
	"""Te lo pasa"""
	await ctx.send('https://cdn.discordapp.com/attachments/767479713953742938/767502683854340096/20201018_184055.jpg')

@client.command()
async def plan(ctx):
	"""Te dice el plan de la carrera que quieras"""
	await ctx.send('Para que queres saber? Salu2 <:picardia:735101971001770055>')

@client.command()
async def remindme(ctx,arg=''):
	"""Te manda un mensaje cuando pase el tiempo que le pidas (en segundos)"""
	try:
		if arg=='':
			await ctx.send('Poné un tiempo conchudo, no me hagas calentar')
			return
		else:
			await ctx.send(f'Ahora te hago acordar en {round(float(arg))} segundos.')
			await asyncio.sleep(float(arg))
			await ctx.send(f'{ctx.author.mention} ya pasó el tiempo.')
	except:
		await ctx.send('¿Me estas tratando de pelotudo? Poné un tiempo y dejate de joder.')

@client.command()
async def campus(ctx):
	men= await ctx.send('<a:loading:767587319833690123> A ver, bancame. <a:loading:767587319833690123>')
	r=requests.get('https://campus.exactas.uba.ar/')
	try:
		r.raise_for_status()
		await men.edit(content='El campus parece estar funcionando.<a:tick:767588474840154173>')
	except:
		await men.edit(content='El campus está caido.<a:cross:767588477231038475>')


@client.command()
async def steam(ctx):
	men= await ctx.send('<a:loading:767587319833690123> A ver, bancame. <a:loading:767587319833690123>')
	r=requests.get('https://store.steampowered.com/')
	try:
		r.raise_for_status()
		await men.edit(content='Steam parece estar funcionando.<a:tick:767588474840154173>')
	except:
		await men.edit(content='Steam está caido.<a:cross:767588477231038475>')


@client.command()
async def no(ctx):
    await ctx.send(file=discord.File('.\\gifs\\nocat.gif'))

@client.command()
async def si(ctx):
    await ctx.send(file=discord.File('.\\gifs\\yescat.gif'))

@client.command()
async def gif(ctx,arg=''):
	if arg=='':
		await ctx.send('Si no me decis que gif queres no te puedo ayudar. Pelotudo')
		return
	
	try:
		await ctx.send(file=discord.File(f'.\\gifs\\{arg}.gif'))
	except FileNotFoundError:
		await ctx.send('Decime un gif que esté en el server. Pelotudo')

@client.command()
async def rdm(ctx):
	for emoji in ctx.guild.emojis.name:
		await ctx.send(emoji)

@client.command(aliases = ["sensuky", "sensooky"])
async def sensu(ctx):
	await ctx.send('<@219301336544444416> https://www.twitch.tv/sensuky')

@client.command(aliases = ["marcos", "MDG"])
async def markz(ctx):
	await ctx.send('<@710666266972651531> https://es.pornhub.com/gayporn')

@client.command()
async def dolar(ctx):
	URL = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'

	json = requests.get(URL).json()
	
	msg=[' 💵 | compra | venta \n ----|--------|-------']

	for index, emoji in enumerate(('🟢', '🔵')):
		compra = json[index]['casa']['compra'][:-1]
		venta = json[index]['casa']['venta'][:-1]

		msg.append(f"\n {emoji} |  {compra} | {venta}")
	
	await ctx.send("".join(msg))

@client.event
async def on_message(message):
	await client.process_commands(message)
	pedido=[]
	if message.author == client.user or message.author.bot:
		return

	if message.content.lower()=='f':
		await message.add_reaction('🇫')

	if message.content.lower()=='si':
		await message.add_reaction('<a:si:767567093896839179>')

	if message.content.lower()=='no':
		await message.add_reaction('<a:no:767567093482520586>')

	if 'q onda' in message.content.lower():
		await message.add_reaction('<:degenerado:751791150364491966>')

	if 'cringe' in message.content.lower():
		await message.add_reaction('<:cringe:735225671969669221>')

	if '<:picardia:735101971001770055>' in message.content:
	    await message.add_reaction('<:picardia:735101971001770055>')

	if '<:picardiant:748344255906447432>' in message.content:
		await message.add_reaction('<:picardiant:748344255906447432>')

	if 'gracias' in message.content.lower() or 'garcias' in message.content.lower():
		await message.add_reaction('<:garcias:764579105542373387>')
	
	if random.choice(list(range(100)))==0:
		await message.add_reaction(random.choice(message.guild.emojis))
	
	if len(message.content)>500:
		await message.add_reaction('<:mucho_texto:743541235637026818>')

	if 'medialuna' in message.content.lower():
		pedido.append('🥐')

	if 'cafe' in message.content.lower():
		pedido.append(':coffee:')
	if len(pedido)!=0:
		await message.channel.send("".join(pedido))


client.run('NzY3NDQwNzExOTUxMDU2OTM2.X4x83A.8fRi9B6ExpsmkLOhIUlvzUmR4iA')
