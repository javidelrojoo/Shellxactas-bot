import discord
from discord.ext import commands

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


def setup(client):
    client.add_cog(Boludeces(client))