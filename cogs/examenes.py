import discord
from discord.ext import commands
import os
import pymongo
import asyncio
from bson.objectid import ObjectId
import bson

mongo_url = os.getenv('MONGO_URL')

mongoclient = pymongo.MongoClient(mongo_url)
mongoprueba = mongoclient['Shellxactas']
mongoexamenes = mongoprueba['Examenes']

class Examenes(commands.Cog):

    def __init__(self, client):
        self.client = client
        

    @commands.group(invoke_without_command=True)
    async def examenes(self, ctx):
        embed=discord.Embed(title="Próximos Exámenes")
        for x in mongoexamenes.find().sort([('mes', pymongo.ASCENDING), ('dia', pymongo.ASCENDING)]):
            embed.add_field(name=f"{x['title']} ({x['dia']}/{x['mes']})", value='\n'.join([self.client.get_user(i).mention for i in x['names']]), inline=False)
        await ctx.send(embed=embed)

    @examenes.command()
    async def ids(self, ctx):
        embed=discord.Embed(title="Próximos Exámenes")
        for x in mongoexamenes.find().sort([('mes', pymongo.ASCENDING), ('dia', pymongo.ASCENDING)]):
            embed.add_field(name=f"{x['title']} ({x['dia']}/{x['mes']})", value=x['_id'], inline=False)
        await ctx.send(embed=embed)

    @examenes.command(aliases=['add'])
    async def agregar(self, ctx):

        def check_author(m):
            return m.author == ctx.message.author
        
        async def clear_all():
            for i in msg_sent:
                await i.delete(delay=1.)
            return


        msg_sent = [ctx.message]

        msg1 = await ctx.send("¿Que fecha es? (En formato DD/MM)")
        msg_sent.append(msg1)
        try:
            res_fecha = await self.client.wait_for("message", check=check_author, timeout=30.)
            msg_sent.append(res_fecha)
            dia, mes = res_fecha.content.split('/')
            dia = int(dia)
            mes = int(mes)
        except ValueError:
            error_msg1 = await ctx.send('Formato Inválido, tiene que ser de la forma \'DD/MM\'')
            msg_sent.append(error_msg1)
            await asyncio.sleep(5.)
            return await clear_all()
        except asyncio.TimeoutError:
            return await clear_all()
        
        if dia > 31 or dia < 0:
            error_msg2 = await ctx.send('Día Inválido')
            msg_sent.append(error_msg2)
            await asyncio.sleep(5.)
            return await clear_all()
        if mes > 12 or mes < 0:
            error_msg3 = await ctx.send('Mes Inválido')
            msg_sent.append(error_msg3)
            await asyncio.sleep(5.)
            return await clear_all()
        
        msg2 = await ctx.send('¿Que examén es?')
        msg_sent.append(msg2)
        try:
            res_title = await self.client.wait_for("message", check=check_author, timeout=30.)
            msg_sent.append(res_title)
            title = res_title.content
        except asyncio.TimeoutError:
            return await clear_all()
        
        msg3 = await ctx.send('¿Quienes rinden?')
        msg_sent.append(msg3)
        try:
            res_names = await self.client.wait_for("message", check=check_author, timeout=30.)
            msg_sent.append(res_names)
            if not res_names.mentions:
                error_msg4 = await ctx.send('Me tenés que decir alguien')
                msg_sent.append(error_msg4)
                await asyncio.sleep(5.)
                return await clear_all()
            names = [i.id for i in res_names.mentions]
        except asyncio.TimeoutError:
            return await clear_all()
        
        result = mongoexamenes.insert_one({'dia': dia, 'mes': mes, 'title': title, 'names': names})
        embed=discord.Embed(title="Se agregó el examen")
        embed.add_field(name=f"{title} ({dia}/{mes})", value='\n'.join([self.client.get_user(i).mention for i in names]), inline=False)
        embed.set_footer(text= result.inserted_id)
        await ctx.send(embed=embed)
        await asyncio.sleep(5.)
        return await clear_all()
    
    @examenes.command(aliases=['edit'])
    async def editar(self, ctx):

        def check_author(m):
            return m.author == ctx.message.author
        
        async def clear_all():
            for i in msg_sent:
                await i.delete(delay=1.)
            return
        
        msg_sent = [ctx.message]
        
        msg0 = await ctx.send("¿Cual es la ID del exámen? (la podes ver poniendo .examenes ids)")
        msg_sent.append(msg0)
        try:
            res_ids = await self.client.wait_for("message", check=check_author, timeout=30.)
            result = mongoexamenes.find_one({'_id': ObjectId(res_ids.content)})
            if result is None:
                raise bson.errors.InvalidId
        except bson.errors.InvalidId:
            error_msg1 = await ctx.send("Esa ID no existe")
            msg_sent.append(error_msg1)
            await asyncio.sleep(5.)
            return await clear_all()
        except asyncio.TimeoutError:
            return await clear_all()
        
        msg1 = await ctx.send("¿Que fecha es? (En formato DD/MM)")
        msg_sent.append(msg1)
        try:
            res_fecha = await self.client.wait_for("message", check=check_author, timeout=30.)
            msg_sent.append(res_fecha)
            dia, mes = res_fecha.content.split('/')
            dia = int(dia)
            mes = int(mes)
        except ValueError:
            error_msg1 = await ctx.send('Formato Inválido, tiene que ser de la forma \'DD/MM\'')
            msg_sent.append(error_msg1)
            await asyncio.sleep(5.)
            return await clear_all()
        except asyncio.TimeoutError:
            return await clear_all()
        
        if dia > 31 or dia < 0:
            error_msg2 = await ctx.send('Día Inválido')
            msg_sent.append(error_msg2)
            await asyncio.sleep(5.)
            return await clear_all()
        if mes > 12 or mes < 0:
            error_msg3 = await ctx.send('Mes Inválido')
            msg_sent.append(error_msg3)
            await asyncio.sleep(5.)
            return await clear_all()
        
        msg2 = await ctx.send('¿Que examén es?')
        msg_sent.append(msg2)
        try:
            res_title = await self.client.wait_for("message", check=check_author, timeout=30.)
            msg_sent.append(res_title)
            title = res_title.content
        except asyncio.TimeoutError:
            return await clear_all()
        
        msg3 = await ctx.send('¿Quienes rinden?')
        msg_sent.append(msg3)
        try:
            res_names = await self.client.wait_for("message", check=check_author, timeout=30.)
            msg_sent.append(res_names)
            if not res_names.mentions:
                error_msg4 = await ctx.send('Me tenés que decir alguien')
                msg_sent.append(error_msg4)
                await asyncio.sleep(5.)
                return await clear_all()
            names = [i.id for i in res_names.mentions]
        except asyncio.TimeoutError:
            return await clear_all()
        
        mongoexamenes.find_one_and_replace({'_id': ObjectId(res_ids.content)}, {'dia': dia, 'mes': mes, 'title': title, 'names': names})
        embed=discord.Embed(title="Se editó el examen")
        embed.add_field(name=f"{title} ({dia}/{mes})", value='\n'.join([self.client.get_user(i).mention for i in names]), inline=False)
        embed.set_footer(text= res_ids.content)
        await ctx.send(embed=embed)
        await asyncio.sleep(5.)
        return await clear_all()


def setup(client):
    client.add_cog(Examenes(client))