import discord
from discord.ext import commands
import random
import asyncio

class Boludeces(commands.Cog):

    def __init__(self,client):
        self.client=client

    @commands.command(brief='Te dice el plan de la carrera que quieras',help='En realidad siempre responde lo mismo.')
    async def plan(self,ctx):
        await ctx.send('Para que queres saber? Salu2 <:picardia:735101971001770055>')

    @commands.command(brief='Es random',help='Manda un emoji random')
    async def rdm(self,ctx):
        await ctx.send(random.choice(ctx.message.guild.emojis))

    @commands.command(brief='Link del twitch de sensu',help='Dale prendé, sensu puto',aliases = ["sensuky", "sensooky"])
    async def sensu(self,ctx):
        await ctx.send('<@219301336544444416> <https://www.twitch.tv/sensuky>')

    @commands.command(brief='Lo que le gusta a markz',help='Es un link a pornhub gay',aliases = ["marcos", "MDG"])
    async def markz(self,ctx):
        await ctx.send('<@710666266972651531> <https://es.pornhub.com/gayporn>')
    
    @commands.command(brief='Que picardia',help='Picardias')
    async def picardy(self,ctx):
        for i in range(15):
            await ctx.send('<:picardia:735101971001770055>')
            await asyncio.sleep(1)
    
    @commands.command(brief='Una piramide',help='Picardias')
    async def piramide(self,ctx):
        for i in range(1,19):
            await ctx.send('<:picardia:735101971001770055>'*i)
            await asyncio.sleep(1)
        for i in range(1,19,-1):
            await ctx.send('<:picardia:735101971001770055>'*i)
            await asyncio.sleep(1)

def setup(client):
    client.add_cog(Boludeces(client))