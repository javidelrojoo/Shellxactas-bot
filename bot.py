import discord
from discord.ext import commands, tasks
import os
import time
import asyncio
import random
import subprocess
import requests
import pymongo
from datetime import datetime, timedelta, time

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='.', status=discord.Status.dnd, case_insensitive=True,
                      description='El bot de Shellxactas', intents=intents)

status = ['Viendo al coscu', 'Estudiando', 'Preparando un golpe de estado', 'Leyendo el Don Quijote',
          'Haciendome una paja', 'Analizando el mercado', 'Comiendome a tu vieja']

if __name__ == '__main__':
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

mongo_url = os.getenv('MONGO_URL')

mongoclient = pymongo.MongoClient(mongo_url)

mongoprueba = mongoclient['Shellxactas']
mongoremindme = mongoprueba["remindme"]
mongocumple = mongoprueba["cumpleaños"]


@client.event
async def on_ready():
    change_status.start()
    print('Loggeado como:')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await check_for_bd.start()


@tasks.loop(minutes=20.0)
async def change_status():
    print('Arrancó el loop de change status')
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(random.choice(status)))


@tasks.loop(hours=24.0)
async def check_for_bd():
    print('Arrancó el loop del bday')
    now = datetime.utcnow()-timedelta(hours=3)
    curmonth = now.month
    curday = now.day
    for bday in mongocumple.find():
        author = client.get_user(int(bday['_id']))
        channelid = int(bday['channelid'])
        channel = client.get_channel(channelid)
        dia = int(bday['dia'])
        mes = int(bday['mes'])
        if dia == curday and mes == curmonth:
            if channel is None:
                await author.send(f'Feliz Cumpleaños {author.mention}!!!')
            else:
                await channel.send(f'Feliz Cumpleaños {author.mention}!!!')


@check_for_bd.before_loop
async def before_checkbd():
    await client.wait_until_ready()


async def upremindme():
    await client.wait_until_ready()
    print('Arrancó el upremindme')
    nowtime = datetime.utcnow()
    for x in mongoremindme.find().sort('wait', pymongo.ASCENDING):
        authorid = int(x['authorid'])
        author = client.get_user(authorid)
        canalid = int(x['channelid'])
        canal = client.get_channel(canalid)
        record = x['recordatorio']
        url = x['url']
        dbwait = x['wait']
        if dbwait > nowtime:
            wait = dbwait-nowtime
            await asyncio.sleep(wait.total_seconds())
            if canal is None:
                await author.send(f'{author.mention} ya pasó el tiempo. {record} {url}')
            else:
                await canal.send(f'{author.mention} ya pasó el tiempo. {record} {url}')
            mongoremindme.delete_one(x)
        else:
            mongoremindme.delete_one(x)

client.loop.create_task(upremindme())

token = os.getenv('TOKEN')

client.run(token)
