import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import pymongo
import asyncio
import random
import os
import campus

mongo_url = os.getenv('MONGO_URL')

mongoclient = pymongo.MongoClient(mongo_url)

mongoprueba = mongoclient['Shellxactas']
mongoremindme = mongoprueba["remindme"]
mongocumple = mongoprueba["cumpleaños"]
mongocampus = mongoprueba['campus']

c = 0

status = ['Viendo al coscu', 'Estudiando', 'Preparando un golpe de estado', 'Leyendo el Don Quijote',
          'Haciendome una paja', 'Analizando el mercado', 'Comiendome a tu vieja']


class Loops(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.campus_loop.start()
        self.change_status.start()
        self.new_day.start()
        self.client.loop.create_task(self.upremindme())

    @tasks.loop(seconds=60.0)
    async def new_day(self):
        now = datetime.utcnow() - timedelta(hours=3)
        hournow = now.hour
        minnow = now.minute
        nowday = now.day
        nowmonth = now.month
        nowyear = now.year
        datenow = datetime(nowyear, nowmonth, nowday)
        if hournow == 0 and minnow == 0:
            mongocampus.insert_one({'date': datenow, 'times': 0})
            await self.check_for_bd()
            await self.campus_resumen(datenow)

    @new_day.before_loop
    async def before_new_day(self):
        await self.client.wait_until_ready()

    @tasks.loop(seconds=60.0)
    async def campus_loop(self):
        global c
        canal = self.client.get_channel(771116008861204513)
        estado = campus.estado_campus(15)
        now = datetime.utcnow() - timedelta(hours=3)
        nowday = now.day
        nowmonth = now.month
        nowyear = now.year
        datenow = datetime(nowyear, nowmonth, nowday)
        if c == 0 and estado:
            return
        if c == 1 and not estado:
            return
        if estado:
            await canal.send('El campus volvió.<a:tick:767588474840154173>')
            c = 0
            return
        if not estado:
            await canal.send('El campus se cayó.<a:cross:767588477231038475>')
            for x in mongocampus.find({'date': datenow}):
                mongocampus.update_one({'date': datenow}, {"$set": {'times': x['times'] + 1}})
            c = 1
            return

    @campus_loop.before_loop
    async def before_campus_loop(self):
        await self.client.wait_until_ready()

    @tasks.loop(minutes=20.0)
    async def change_status(self):
        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Game(random.choice(status)))

    @change_status.before_loop
    async def before_change_status(self):
        await self.client.wait_until_ready()

    async def upremindme(self):
        await self.client.wait_until_ready()
        for x in mongoremindme.find().sort('wait', pymongo.ASCENDING):
            nowtime = datetime.utcnow()
            authorid = int(x['authorid'])
            author = self.client.get_user(authorid)
            canalid = int(x['channelid'])
            canal = self.client.get_channel(canalid)
            record = x['recordatorio']
            url = x['url']
            dbwait = x['wait']
            if dbwait > nowtime:
                wait = dbwait - nowtime
                await asyncio.sleep(wait.total_seconds())
                if canal is None:
                    await author.send(f'{author.mention} ya pasó el tiempo. {record} {url}')
                else:
                    await canal.send(f'{author.mention} ya pasó el tiempo. {record} {url}')
                mongoremindme.delete_one(x)
            else:
                mongoremindme.delete_one(x)

    async def check_for_bd(self):
        await self.client.wait_until_ready()
        now = datetime.utcnow() - timedelta(hours=3)
        curmonth = now.month
        curday = now.day
        for bday in mongocumple.find():
            author = self.client.get_user(int(bday['_id']))
            channelid = int(bday['channelid'])
            channel = self.client.get_channel(channelid)
            dia = int(bday['dia'])
            mes = int(bday['mes'])
            if dia == curday and mes == curmonth:
                if channel is None:
                    await author.send(f'Feliz Cumpleaños {author.mention}!!!')
                else:
                    await channel.send(f'Feliz Cumpleaños {author.mention}!!!')

    async def campus_resumen(self, datenow):
        datenow = datenow - timedelta(days=1)
        canal = self.client.get_channel(771116008861204513)
        campus.plot()
        for x in mongocampus.find({'date': datenow}):
            times = x['times']
            await canal.send(f'Hoy el campus se cayó {times} veces.', file=discord.File('campus.png'))


def setup(client):
    client.add_cog(Loops(client))
