import discord
from discord.ext import commands, tasks
import remindme as rmdm
import asyncio
import requests
from datetime import datetime, time, timedelta
import pymongo
import os
import campus

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
    async def remindme(self, ctx, tiempo: str, *, recordatorio=''):
        link = ctx.message.jump_url
        if rmdm.tiempo(tiempo) is None:
            await ctx.send('¿Me estas tratando de pelotudo? Poné un tiempo y dejate de joder.')
            return
        else:
            show, wait, frmt = rmdm.tiempo(tiempo)

            authorid = ctx.message.author.id
            channel = ctx.channel.id
            date = datetime.utcnow()
            waitdb = date + timedelta(seconds=wait)
            recor = recordatorio
            datos = {'authorid': authorid, 'channelid': channel, 'wait': waitdb,
                     'recordatorio': recor, 'url': link}
            mongoremindme.insert_one(datos)
            print('El recordatorio se guardó en la base de datos')

            await ctx.send(f'Ahora te hago acordar en {show} {frmt}.')
            await asyncio.sleep(wait)
            await ctx.send(f'{ctx.author.mention} ya pasó el tiempo. {recordatorio} {link}')
            mongoremindme.delete_one(datos)

    @remindme.error
    async def remindme_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send('Poné un tiempo conchudo, no me hagas calentar')
            return

    @commands.group(brief='Fijate el estado del campus',
                      help='Este comando sirve para fijarse si el campus está activo o caido')
    async def campus(self, ctx):
        if ctx.invoked_subcommand is None:
            men = await ctx.send('<a:loading:767587319833690123> A ver, bancame. <a:loading:767587319833690123>')
            estado = campus.estado_campus(5)
            if not estado:
                await men.edit(content='El campus está caido.<a:cross:767588477231038475>')
                return
            if estado:
                await men.edit(content='El campus parece estar funcionando.<a:tick:767588474840154173>')
                return
    
    @campus.command()
    async def historico(self, ctx):
        await ctx.send(f'El campus se cayó {campus.count()} veces.')

    @campus.command()
    async def hoy(self, ctx):
        await ctx.send(f'El campus se cayó {campus.count(datetime.utcnow())} veces hoy.')

    @campus.command()
    async def promedio(self, ctx):
        await ctx.send(f'El promedio de caidas del campus por día es de {round(campus.average(), 2)}.')

    @commands.command(brief='Manda el emoji que elijas',
                      help='Con este comando podes hacer que el bot mande el emoji del server que quieras, incluso '
                           'los animados. Tenés que poner el nombre exacto del emoji, podes usar .emoji lista para '
                           'ver la lista de emojis.')
    @commands.guild_only()
    async def emoji(self, ctx, nombre: str):
        if nombre == 'lista' or nombre == 'list':
            await self.paginas_emoji(ctx)
            return
        for emoji in ctx.message.guild.emojis:
            name = emoji.name
            if nombre == name:
                await ctx.message.delete()
                await ctx.send(f'**{ctx.author.name}**')
                await ctx.send(emoji)
                return
        await ctx.send('No encontré ese emoji en el server. Poné .emoji lista para ver la lista')

    async def paginas_emoji(self, ctx):
        contents = []
        embed = discord.Embed()
        for emoji in ctx.message.guild.emojis:
            embed.add_field(name=emoji.name, value=emoji, inline=True)
            if len(embed.fields) == 24:
                contents.append(embed)
                embed = discord.Embed()
        
        contents.append(embed)
        if contents == []:
            await ctx.send('No hay ningún emoji en este server')
            return
        pages = len(contents)
        cur_page = 1
        contents[0].set_footer(text=f'Pagina {cur_page}/{pages}')
        message = await ctx.send(embed=contents[0])

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=15, check=check)
                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    contents[cur_page-1].set_footer(text=f'Pagina {cur_page}/{pages}')
                    await message.edit(embed=contents[cur_page-1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    contents[cur_page - 1].set_footer(text=f'Pagina {cur_page}/{pages}')
                    await message.edit(embed=contents[cur_page-1])
                    await message.remove_reaction(reaction, user)
                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.remove_reaction("◀️", self.client.user)
                await message.remove_reaction("▶️", self.client.user)
                break

    @emoji.error
    async def emoji_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.NoPrivateMessage):
            await ctx.send('Este comando solo sirve en un server')
            return
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send('Me tenes que decir que emoji querés. Poné .emoji lista para ver la lista')
            return
        raise error

    @commands.command(brief='El github de este bot',
                      help='Con este comando el bot manda el link del github de este bot')
    async def github(self, ctx):
        await ctx.send('https://github.com/javidelrojoo/Shellxactas-bot')

    @commands.command(brief='Agrega un emoji al server',
                      help='Este comando sirve para agregar emojis al server. El archivo que quieras guardar como '
                           'emoji tiene que estar adjunto al mismo mensaje donde pusiste el comando y tiene que ser '
                           'un GIF, PNG o JPG. \n\n Tambien el archivo no puede pesar mas que 256 kb.')
    @commands.guild_only()
    async def emojimaker(self, ctx, nombre: str):
        for emoji in ctx.message.guild.emojis:
            if emoji.name == nombre:
                await ctx.send('Ya hay un emoji con ese nombre.')
                return
        if not ctx.message.attachments:
            await ctx.send('Adjunta el archivo que queres como emoji.')
            return
        for file in ctx.message.attachments:
            ext = file.filename.split('.')[-1]
            await file.save(f'temp.{ext}')
            with open(f"temp.{ext}", "rb") as img:
                img_byte = img.read()
                emoji = await ctx.message.guild.create_custom_emoji(name=nombre, image=img_byte)
                await ctx.send(f'El emoji se agregó correctamente {emoji}')
            os.remove(f"temp.{ext}")

    @emojimaker.error
    async def emojimaker_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, discord.ext.commands.NoPrivateMessage):
            await ctx.send('Este comando solo puede usarse en un server')
            return
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send('Me tenes que decir el nombre que queres para el emoji')
            return
        if isinstance(error, discord.HTTPException):
            await ctx.send(f'No se pudo agregar el emoji, {error}')
            return
        await ctx.send(f'Ocurrió un error, probablemente sea porque el archivo no es ni gif, ni jpg ni png. {error}')

    @commands.command()
    async def estado(self, ctx, url: str):
        men = await ctx.send('<a:loading:767587319833690123> A ver, bancame. <a:loading:767587319833690123>')
        ping = campus.ping(5, url)
        if ping == 0:
            await men.edit(content='La pagina está caida.<a:cross:767588477231038475>')
            return
        if ping == 1:
            await men.edit(content='La pagina parece estar funcionando.<a:tick:767588474840154173>')
            return
        if ping == 2:
            await men.edit(content='¿Eso es una pagina? Probá poniendo el link.')
            return
        if ping == 3:
            await men.edit(content='¿Eso es una pagina? Probá sacando la parte de https://.')
            return

    @estado.error
    async def estado_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send('Me tenes que dar una página para que me fije el estado')

    @commands.command(brief='Te dice el plan de la carrera que quieras')
    async def plan(self, ctx, *,carrera):
        if carrera in ['fisica', 'física', 'df']:
            await ctx.send('https://cdn.discordapp.com/attachments/697915316810022950/773713786262913104/Mapa_Lic_Fisica.png')
            return
        if carrera in ['compu', 'computacion', 'computación', 'dc', 'cs']:
            await ctx.send('https://cdn.discordapp.com/attachments/697915316810022950/758754732906512454/planCs2.png')
            return
        if carrera in ['mate_pura', 'mate pura', 'matematica pura', 'matemática pura']:
            await ctx.send('https://cdn.discordapp.com/attachments/746876013535035402/781131469325205534/planMatePura.png')
            return
        if carrera in ['mate_aplicada', 'mate aplicada', 'matematica aplicada', 'matemática aplicada']:
            await ctx.send('https://cdn.discordapp.com/attachments/697915316810022950/762680026419167232/planMateAplicada.png')
            return
        if carrera in ['oceano', 'océano', 'oceanografia', 'oceanografía']:
            await ctx.send('https://cdn.discordapp.com/attachments/734919493343641611/872598511231860776/Plan_de_Estudios_Oceano_2.0-Copy_of_Page-1.png')
            return
        if carrera in ['quimica', 'química']:
            await ctx.send('https://media.discordapp.net/attachments/750169342666211408/818513992531574814/planQuimica.png')
            return
        if carrera in ['cdd', 'ciencia de datos']:
            await ctx.send('https://media.discordapp.net/attachments/767479713953742938/821216994677227580/correlatividadesLCD.png')
            return
        await ctx.send('Eso no es una carrera')
        await ctx.send('<:picangry:821149118659428354>')
    
    @plan.error
    async def plan_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send('Me tenes que decir alguna carrera de la que quieras el plan')
            await ctx.send('<:picangry:821149118659428354>')

def setup(client):
    client.add_cog(Utilidades(client))
