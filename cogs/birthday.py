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


class Birthday(commands.Cog, name='Cumpleaños'):

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
        if dia > 31 or dia < 0:
            await ctx.send('Día Inválido')
            return
        if mes > 12 or mes < 0:
            await ctx.send('Mes Inválido')
            return
        authorid = ctx.message.author.id
        channelid = ctx.channel.id
        try:
            datos = {'_id': authorid, 'channelid': channelid, 'dia': dia, 'mes': mes}
            mongocumple.insert_one(datos)
        except pymongo.errors.DuplicateKeyError:
            await ctx.send('Ya tengo registrado tu cumpleaños, podes usar .bd_delete para borrar tu cumpleaños.')
            return
        await ctx.send('Se guardó el cumpleaños')

    @commands.command(aliases=['bd_del', 'bd_borrar'], brief='Borrá tu cumpleaños', help='Usá este comando para '
                                                                                         'borrar tu cumpleaños')
    async def bd_delete(self, ctx):
        authorid = ctx.message.author.id
        query = mongocumple.find_one({'_id': authorid})
        if query is None:
            await ctx.send('No tengo tu cumpleaños registrado')
            return
        else:
            mongocumple.delete_one(query)
            await ctx.send('Ya eliminé tu cumpleaños')
            return

    @commands.command(aliases=['bd_lista'])
    async def bd_list(self, ctx):
        emb = discord.Embed(title='Lista de Cumpleaños', color=0xfc0303)
        for bday in mongocumple.find().sort([('mes', pymongo.ASCENDING), ('dia', pymongo.ASCENDING)]):
            author = self.client.get_user(int(bday['_id']))
            dia = bday['dia']
            mes = bday['mes']
            emb.add_field(name=f'{author}', value=f'{dia}/{mes}', inline=True)
        await ctx.send(embed=emb)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def bdforce_add(self, ctx, fecha: str, member: discord.User, channel: discord.channel.TextChannel):
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
        if dia > 31 or dia < 0:
            await ctx.send('Día Inválido')
            return
        if mes > 12 or mes < 0:
            await ctx.send('Mes Inválido')
            return
        authorid = member.id
        channelid = channel.id
        try:
            datos = {'_id': authorid, 'channelid': channelid, 'dia': dia, 'mes': mes}
            mongocumple.insert_one(datos)
        except pymongo.errors.DuplicateKeyError:
            await ctx.send('Ya tengo registrado un cumpleaños con este usuario')
            return
        await ctx.send('Se guardó el cumpleaños')

    @bdforce_add.error
    async def bdforce_add_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.MissingPermissions):
            await ctx.send('Solo los admin pueden usar este comando <:pepe_cool:755853836865896448>')
            return
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            if error.param.name == 'member':
                await ctx.send('Te falta el usuario')
                return
            if error.param.name == 'channel':
                await ctx.send('Te falta el canal')
                return
        if isinstance(error, discord.ext.commands.UserNotFound):
            await ctx.send('No encontré a ese usuario')
            return
        if isinstance(error, discord.ext.commands.errors.ChannelNotFound):
            await ctx.send('No encontré a ese canal')
        raise error

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def bdforce_delete(self, ctx, member: discord.User):
        authorid = member.id
        query = mongocumple.find_one({'_id': authorid})
        if query is None:
            await ctx.send('No tengo un cumpleaños asociado a este usuario registrado')
            return
        else:
            mongocumple.delete_one(query)
            await ctx.send('Ya eliminé el cumpleaños')
            return

    @bdforce_delete.error
    async def bdforce_delete_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.MissingPermissions):
            await ctx.send('Solo los admin pueden usar este comando <:pepe_cool:755853836865896448>')
            return
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send('Te falta el usuario')
            return
        if isinstance(error, discord.ext.commands.UserNotFound):
            await ctx.send('No encontré a ese usuario')
            return
        raise error


def setup(client):
    client.add_cog(Birthday(client))
