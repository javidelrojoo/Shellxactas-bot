import discord
from discord.ext import commands
import random
import asyncio
import img_editor as img


class Boludeces(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='Te dice el plan de la carrera que quieras', help='En realidad siempre responde lo mismo.')
    async def plan(self, ctx):
        await ctx.send('Para que queres saber? Salu2 <:picardia:735101971001770055>')

    @commands.command(brief='Es random', help='Manda un emoji random')
    async def rdm(self, ctx):
        await ctx.send(random.choice(ctx.message.guild.emojis))

    @commands.command(brief='Link del twitch de sensu', help='Dale prendé, sensu puto', aliases=["sensuky", "sensooky"])
    async def sensu(self, ctx):
        await ctx.send('<@219301336544444416> <https://www.twitch.tv/sensuky>')

    @commands.command(brief='Lo que le gusta a markz', help='Es un link a pornhub gay', aliases=["marcos", "MDG"])
    async def markz(self, ctx):
        await ctx.send('<@710666266972651531> <https://es.pornhub.com/gayporn>')

    @commands.command(brief='Que picardia', help='Picardias')
    @commands.has_permissions(administrator=True)
    async def picardy(self, ctx):
        for i in range(15):
            await ctx.send('<:picardia:735101971001770055>')
            await asyncio.sleep(1)

    @picardy.error
    async def picardy_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send('Solo los admin pueden usar este comando <:pepe_cool:755853836865896448>')
            return
        raise error

    @commands.command(brief='Una piramide', help='Picardias')
    async def piramide(self, ctx):
        for i in range(1, 6):
            await ctx.send('<:picardia:735101971001770055>' * i)
            await asyncio.sleep(1)
        for i in list(range(1, 5))[::-1]:
            await ctx.send('<:picardia:735101971001770055>' * i)
            await asyncio.sleep(1)
    
    @commands.command()
    async def picardia(self, ctx):
        if not ctx.message.attachments:
            await ctx.send('Adjunta la imagen a la que le queres agregar el picardia.')
            return
        for file in ctx.message.attachments:
            ext = file.filename.split('.')[-1]
            await file.save(f'temp.{ext}')
            img.picardia_overlay(f'temp.{ext}')
            await ctx.send(file=discord.File('edit.png'))

    @commands.command(aliases=['traductorjose'])
    async def josetraductor(self, ctx, *, palabra: str):
        palabra = palabra.replace(' ', '+')
        await ctx.send(f'https://www.urbandictionary.com/define.php?term={palabra}')

    @josetraductor.error
    async def josetraductor_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send('Me tenes que decir algo que quieras traducir')
    
    @commands.command()
    async def F(self, ctx):
        for i in [5, 1, 3, 1, 1, 1]:
            await ctx.send('<:picardiant:748344255906447432>' * i)
            await asyncio.sleep(1)


def setup(client):
    client.add_cog(Boludeces(client))
