import discord
from discord.ext import commands,tasks
import os
import time
import asyncio
import random
import subprocess
import requests
import dolar as dlr
import remindme as rmdm
from boto.s3.connection import S3Connection

client = commands.Bot(command_prefix='.',status=discord.Status.dnd,case_insensitive=True,description='El bot de Shellxactas')

status=['Viendo al coscu','Estudiando','Preparando un golpe de estado','Estudiando para historia de la ciencia','Leyendo el Don Quijote','Haciendome una paja','Analizando el mercado','Comiendome a tu vieja']

@client.event
async def on_ready():
    change_status.start()
    shame_loop.start()
    print('Estoy Listo')

@tasks.loop(minutes=20)
async def change_status():
    await client.change_presence(status=discord.Status.dnd,activity=discord.Game(random.choice(status)))


@tasks.loop(hours=6)
async def shame_loop():
    channel=client.get_channel(734919493343641611)
    file=file=discord.File('img\\shame.gif')
    await channel.send('<@&768612674304606279> Shame!',file=file)

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
async def remindme(ctx,arg=None,*,recordatorio=''):
    """Te manda un mensaje cuando pase el tiempo que le pidas (en segundos)"""
    if arg==None:
        await ctx.send('Poné un tiempo conchudo, no me hagas calentar')
        return
    if ctx.message.guild==None:
        link=f'https://discord.com/channels/@me/{ctx.channel.id}/{ctx.message.id}'
    else:
        link=f'https://discord.com/channels/{ctx.message.guild.id}/{ctx.channel.id}/{ctx.message.id}'
    if rmdm.tiempo(arg)==None:
        await ctx.send('¿Me estas tratando de pelotudo? Poné un tiempo y dejate de joder.')
    else:
        show,wait,frmt=rmdm.tiempo(arg)
        await ctx.send(f'Ahora te hago acordar en {show} {frmt}.')
        await asyncio.sleep(wait)
        await ctx.send(f'{ctx.author.mention} ya pasó el tiempo. {recordatorio} {link}')

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
async def emoji(ctx,arg=None):
    if arg==None:
        await ctx.send('Me tenes que decir que emoji querés.')
        return
    if arg=='lista':
        await ctx.message.add_reaction('<a:tick:767588474840154173>')
        lista=[]
        for emoji in ctx.message.guild.emojis:
            lista.append(f'**{emoji.name}**:{emoji}\n')
            if len(''.join(lista))>1900:
                await ctx.author.send(''.join(lista))
                lista=[]
        await ctx.author.send(''.join(lista))
        return
    for emoji in ctx.message.guild.emojis:
        name=str(emoji.name)
        if str(arg)==name:
            await ctx.send(emoji)
            return
    await ctx.send('No encontré ese emoji en el server. Poné .emoji lista para ver la lista')

@client.command()
async def rdm(ctx):
	await ctx.send(random.choice(ctx.message.guild.emojis))

@client.command(aliases = ["sensuky", "sensooky"])
async def sensu(ctx):
	await ctx.send('<@219301336544444416> <https://www.twitch.tv/sensuky>')

@client.command(aliases = ["marcos", "MDG"])
async def markz(ctx):
	await ctx.send('<@710666266972651531> <https://es.pornhub.com/gayporn>')

@client.command()
async def dolar(ctx):
	if dlr.valor_dolar_blue()==-1:
		await ctx.send('Ocurrió un error.')
		return
	compra,venta,act=dlr.valor_dolar_blue()
	embedVar = discord.Embed(title="Precio Dolar",url="https://www.dolarhoy.com/cotizaciondolarblue",color=0x0400ff)
	embedVar.add_field(name="Compra", value=f"${compra}", inline=False)
	embedVar.add_field(name="Venta", value=f"${venta}", inline=False)
	embedVar.set_footer(text=f"Última actualizacion: {act}")
	await ctx.send(embed=embedVar)

@client.command()
async def dolarapeso(ctx,dolares=None):
    try:
        dolares=float(dolares)
    except ValueError:
        await ctx.send('Ingresá un numero.')
        return
    except TypeError:
        await ctx.send('¿Cuantos dolares queres convertir a pesos?')
        return
    venta=dlr.valor_dolar_blue()[1]
    await ctx.send(f'${round(venta*dolares)}')

@client.command()
async def token(ctx):
	s3 = S3Connection(os.environ['TOKEN'])
	await ctx.send(s3)

@client.command()
async def emojimaker(ctx,name=None):
    if ctx.message.guild==None:
        await ctx.send('Este comando solo funciona en un server.')
        return
    if name==None:
        await ctx.send('Tenes que decirme el nombre que queres.')
        return
    for emoji in ctx.message.guild.emojis:
        if emoji.name==name:
            await ctx.send('Ya hay un emoji con ese nombre.')
            return
    if ctx.message.attachments==[]:
        await ctx.send('Adjunta el archivo que queres como emoji.')
        return
    for file in ctx.message.attachments:
        ext=file.filename.split('.')[-1]
        if ext.lower()!=('gif' and 'jpg' and 'png'):
            await ctx.send('Formato inválido, tiene que ser GIF, JPG o PNG.')
            return
        await file.save(f'temp.{ext}')
    with open(f"temp.{ext}", "rb") as img:
        img_byte = img.read()
        try:
            await ctx.message.guild.create_custom_emoji(name = (f"{name}"), image = img_byte)
        except:
            await ctx.send('El archivo no puede pesar mas de 256 kb.')
            return
    for emoji in ctx.message.guild.emojis:
        if emoji.name==name:
            await ctx.send('El emoji se agregó correctamente')
            return
    ctx.send('Algo falló')

@client.event
async def on_message(message):
	await client.process_commands(message)
	pedido=[]
	if message.author == client.user or message.author.bot:
		return

	if message.content.lower()=='f':
		await message.add_reaction('<:f_:768439683020488724>')

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
	
	if random.choice(list(range(1000)))==0:
		await message.add_reaction(random.choice(message.guild.emojis))
	
	if len(message.content)>500:
		await message.add_reaction('<:mucho_texto:743541235637026818>')
	
	if 'uwu' in message.content.lower() and message.content.lower()!='<:uwu:768614592699957278>':
		await message.add_reaction('<:uwu:768614592699957278>')

	if 'medialuna' in message.content.lower():
		pedido.append('🥐')

	if 'cafe' in message.content.lower():
		pedido.append(':coffee:')
	if len(pedido)!=0:
		await message.channel.send("".join(pedido))


client.run('NzY3NDQwNzExOTUxMDU2OTM2.X4x83A.8fRi9B6ExpsmkLOhIUlvzUmR4iA')
