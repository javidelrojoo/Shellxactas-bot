import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, time, timedelta
import pymongo
import os

mongo_url = os.getenv('MONGO_URL')

mongoclient = pymongo.MongoClient(mongo_url)

mongoprueba = mongoclient['Shellxactas']
mongocumple = mongoprueba["cumpleaños"]


class Birthday(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['bd_agregar'], brief='Agregá tu cumpleaños a la lista', help='Agregá tu cumpleaños '
                                                                                            'para que el bot te desee'
                                                                                            ' un feliz cumpleaños, '
                                                                                            'el formato de la fecha '
                                                                                            'es \'DD/MM\'')
    async def bd_add(self, ctx, fecha: str):
        lista = fecha.split('/')
        if len(lista) != 2:
            await ctx.send('Formato Inválido, tiene que ser de la forma \'DD/MM\'')
            return
        dia, mes = lista
        try:
            dia = int(dia)
            mes = int(mes)
        except ValueError:
            await ctx.send('Formato Inválido, tiene que ser de la forma \'DD/MM\'')
            return
        authorid = ctx.message.author.id
        channelid = ctx.channel.id
        try:
            datos = {'_id': f'{authorid}', 'channelid': f'{channelid}', 'dia': f'{dia}', 'mes': f'{mes}'}
            mongocumple.insert_one(datos)
        except pymongo.errors.DuplicateKeyError:
            await ctx.send('Ya tengo registrado tu cumpleaños, podes usar .bd_delete para borrar tu cumpleaños.')
            return
        await ctx.send('Se guardó el cumpleaños')

    @commands.command(aliases=['bd_del', 'bd_borrar'], brief='Borrá tu cumpleaños', help='Usá este comando para '
                                                                                         'borrar tu cumpleaños')
    async def bd_delete(self, ctx):
        authorid = ctx.message.author.id
        query = mongocumple.find_one({'_id': f'{authorid}'})
        if query is None:
            await ctx.send('No tengo tu cumpleaños registrado')
            return
        else:
            mongocumple.delete_one(query)
            await ctx.send('Ya eliminé tu cumpleaños')
            return


def setup(client):
    client.add_cog(Birthday(client))
