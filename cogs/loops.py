import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import pymongo
import asyncio
import random
import os
# import campus
import download_video

mongo_url = os.getenv('MONGO_URL')

mongoclient = pymongo.MongoClient(mongo_url)

mongoprueba = mongoclient['Shellxactas']
mongoremindme = mongoprueba["remindme"]
mongocumple = mongoprueba["cumpleaños"]
# mongocampus = mongoprueba['campus']
mongoexamenes = mongoprueba['Examenes']

c = 0
new = True

status = ['Preparando un golpe de estado', 'Haciendome una paja', 'Analizando el mercado', 'Comiendome a tu vieja', 'Cagando a piñas al dank memer', 'Meando en la esquina de tu casa', 'En la playa con tu vieja en tanga']


class Loops(commands.Cog):

    def __init__(self, client):
        self.client = client
        # self.campus_loop.start()
        self.change_status.start()
        self.new_day.start()
        self.client.loop.create_task(self.upremindme())

    @tasks.loop(seconds=30.0)
    async def new_day(self):
        global new
        now = datetime.utcnow() - timedelta(hours=3)
        hournow = now.hour
        minnow = now.minute
        nowday = now.day
        nowmonth = now.month
        nowyear = now.year
        datenow = datetime(nowyear, nowmonth, nowday)
        general = self.client.get_channel(734919493343641611)
        for i in [(0,0), (1,0), (1,1), (1,11), (1,23), (1,27), (2,0), (2,2), (2,22), (2,34), (3,0), (3,3), (3,14), (3,33), (3,45), (4,0), (4,20), (4,4), (4,44), (4,56), (5,0), (5,5), (5,55), (6,0), (6,54), (6,6), (7,0), (7,7), (8,0), (8,8), (9,0), (9,9), (10,0), (10,10), (11,0), (11,11), (12,0), (12,12), (13,0), (13,13), (14,0), (14,14), (15,0), (15,15), (16,0), (16,16), (17,0), (17,17), (18,0), (18,18), (19,0), (19,19), (20,0), (20,20), (21,0), (21,21), (22,0), (22,22), (23,0), (23,23)]:
            if hournow == i[0] and minnow == i[1]:
                await general.send(f'{i[0]}:{i[1]}')
        if hournow == 0 and minnow == 0 and new:
            # mongocampus.insert_one({'date': datenow, 'times': 0})
            await self.check_for_bd()
            # await self.campus_resumen(datenow)
            await self.volve_eze()
            await self.check_examenes()
            new = False
            return
        elif hournow == 0 and minnow == 0:
            return
        else:
            new = True
            return
        
    @new_day.before_loop
    async def before_new_day(self):
        await self.client.wait_until_ready()

    # @tasks.loop(seconds=60.0)
    # async def campus_loop(self):
    #     global c
    #     canal = self.client.get_channel(771116008861204513)
    #     estado = campus.estado_campus(15)
    #     now = datetime.utcnow() - timedelta(hours=3)
    #     nowday = now.day
    #     nowmonth = now.month
    #     nowyear = now.year
    #     datenow = datetime(nowyear, nowmonth, nowday)
    #     if c == 0 and estado:
    #         return
    #     if c == 1 and not estado:
    #         return
    #     if estado:
    #         await canal.send('El campus volvió.<a:tick:767588474840154173> <@&778645823503466546>')
    #         c = 0
    #         return
    #     if not estado:
    #         await canal.send('El campus se cayó.<a:cross:767588477231038475> <@&778645823503466546>')
    #         x = mongocampus.find_one({'date': datenow})
    #         if x is None:
    #             mongocampus.insert_one({'date': datenow, 'times': 1})
    #         else:
    #             mongocampus.update_one({'date': datenow}, {"$set": {'times': x['times'] + 1}})
    #         c = 1
    #         return

    # @campus_loop.before_loop
    # async def before_campus_loop(self):
    #     await self.client.wait_until_ready()

    @tasks.loop(hours=1.0)
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

    # async def campus_resumen(self, datenow):
    #     datenow = datenow - timedelta(days=1)
    #     canal = self.client.get_channel(771116008861204513)
    #     campus.plot()
    #     for x in mongocampus.find({'date': datenow}):
    #         times = x['times']
    #         await canal.send(f'Hoy el campus se cayó {times} veces.', file=discord.File('campus.png'))
    
    async def volve_eze(self):
        canal = self.client.get_channel(734919493343641611)
        await canal.send("<@699664841127755807> VOLVÉ!!!!")
    
    async def check_examenes(self):
        await self.client.wait_until_ready()
        now = datetime.utcnow() - timedelta(hours=3)
        for x in mongoexamenes.find():
            if x['date'] + timedelta(hours=24) < now:
                mongoexamenes.delete_one(x)

    

def setup(client):
    client.add_cog(Loops(client))
