import discord
from discord.ext import commands
import remindme as rmdm
import asyncio

class Utilidades(commands.Cog):

    def __init__(self,client):
        self.client=client
    
    @commands.command(brief='Te dice el ping del bot',help='Usando este comando podes averiguar el ping del bot.')
    async def ping(self,ctx):
        await ctx.send(f'Pong! {round(self.client.latency*1000,2)} ms')

    @commands.command(brief='Te hace acordar de lo que sea',help='Con este comando podés hacer que el bot te haga acordar sobre lo que le pidas. \n\n Como primer argumento (obligatorio) tenes que poner en cuanto tiempo queres que te recuerde (despues del numero pones si queres que sean dias (d), horas (h), minutos (m) o segundos (s), si no pones nada lo toma como segundos). \n\n Como segundo argumento (opcional) podes poner el texto que queres que el bot te recuerde. Una vez que pasó el tiempo el bot te taggea, pone el recordatorio que ingresaste y tambien el link del mensaje original. \n\n Un ejemplo de uso: .remindme 10m ella no te quiere')
    async def remindme(self,ctx,tiempo=None,*,recordatorio=''):
        if tiempo==None:
            await ctx.send('Poné un tiempo conchudo, no me hagas calentar')
            return
        if ctx.message.guild==None:
            link=f'https://discord.com/channels/@me/{ctx.channel.id}/{ctx.message.id}'
        else:
            link=f'https://discord.com/channels/{ctx.message.guild.id}/{ctx.channel.id}/{ctx.message.id}'
        if rmdm.tiempo(tiempo)==None:
            await ctx.send('¿Me estas tratando de pelotudo? Poné un tiempo y dejate de joder.')
        else:
            show,wait,frmt=rmdm.tiempo(tiempo)
            await ctx.send(f'Ahora te hago acordar en {show} {frmt}.')
            await asyncio.sleep(wait)
            await ctx.send(f'{ctx.author.mention} ya pasó el tiempo. {recordatorio} {link}')

def setup(client):
    client.add_cog(Utilidades(client))