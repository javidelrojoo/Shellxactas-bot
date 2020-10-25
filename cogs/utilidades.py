import discord
from discord.ext import commands
import remindme as rmdm
import asyncio
import requests
from datetime import datetime, time, timedelta
import pymongo
import os

mongo_url = os.getenv('MONGO_URL')

mongoclient = pymongo.MongoClient(mongo_url)

mongoprueba = mongoclient['Shellxactas']
mongoremindme = mongoprueba["remindme"]

class Utilidades(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='Te dice el ping del bot', help='Usando este comando podes averiguar el ping del bot.')
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000, 2)} ms')

    @commands.command(brief='Te hace acordar de lo que sea',
                      help='Con este comando podés hacer que el bot te haga acordar sobre lo que le pidas. \n\n Como '
                           'primer argumento (obligatorio) tenes que poner en cuanto tiempo queres que te recuerde ('
                           'despues del numero pones si queres que sean dias (d), horas (h), minutos (m) o segundos ('
                           's), si no pones nada lo toma como segundos). \n\n Como segundo argumento (opcional) podes '
                           'poner el texto que queres que el bot te recuerde. Una vez que pasó el tiempo el bot te '
                           'taggea, pone el recordatorio que ingresaste y tambien el link del mensaje original. \n\n '
                           'Un ejemplo de uso: .remindme 10m ella no te quiere')
    async def remindme(self, ctx, tiempo=None, *, recordatorio=''):
        if tiempo is None:
            await ctx.send('Poné un tiempo conchudo, no me hagas calentar')
            return
        link = ctx.message.jump_url
        if rmdm.tiempo(tiempo) is None:
            await ctx.send('¿Me estas tratando de pelotudo? Poné un tiempo y dejate de joder.')
            return
        else:
            show, wait, frmt = rmdm.tiempo(tiempo)
            
            authorid = ctx.message.author.id
            channel = ctx.channel.id
            date = ctx.message.created_at
            waitdb = date + timedelta(seconds=wait)
            recor = recordatorio
            datos = {'authorid': f'{authorid}', 'channelid': f'{channel}', 'wait': f'{waitdb}',
                     'recordatorio': f'{recor}', 'url': f'{link}'}
            mongoremindme.insert_one(datos)
            print('El recordatorio se guardó en la base de datos')

            await ctx.send(f'Ahora te hago acordar en {show} {frmt}.')
            await asyncio.sleep(wait)
            await ctx.send(f'{ctx.author.mention} ya pasó el tiempo. {recordatorio} {link}')


    @commands.command(brief='Fijate el estado del campus',
                      help='Este comando sirve para fijarse si el campus está activo o caido')
    async def campus(self, ctx):
        men = await ctx.send('<a:loading:767587319833690123> A ver, bancame. <a:loading:767587319833690123>')
        r = requests.get('https://campus.exactas.uba.ar/', timeout=5)
        try:
            r.raise_for_status()
            await men.edit(content='El campus parece estar funcionando.<a:tick:767588474840154173>')
        except:
            await men.edit(content='El campus está caido.<a:cross:767588477231038475>')

    @commands.command(brief='Fijate el estado de steam',
                      help='Este comando sirve para fijarse si steam está activo o caido')
    async def steam(self, ctx):
        men = await ctx.send('<a:loading:767587319833690123> A ver, bancame. <a:loading:767587319833690123>')
        r = requests.get('https://store.steampowered.com/', timeout=5)
        try:
            r.raise_for_status()
            await men.edit(content='Steam parece estar funcionando.<a:tick:767588474840154173>')
        except:
            await men.edit(content='Steam está caido.<a:cross:767588477231038475>')

    @commands.command(brief='Manda el emoji que elijas',
                      help='Con este comando podes hacer que el bot mande el emoji del server que quieras, incluso '
                           'los animados. Tenés que poner el nombre exacto del emoji, podes usar .emoji lista para '
                           'ver la lista de emojis.')
    async def emoji(self, ctx, nombre=None):
        if nombre is None:
            await ctx.send('Me tenes que decir que emoji querés.')
            return
        if nombre == 'lista':
            await ctx.message.add_reaction('<a:tick:767588474840154173>')
            lista = []
            for emoji in ctx.message.guild.emojis:
                lista.append(f'**{emoji.name}**:{emoji}\n')
                if len(''.join(lista)) > 1900:
                    await ctx.author.send(''.join(lista))
                    lista = []
            await ctx.author.send(''.join(lista))
            return
        for emoji in ctx.message.guild.emojis:
            name = str(emoji.name)
            if str(nombre) == name:
                await ctx.send(emoji)
                return
        await ctx.send('No encontré ese emoji en el server. Poné .emoji lista para ver la lista')

    @commands.command(brief='El github de este bot',
                      help='Con este comando el bot manda el link del github de este bot')
    async def github(self, ctx):
        await ctx.send('https://github.com/javidelrojoo/Shellxactas-bot')

    @commands.command(brief='Agrega un emoji al server',
                      help='Este comando sirve para agregar emojis al server. El archivo que quieras guardar como '
                           'emoji tiene que estar adjunto al mismo mensaje donde pusiste el comando y tiene que ser '
                           'un GIF, PNG o JPG. \n\n Tambien el archivo no puede pesar mas que 256 kb.')
    async def emojimaker(self, ctx, nombre=None):
        if ctx.message.guild is None:
            await ctx.send('Este comando solo funciona en un server.')
            return
        if nombre is None:
            await ctx.send('Tenes que decirme el nombre que queres.')
            return
        for emoji in ctx.message.guild.emojis:
            if emoji.name == nombre:
                await ctx.send('Ya hay un emoji con ese nombre.')
                return
        if not ctx.message.attachments:
            await ctx.send('Adjunta el archivo que queres como emoji.')
            return
        for file in ctx.message.attachments:
            ext = file.filename.split('.')[-1]
            if ext.lower() != ('gif' and 'jpg' and 'png'):
                await ctx.send('Formato inválido, tiene que ser GIF, JPG o PNG.')
                return
            await file.save(f'temp.{ext}')
        with open(f"temp.{ext}", "rb") as img:
            img_byte = img.read()
            try:
                await ctx.message.guild.create_custom_emoji(name=(f"{nombre}"), image=img_byte)
            except:
                await ctx.send('El archivo no puede pesar mas de 256 kb.')
                return
        for emoji in ctx.message.guild.emojis:
            if emoji.name == nombre:
                await ctx.send('El emoji se agregó correctamente')
                return
        ctx.send('Algo falló')


def setup(client):
    client.add_cog(Utilidades(client))
